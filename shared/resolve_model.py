#!/usr/bin/env python3
"""Resolve a Preflight task assignment from defaults and one optional override."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from types import ModuleType
from typing import Any, TypedDict

try:
    import yaml as _yaml
except ImportError:
    yaml: ModuleType | None = None
else:
    yaml = _yaml


COMPLEXITIES = ("routine", "complex", "high-risk")
PROFILE_NAMES = ("baseline", "optimised")


class Assignment(TypedDict):
    model: str
    alias: str
    reasoning_effort: str
    workflow: str
    role: str
    complexity: str | None
    config_path: str
    source: str
    profile: str


class ConfigError(Exception):
    pass


if yaml is not None:

    class UniqueKeyLoader(_yaml.SafeLoader):
        pass

    def unique_mapping(
        loader: UniqueKeyLoader, node: _yaml.MappingNode
    ) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=True)
            if not isinstance(key, str):
                raise ConfigError(
                    f"mapping key must be a string at line {key_node.start_mark.line + 1}"
                )
            if key in result:
                raise ConfigError(
                    f"duplicate YAML key {key!r} at line {key_node.start_mark.line + 1}"
                )
            result[key] = loader.construct_object(value_node, deep=True)
        return result

    UniqueKeyLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping
    )


def read_yaml(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise ConfigError(
            "PyYAML is required to resolve model roles; use an existing Python environment with PyYAML"
        )
    try:
        value = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    except (OSError, UnicodeError) as error:
        raise ConfigError(f"cannot read model configuration {path}: {error}") from error
    except yaml.YAMLError as error:
        raise ConfigError(f"invalid YAML in {path}: {error}") from error
    if not isinstance(value, dict):
        raise ConfigError(f"model configuration must be a mapping: {path}")
    return value


def mapping(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ConfigError(f"{context} must be a mapping")
    return value


def keys(value: dict[str, Any], allowed: set[str], context: str) -> None:
    unknown = value.keys() - allowed
    if unknown:
        raise ConfigError(f"unknown {context} key: {', '.join(sorted(unknown))}")


def nonempty(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"{context} must be a nonempty string")
    return value


def profile(value: Any, context: str, *, complexity: bool = False) -> dict[str, Any]:
    entry = mapping(value, context)
    keys(
        entry,
        {"model", "reasoning_effort"}
        if complexity
        else {"model", "reasoning_effort", "complexity"},
        context,
    )
    for field in ("model", "reasoning_effort"):
        if field in entry:
            nonempty(entry[field], f"{context}.{field}")
    if not complexity and "complexity" in entry:
        levels = mapping(entry["complexity"], f"{context}.complexity")
        keys(levels, set(COMPLEXITIES), f"{context}.complexity")
        for level, level_profile in levels.items():
            profile(level_profile, f"{context}.complexity.{level}", complexity=True)
    return entry


def validate_v2(
    value: dict[str, Any], context: str, base: dict[str, Any] | None = None
) -> None:
    keys(
        value,
        {"version", "models", "defaults", "workflows", "profile", "profiles"},
        context,
    )
    if type(value.get("version")) is not int or value["version"] != 2:
        raise ConfigError(f"{context}.version must be 2")
    if base is None:
        for field in ("models", "defaults", "workflows"):
            if field not in value:
                raise ConfigError(f"{context}.{field} is required")
    models = mapping(value.get("models", {}), f"{context}.models")
    for alias, model_id in models.items():
        nonempty(alias, f"{context}.models alias")
        nonempty(model_id, f"{context}.models.{alias}")
    if base is None and not models:
        raise ConfigError(f"{context}.models must contain at least one alias")
    defaults = mapping(value.get("defaults", {}), f"{context}.defaults")
    keys(defaults, {"model", "reasoning_effort"}, f"{context}.defaults")
    for field, entry in defaults.items():
        nonempty(entry, f"{context}.defaults.{field}")
    if base is None and set(defaults) != {"model", "reasoning_effort"}:
        raise ConfigError(f"{context}.defaults must contain model and reasoning_effort")
    workflows = mapping(value.get("workflows", {}), f"{context}.workflows")
    if base is not None:
        keys(workflows, set(base["workflows"]), f"{context}.workflows")
    for workflow, workflow_value in workflows.items():
        block = mapping(workflow_value, f"{context}.workflows.{workflow}")
        keys(block, {"roles"}, f"{context}.workflows.{workflow}")
        if base is None and "roles" not in block:
            raise ConfigError(f"{context}.workflows.{workflow}.roles is required")
        roles = mapping(block.get("roles", {}), f"{context}.workflows.{workflow}.roles")
        if base is not None:
            keys(
                roles,
                set(base["workflows"][workflow]["roles"]),
                f"{context}.workflows.{workflow}.roles",
            )
        for role, role_value in roles.items():
            profile(role_value, f"{context}.workflows.{workflow}.roles.{role}")
    if base is None and not workflows:
        raise ConfigError(f"{context}.workflows must contain at least one workflow")
    if "profile" in value:
        selected = value["profile"]
        if selected not in PROFILE_NAMES:
            raise ConfigError(
                f"{context}.profile must be one of: {', '.join(PROFILE_NAMES)}"
            )
    profiles = mapping(value.get("profiles", {}), f"{context}.profiles")
    keys(profiles, set(PROFILE_NAMES), f"{context}.profiles")
    profile_base = base if base is not None else value
    for name, overlay in profiles.items():
        validate_profile_overlay(overlay, f"{context}.profiles.{name}", profile_base)


def validate_profile_overlay(value: Any, context: str, base: dict[str, Any]) -> None:
    overlay = mapping(value, context)
    keys(overlay, {"defaults", "workflows"}, context)
    defaults = mapping(overlay.get("defaults", {}), f"{context}.defaults")
    keys(defaults, {"model", "reasoning_effort"}, f"{context}.defaults")
    for field, entry in defaults.items():
        nonempty(entry, f"{context}.defaults.{field}")
    workflows = mapping(overlay.get("workflows", {}), f"{context}.workflows")
    keys(workflows, set(base["workflows"]), f"{context}.workflows")
    for workflow, workflow_value in workflows.items():
        block = mapping(workflow_value, f"{context}.workflows.{workflow}")
        keys(block, {"roles"}, f"{context}.workflows.{workflow}")
        roles = mapping(block.get("roles", {}), f"{context}.workflows.{workflow}.roles")
        keys(
            roles,
            set(base["workflows"][workflow]["roles"]),
            f"{context}.workflows.{workflow}.roles",
        )
        for role, role_value in roles.items():
            profile(role_value, f"{context}.workflows.{workflow}.roles.{role}")


def merged_v2(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "models": {**base["models"], **override.get("models", {})},
        "defaults": {**base["defaults"], **override.get("defaults", {})},
        "workflows": {},
    }
    for workflow, block in base["workflows"].items():
        changed_roles = override.get("workflows", {}).get(workflow, {}).get("roles", {})
        roles = {}
        for role, base_profile in block["roles"].items():
            change = changed_roles.get(role, {})
            roles[role] = {
                **base_profile,
                **{
                    field: entry
                    for field, entry in change.items()
                    if field != "complexity"
                },
                "complexity": {
                    **base_profile.get("complexity", {}),
                    **{
                        level: {
                            **base_profile.get("complexity", {}).get(level, {}),
                            **entry,
                        }
                        for level, entry in change.get("complexity", {}).items()
                    },
                },
            }
        result["workflows"][workflow] = {"roles": roles}
    aliases = result["models"]
    for alias, model_id in aliases.items():
        if model_id in aliases:
            raise ConfigError(
                f"model alias {alias!r} must name a concrete model ID, not alias {model_id!r}"
            )
    for context, entry in [("defaults", result["defaults"])] + [
        (f"{workflow}.{role}", item)
        for workflow, block in result["workflows"].items()
        for role, item in block["roles"].items()
    ]:
        candidates = [entry] + list(entry.get("complexity", {}).values())
        for candidate in candidates:
            alias = candidate.get("model")
            if alias is not None and alias not in aliases:
                raise ConfigError(f"unknown model alias {alias!r} in {context}")
    return result


def profile_overlay(config: dict[str, Any], name: str) -> dict[str, Any]:
    overlay: dict[str, Any] = config.get("profiles", {}).get(name, {})
    return overlay


def selected_profile(config: dict[str, Any]) -> str:
    selected: str = config.get("profile", "baseline")
    return selected


def effective_profiles(
    shipped: dict[str, Any], override: dict[str, Any] | None = None
) -> dict[str, dict[str, Any]]:
    """Validate and merge both profiles using the resolver's override precedence."""
    validate_v2(shipped, "defaults")
    shipped_root = merged_v2(shipped, {})
    if override is not None:
        validate_v2(override, "override", shipped)
    profiles = {}
    for name in PROFILE_NAMES:
        config = merged_v2(shipped_root, profile_overlay(shipped, name))
        if override is not None:
            config = merged_v2(config, override)
            config = merged_v2(config, profile_overlay(override, name))
        profiles[name] = config
    return profiles


def assignment_values(
    config: dict[str, Any], workflow: str, role: str, complexity: str | None
) -> tuple[str, str, str]:
    """Resolve one assignment from an already validated effective profile."""
    if workflow not in config["workflows"]:
        raise ConfigError(f"unknown workflow {workflow!r}")
    roles = config["workflows"][workflow]["roles"]
    if role not in roles:
        raise ConfigError(f"unknown role {role!r} in workflow {workflow!r}")
    chosen = roles[role]
    level = chosen.get("complexity", {}).get(complexity, {})
    alias = level.get("model", chosen.get("model", config["defaults"]["model"]))
    effort = level.get(
        "reasoning_effort",
        chosen.get("reasoning_effort", config["defaults"]["reasoning_effort"]),
    )
    return config["models"][alias], alias, effort


def default_path() -> Path:
    beside = Path(__file__).resolve().with_name("model-roles.default.yaml")
    return (
        beside
        if beside.is_file()
        else Path(__file__).resolve().parent.parent
        / "config"
        / "model-roles.default.yaml"
    )


def resolve(
    workflow: str,
    role: str,
    complexity: str | None,
    repo: Path,
    user_config: Path | None = None,
    defaults: Path | None = None,
) -> Assignment:
    if complexity is not None and complexity not in COMPLEXITIES:
        raise ConfigError(f"unknown complexity {complexity!r}")
    if not repo.is_dir():
        raise ConfigError(f"repository directory does not exist: {repo}")
    shipped_path = defaults if defaults is not None else default_path()
    shipped = read_yaml(shipped_path)
    validate_v2(shipped, str(shipped_path))
    repo_path = repo / ".preflight" / "model-roles.yaml"
    user_path = (
        user_config
        if user_config is not None
        else Path.home() / ".config" / "preflight" / "model-roles.yaml"
    )
    if repo_path.exists() or repo_path.is_symlink():
        selected = repo_path
    elif user_path.exists() or user_path.is_symlink() or user_config is not None:
        selected = user_path
    else:
        selected = None
    source = "default" if selected is None else "override"
    override = read_yaml(selected) if selected is not None else None
    profiles = effective_profiles(shipped, override)
    active_profile = (
        selected_profile(override)
        if override is not None and "profile" in override
        else selected_profile(shipped)
    )
    model, alias, effort = assignment_values(
        profiles[active_profile], workflow, role, complexity
    )
    return {
        "model": model,
        "alias": alias,
        "reasoning_effort": effort,
        "workflow": workflow,
        "role": role,
        "complexity": complexity,
        "config_path": str(selected or shipped_path),
        "source": source,
        "profile": active_profile,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workflow", required=True)
    parser.add_argument("--role", required=True)
    parser.add_argument("--complexity", choices=COMPLEXITIES)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--user-config", type=Path)
    parser.add_argument("--defaults", type=Path)
    args = parser.parse_args()
    try:
        result = resolve(
            args.workflow,
            args.role,
            args.complexity,
            args.repo,
            args.user_config,
            args.defaults,
        )
    except ConfigError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
