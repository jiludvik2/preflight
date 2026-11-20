#!/usr/bin/env python3
"""Discover a runtime catalog, preview explicit model edits, then write a reviewed plan."""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import stat
import subprocess
import sys
import tempfile
import time
from typing import Any
import uuid

from resolve_model import (
    COMPLEXITIES,
    ConfigError,
    assignment_values,
    default_path,
    effective_profiles,
    mapping,
    nonempty,
    read_yaml,
    yaml,
)

MAX_BYTES = 2 * 1024 * 1024
SYSTEM_DIRECTORY_ALIASES = {
    Path("/tmp"): Path("/private/tmp"),
    Path("/var"): Path("/private/var"),
}


def absolute(path: Path) -> Path:
    return Path(os.path.abspath(path.expanduser()))


def regular_path(path: Path) -> None:
    """Refuse links except verified macOS system directory aliases in ancestors."""
    for part in reversed((path, *path.parents)):
        if part.is_symlink() and not (
            part != path and SYSTEM_DIRECTORY_ALIASES.get(part) == part.resolve()
        ):
            raise ConfigError(f"symlinks are not supported: {part}")
        if part.exists() and part != path and not part.is_dir():
            raise ConfigError(f"parent is not a directory: {part}")
    if path.exists() and not path.is_file():
        raise ConfigError(f"not a regular file: {path}")


def file_bytes(path: Path) -> bytes | None:
    regular_path(path)
    if not path.exists():
        return None
    if path.stat().st_size > MAX_BYTES:
        raise ConfigError(f"file exceeds {MAX_BYTES} bytes: {path}")
    data = path.read_bytes()
    if len(data) > MAX_BYTES:
        raise ConfigError(f"file exceeds {MAX_BYTES} bytes: {path}")
    return data


def snapshot(path: Path) -> dict[str, Any]:
    value = file_bytes(path)
    return {
        "path": str(path),
        "sha256": hashlib.sha256(value).hexdigest() if value is not None else None,
    }


def read_json(path: Path) -> dict[str, Any]:
    value = file_bytes(path)
    if value is None:
        raise ConfigError(f"file does not exist: {path}")
    try:
        return mapping(json.loads(value), "JSON document")
    except (ValueError, UnicodeError) as error:
        raise ConfigError(f"invalid JSON document: {path}") from error


def catalog_models(catalog: dict[str, Any]) -> dict[str, set[str]]:
    if type(catalog.get("version")) is not int or catalog["version"] != 1:
        raise ConfigError("catalog.version must be 1")
    if catalog.get("runtime") not in ("codex", "claude-code"):
        raise ConfigError("catalog.runtime must be codex or claude-code")
    observed_at = nonempty(catalog.get("observed_at"), "catalog.observed_at")
    try:
        if (
            re.fullmatch(
                r"\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[Zz]|[+-]\d{2}:[0-5]\d)",
                observed_at,
            )
            is None
        ):
            raise ValueError("not RFC3339")
        timestamp = datetime.fromisoformat(
            observed_at[:-1] + "+00:00" if observed_at[-1] in "Zz" else observed_at
        )
        if timestamp.utcoffset() is None:
            raise ValueError("timezone is required")
    except ValueError as error:
        raise ConfigError(
            "catalog.observed_at must be a timezone-aware RFC3339 timestamp"
        ) from error
    provenance = nonempty(catalog.get("provenance"), "catalog.provenance")
    if provenance not in ("codex-app-server", "user-confirmed"):
        raise ConfigError(
            "catalog.provenance must be codex-app-server or user-confirmed"
        )
    if catalog["runtime"] == "claude-code" and provenance != "user-confirmed":
        raise ConfigError(
            "Claude catalogs must be user-confirmed in the target runtime"
        )
    models = catalog.get("models")
    if not isinstance(models, list) or not models:
        raise ConfigError("catalog.models must be a nonempty list")
    result: dict[str, set[str]] = {}
    for entry in models:
        record = mapping(entry, "catalog model")
        selector = nonempty(record.get("selector"), "model.selector")
        efforts = record.get("supported_reasoning_efforts")
        if not isinstance(efforts, list):
            raise ConfigError(
                f"model {selector!r} needs explicit supported_reasoning_efforts"
            )
        supported = {nonempty(effort, "reasoning effort") for effort in efforts}
        if selector in result:
            raise ConfigError(f"duplicate catalog selector: {selector!r}")
        result[selector] = supported
    return result


class CodexCatalog:
    """A bounded JSON-lines app-server session; it never creates a thread or turn."""

    def __init__(self, process: subprocess.Popen[bytes], timeout: float) -> None:
        self.process = process
        self.deadline = time.monotonic() + timeout
        self.buffer = b""
        self.received = 0
        self.selector = selectors.DefaultSelector()
        assert process.stdout is not None
        self.selector.register(process.stdout, selectors.EVENT_READ)

    def send(
        self, method: str, params: dict[str, Any] | None, request_id: int | None
    ) -> None:
        message: dict[str, Any] = {"method": method}
        if params is not None:
            message["params"] = params
        if request_id is not None:
            message["id"] = request_id
        assert self.process.stdin is not None
        try:
            self.process.stdin.write(json.dumps(message).encode() + b"\n")
            self.process.stdin.flush()
        except (BrokenPipeError, OSError) as error:
            raise ConfigError("Codex app-server closed its input") from error

    def response(self, request_id: int) -> dict[str, Any]:
        while True:
            if b"\n" in self.buffer:
                line, self.buffer = self.buffer.split(b"\n", 1)
                try:
                    message = mapping(json.loads(line), "app-server message")
                except (ValueError, UnicodeError, ConfigError) as error:
                    raise ConfigError(
                        "Codex app-server returned an invalid message"
                    ) from error
                if message.get("id") != request_id:
                    continue
                if "error" in message:
                    raise ConfigError(
                        "Codex app-server rejected the catalog request; check CLI login and version"
                    )
                return mapping(message.get("result"), "app-server result")
            remaining = self.deadline - time.monotonic()
            if remaining <= 0 or not self.selector.select(remaining):
                raise ConfigError("Codex model discovery timed out")
            assert self.process.stdout is not None
            chunk = os.read(self.process.stdout.fileno(), 65536)
            if not chunk:
                raise ConfigError(
                    "Codex app-server exited before completing model discovery"
                )
            self.received += len(chunk)
            if self.received > MAX_BYTES:
                raise ConfigError("Codex model discovery exceeded its output limit")
            self.buffer += chunk


def discover_codex(timeout: float = 15.0) -> dict[str, Any]:
    try:
        process = subprocess.Popen(
            ["codex", "app-server", "--listen", "stdio://"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except OSError as error:
        raise ConfigError(
            "cannot start codex app-server; install and sign into the target Codex CLI"
        ) from error
    session = CodexCatalog(process, timeout)
    try:
        session.send(
            "initialize", {"clientInfo": {"name": "preflight", "version": "0.1.0"}}, 0
        )
        session.response(0)
        session.send("initialized", None, None)
        records = []
        cursor: str | None = None
        cursors: set[str] = set()
        request_id = 1
        while True:
            session.send("model/list", {"cursor": cursor}, request_id)
            result = session.response(request_id)
            entries = result.get("data")
            if not isinstance(entries, list):
                raise ConfigError("Codex model/list did not return a model list")
            for entry in entries:
                record = mapping(entry, "Codex model")
                selector = nonempty(
                    record.get("model") or record.get("id"), "Codex model selector"
                )
                supported = record.get("supportedReasoningEfforts", [])
                if not isinstance(supported, list):
                    raise ConfigError(
                        "Codex model has no explicit reasoning effort capabilities"
                    )
                efforts = [
                    nonempty(
                        mapping(item, "Codex effort").get("reasoningEffort"),
                        "Codex reasoning effort",
                    )
                    for item in supported
                ]
                records.append(
                    {"selector": selector, "supported_reasoning_efforts": efforts}
                )
            cursor = result.get("nextCursor")
            if cursor is None:
                break
            if not isinstance(cursor, str) or not cursor or cursor in cursors:
                raise ConfigError(
                    "Codex model/list returned an invalid pagination cursor"
                )
            cursors.add(cursor)
            request_id += 1
        catalog = {
            "version": 1,
            "runtime": "codex",
            "observed_at": datetime.now(timezone.utc).isoformat(),
            "provenance": "codex-app-server",
            "models": records,
        }
        catalog_models(catalog)
        return catalog
    finally:
        session.selector.close()
        if process.stdin is not None:
            process.stdin.close()
        try:
            process.wait(timeout=1)
        except subprocess.TimeoutExpired:
            process.terminate()
            try:
                process.wait(timeout=1)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        if process.stdout is not None:
            process.stdout.close()


def edits(values: list[str], context: str) -> dict[str, str]:
    result = {}
    for value in values:
        key, separator, entry = value.partition("=")
        if not separator or not key or not entry or key in result:
            raise ConfigError(f"{context} expects distinct name=value edits")
        result[key] = entry
    return result


def change_config(
    shipped: dict[str, Any],
    original: dict[str, Any],
    models: dict[str, str],
    efforts: dict[str, str],
) -> dict[str, Any]:
    proposed = deepcopy(original)
    aliases = effective_profiles(shipped, proposed)["baseline"]["models"]
    for alias, selector in sorted(models.items()):
        if alias not in aliases:
            raise ConfigError(f"unknown model alias: {alias!r}")
        proposed.setdefault("models", {})[alias] = nonempty(selector, "model selector")
    for path, effort in sorted(efforts.items()):
        parts = path.split(".")
        if parts[-1] != "reasoning_effort" or len(parts) < 2:
            raise ConfigError("effort edits must name an exact reasoning_effort leaf")
        entry = proposed
        for part in parts[:-1]:
            entry = mapping(entry.setdefault(part, {}), "effort edit path")
        entry[parts[-1]] = nonempty(effort, "reasoning effort")
    effective_profiles(shipped, proposed)
    return proposed


def checked_assignments(
    shipped: dict[str, Any], proposed: dict[str, Any], catalog: dict[str, Any]
) -> list[dict[str, Any]]:
    available = catalog_models(catalog)
    assignments = []
    for profile, config in effective_profiles(shipped, proposed).items():
        for workflow, block in config["workflows"].items():
            for role in block["roles"]:
                for complexity in (None, *COMPLEXITIES):
                    model, alias, effort = assignment_values(
                        config, workflow, role, complexity
                    )
                    context = (
                        f"{profile}/{workflow}/{role}/{complexity or 'unspecified'}"
                    )
                    if model not in available:
                        raise ConfigError(
                            f"{context}: selector {model!r} is absent from the catalog"
                        )
                    if effort not in available[model]:
                        raise ConfigError(
                            f"{context}: selector {model!r} does not support effort {effort!r}"
                        )
                    assignments.append(
                        {
                            "profile": profile,
                            "workflow": workflow,
                            "role": role,
                            "complexity": complexity,
                            "model": model,
                            "alias": alias,
                            "reasoning_effort": effort,
                        }
                    )
    return assignments


def preview(
    catalog_path: Path,
    repo: Path,
    scope: str,
    models: dict[str, str],
    efforts: dict[str, str],
    *,
    user_config: Path | None = None,
    defaults: Path | None = None,
    target: Path | None = None,
) -> dict[str, Any]:
    if not repo.is_dir():
        raise ConfigError(f"repository directory does not exist: {repo}")
    if scope not in ("project", "user"):
        raise ConfigError("scope must be project or user")
    repo = absolute(repo)
    catalog_path = absolute(catalog_path)
    shipped_path = absolute(defaults or default_path())
    user_path = absolute(
        user_config or Path.home() / ".config/preflight/model-roles.yaml"
    )
    project_path = repo / ".preflight/model-roles.yaml"
    target_path = absolute(
        target or (project_path if scope == "project" else user_path)
    )
    if target_path in (shipped_path, catalog_path):
        raise ConfigError(
            "configuration target must be separate from defaults and catalog"
        )
    paths = [shipped_path, catalog_path, target_path]
    inherited = scope == "project" and file_bytes(target_path) is None
    if inherited:
        paths.append(user_path)
    if scope == "user":
        paths.append(project_path)
    sources = [snapshot(path) for path in dict.fromkeys(paths)]
    catalog = read_json(catalog_path)
    shipped = read_yaml(shipped_path)
    original_path = user_path if inherited else target_path
    original = (
        read_yaml(original_path)
        if file_bytes(original_path) is not None
        else {"version": 2}
    )
    proposed = change_config(shipped, original, models, efforts)
    assignments = checked_assignments(shipped, proposed, catalog)
    original_bytes = file_bytes(target_path)
    if yaml is None:
        raise ConfigError("PyYAML is required to configure model roles")
    text = (
        original_bytes.decode("utf-8")
        if proposed == original and original_bytes is not None
        else yaml.safe_dump(proposed, sort_keys=False)
    )
    warnings = [
        "Catalog availability was observed at "
        + catalog["observed_at"]
        + "; write does not refresh availability or switch runtimes."
    ]
    if original_bytes is not None and text.encode() != original_bytes:
        warnings.append(
            "Writing normalizes YAML formatting and comments; original bytes will be backed up."
        )
    if inherited and file_bytes(user_path) is not None:
        warnings.append(
            "The new project file includes the current user override, preserving its customization."
        )
    if scope == "user" and file_bytes(project_path) is not None:
        warnings.append(
            "This repository has a project override which shadows the user configuration."
        )
    if sources != [snapshot(Path(source["path"])) for source in sources]:
        raise ConfigError("configuration inputs changed during preview; retry")
    return {
        "version": 1,
        "runtime": catalog["runtime"],
        "repo": str(repo),
        "scope": scope,
        "catalog_path": str(catalog_path),
        "defaults_path": str(shipped_path),
        "user_config": str(user_path),
        "target": str(target_path),
        "sources": sources,
        "models": models,
        "efforts": efforts,
        "proposed_yaml": text,
        "assignments": assignments,
        "warnings": warnings,
    }


def exclusive_json(path: Path, value: dict[str, Any]) -> None:
    regular_path(path)
    data = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    with path.open("xb") as output:
        output.write(data)


def write_plan(plan_path: Path, catalog_path: Path) -> dict[str, Any]:
    plan = read_json(absolute(plan_path))
    if plan.get("version") != 1 or plan.get("catalog_path") != str(
        absolute(catalog_path)
    ):
        raise ConfigError("plan version or catalog path does not match")
    sources = plan.get("sources")
    if not isinstance(sources, list):
        raise ConfigError("invalid plan sources")
    for source in sources:
        record = mapping(source, "plan source")
        if record != snapshot(Path(nonempty(record.get("path"), "source path"))):
            raise ConfigError(
                "a catalog, default, or configuration input changed; preview again"
            )
    reconstructed = preview(
        absolute(catalog_path),
        Path(nonempty(plan.get("repo"), "plan.repo")),
        nonempty(plan.get("scope"), "plan.scope"),
        mapping(plan.get("models"), "plan.models"),
        mapping(plan.get("efforts"), "plan.efforts"),
        user_config=Path(nonempty(plan.get("user_config"), "plan.user_config")),
        defaults=Path(nonempty(plan.get("defaults_path"), "plan.defaults_path")),
        target=Path(nonempty(plan.get("target"), "plan.target")),
    )
    if reconstructed != plan:
        raise ConfigError(
            "plan does not match the current inputs and explicit edits; preview again"
        )
    target = Path(plan["target"])
    desired = plan["proposed_yaml"].encode("utf-8")
    original = file_bytes(target)
    if original == desired:
        if sources != [snapshot(Path(source["path"])) for source in sources]:
            raise ConfigError(
                "configuration inputs changed before writing; preview again"
            )
        return {"status": "unchanged", "target": str(target)}
    target.parent.mkdir(parents=True, exist_ok=True)
    regular_path(target)
    lock = target.with_name(target.name + ".lock")
    try:
        lock_fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as error:
        raise ConfigError(
            f"configuration writer lock exists: {lock}; inspect it before retrying"
        ) from error
    temporary: Path | None = None
    backup: Path | None = None
    try:
        os.close(lock_fd)
        for source in sources:
            if source != snapshot(Path(source["path"])):
                raise ConfigError(
                    "configuration inputs changed before writing; preview again"
                )
        mode = stat.S_IMODE(target.stat().st_mode) if original is not None else 0o600
        fd, name = tempfile.mkstemp(prefix=".preflight-models-", dir=target.parent)
        temporary = Path(name)
        with os.fdopen(fd, "wb") as output:
            os.fchmod(output.fileno(), mode)
            output.write(desired)
            output.flush()
            os.fsync(output.fileno())
        if original is None:
            os.link(temporary, target)
        else:
            backup = target.with_name(target.name + ".bak-" + uuid.uuid4().hex)
            with backup.open("xb") as output:
                os.chmod(backup, mode)
                output.write(original)
                output.flush()
                os.fsync(output.fileno())
            if file_bytes(target) != original:
                raise ConfigError("target changed before replacement; preview again")
            os.replace(temporary, target)
        return {
            "status": "written",
            "target": str(target),
            "backup": str(backup) if backup else None,
        }
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
        lock.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    discover = commands.add_parser("discover")
    discover.add_argument("--runtime", required=True, choices=("codex", "claude-code"))
    discover.add_argument("--output", required=True, type=Path)
    configure = commands.add_parser("preview")
    configure.add_argument("--catalog", required=True, type=Path)
    configure.add_argument("--repo", required=True, type=Path)
    configure.add_argument("--scope", required=True, choices=("project", "user"))
    configure.add_argument("--model", action="append", default=[])
    configure.add_argument("--effort", action="append", default=[])
    configure.add_argument("--plan", required=True, type=Path)
    configure.add_argument("--user-config", type=Path)
    configure.add_argument("--defaults", type=Path)
    configure.add_argument("--target", type=Path)
    write = commands.add_parser("write")
    write.add_argument("--plan", required=True, type=Path)
    write.add_argument("--catalog", required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.command == "discover":
            if args.runtime == "claude-code":
                raise ConfigError(
                    "automatic Claude Code discovery is unavailable; provide a user-confirmed JSON catalog from the target runtime's model picker with explicit effort capabilities"
                )
            result = discover_codex()
            exclusive_json(absolute(args.output), result)
        elif args.command == "preview":
            result = preview(
                args.catalog,
                args.repo,
                args.scope,
                edits(args.model, "--model"),
                edits(args.effort, "--effort"),
                user_config=args.user_config,
                defaults=args.defaults,
                target=args.target,
            )
            if absolute(args.plan) in {
                Path(source["path"]) for source in result["sources"]
            }:
                raise ConfigError(
                    "plan output must be separate from all configuration inputs"
                )
            exclusive_json(absolute(args.plan), result)
        else:
            result = write_plan(args.plan, args.catalog)
    except (ConfigError, OSError, UnicodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
