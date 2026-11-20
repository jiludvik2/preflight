#!/usr/bin/env python3
"""Install Preflight skills without touching user config."""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
import shutil
import sys
import tempfile
from typing import NoReturn
import uuid


SOURCE_ROOT = Path(__file__).resolve().parent
SKILL_NAMES = ("define-change", "design-solution")
RECEIPT = ".preflight-owner.json"
FORMAT = 1


class DeploymentError(Exception):
    pass


@dataclass(frozen=True)
class SkillSpec:
    name: str
    source: Path


@dataclass(frozen=True)
class Target:
    root: Path
    state: Path
    backups: Path


@dataclass(frozen=True)
class Receipt:
    managed_files: tuple[str, ...]


def fail(message: str) -> NoReturn:
    raise DeploymentError(message)


def is_relative_name(value: str) -> bool:
    path = Path(value)
    return (
        bool(value)
        and not path.is_absolute()
        and ".." not in path.parts
        and "." not in path.parts
    )


def check_no_symlink_ancestors(path: Path, *, label: str) -> None:
    absolute = path.absolute()
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        if current.exists() or current.is_symlink():
            if current.is_symlink():
                # macOS exposes these two system aliases. They are not caller
                # controlled links and are needed for standard temporary paths.
                if current in {Path("/tmp"), Path("/var")} and current.resolve() in {
                    Path("/private/tmp"),
                    Path("/private/var"),
                }:
                    continue
                fail(f"{label} has a symlink ancestor: {current}")


def check_tree(path: Path, *, label: str) -> None:
    if path.is_symlink():
        fail(f"{label} must not be a symlink: {path}")
    if not path.is_dir():
        fail(f"{label} must be a directory: {path}")
    for parent, dirs, files in os.walk(path, followlinks=False):
        base = Path(parent)
        for name in [*dirs, *files]:
            entry = base / name
            if entry.is_symlink():
                fail(f"{label} contains a symlink: {entry}")


def contained(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def source_specs() -> tuple[SkillSpec, ...]:
    return tuple(SkillSpec(name, SOURCE_ROOT / "skills" / name) for name in SKILL_NAMES)


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "operation", choices=("install", "reinstall", "uninstall", "restore")
    )
    destination = parser.add_mutually_exclusive_group(required=True)
    destination.add_argument("--user", action="store_true")
    destination.add_argument("--repo", type=Path)
    destination.add_argument("--target", type=Path)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("skills", nargs="*")
    parser.add_argument("--backup", help="backup ID required by restore")
    args = parser.parse_intermixed_args(argv)
    if args.all and args.skills:
        parser.error("--all cannot be combined with named skills")
    if not args.all and not args.skills:
        parser.error("choose --all or at least one skill")
    if args.operation == "restore" and not args.backup:
        parser.error("restore requires --backup ID")
    if args.operation == "restore" and (args.all or len(args.skills) != 1):
        parser.error(
            "restore accepts exactly one named skill because backup IDs are package-specific"
        )
    if args.operation != "restore" and args.backup:
        parser.error("--backup is only valid with restore")
    return args


def resolve_target(args: argparse.Namespace) -> Target:
    if args.target:
        root = args.target.absolute()
    elif args.user:
        root = Path.home() / ".agents" / "skills"
    else:
        repo = args.repo.absolute()
        if not (repo / ".git").exists():
            fail(f"--repo must name a git worktree root: {repo}")
        root = repo / ".agents" / "skills"
    check_no_symlink_ancestors(root, label="target")
    if root.exists() and not root.is_dir():
        fail(f"target is not a directory: {root}")
    if root.is_symlink():
        fail(f"target must not be a symlink: {root}")
    return Target(
        root, root.parent / ".preflight-state", root.parent / ".preflight-backups"
    )


def select(args: argparse.Namespace) -> tuple[SkillSpec, ...]:
    selected = SKILL_NAMES if args.all else tuple(args.skills)
    if len(set(selected)) != len(selected):
        fail("duplicate skill selection")
    unknown = sorted(set(selected) - set(SKILL_NAMES))
    if unknown:
        fail(f"unknown skill: {', '.join(unknown)}")
    by_name = {spec.name: spec for spec in source_specs()}
    return tuple(by_name[name] for name in selected)


def applicable_specs(
    args: argparse.Namespace, target: Target, specs: tuple[SkillSpec, ...]
) -> tuple[tuple[SkillSpec, ...], list[str]]:
    if args.operation == "uninstall" and args.all:
        present = tuple(
            spec
            for spec in specs
            if (target.root / spec.name).exists()
            or (target.root / spec.name).is_symlink()
        )
        return present, [
            f"skipped {spec.name}: not installed at {target.root / spec.name}"
            for spec in specs
            if spec not in present
        ]
    return specs, []


def read_receipt(package: Path, skill: str) -> Receipt:
    check_tree(package, label=f"package {skill}")
    receipt = package / RECEIPT
    if receipt.is_symlink() or not receipt.is_file():
        fail(f"target for {skill} is unowned or has a malformed receipt")
    try:
        data: object = json.loads(receipt.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"target for {skill} has a malformed receipt: {exc}")
    if (
        not isinstance(data, dict)
        or data.get("format") != FORMAT
        or data.get("skill") != skill
    ):
        fail(f"target for {skill} is unowned or has a malformed receipt")
    package_id, managed = data.get("package_id"), data.get("managed_files")
    if (
        not isinstance(package_id, str)
        or not package_id
        or not isinstance(managed, list)
    ):
        fail(f"target for {skill} has a malformed receipt")
    managed_names: list[str] = []
    for item in managed:
        if (
            not isinstance(item, str)
            or not is_relative_name(item)
            or Path(item).as_posix() != item
        ):
            fail(f"target for {skill} has a malformed receipt")
        managed_names.append(item)
    if len(managed_names) != len(set(managed_names)) or RECEIPT in managed_names:
        fail(f"target for {skill} has a malformed receipt")
    for name in managed_names:
        entry = package / name
        if not entry.is_file() or entry.is_symlink():
            fail(f"target for {skill} has a malformed receipt")
    return Receipt(tuple(managed_names))


def source_is_valid(spec: SkillSpec) -> None:
    check_no_symlink_ancestors(spec.source, label=f"source {spec.name}")
    check_tree(spec.source, label=f"source {spec.name}")
    shared = SOURCE_ROOT / "shared"
    check_tree(shared, label="source shared guidance")
    config = SOURCE_ROOT / "config" / "model-roles.default.yaml"
    check_no_symlink_ancestors(config, label="default model configuration")
    if not config.is_file():
        fail(f"default model configuration is missing: {config}")
    skill_file = spec.source / "SKILL.md"
    if not skill_file.is_file():
        fail(f"source {spec.name} has no SKILL.md")
    try:
        frontmatter = skill_file.read_text(encoding="utf-8").split("---", 2)[1]
    except (UnicodeDecodeError, IndexError):
        fail(f"source {spec.name} has malformed frontmatter")
    if f"name: {spec.name}" not in frontmatter:
        fail(f"source {spec.name} has the wrong frontmatter name")


def source_managed_paths(spec: SkillSpec) -> set[str]:
    paths = {
        entry.relative_to(spec.source).as_posix()
        for entry in spec.source.rglob("*")
        if entry.is_file()
        and "__pycache__" not in entry.parts
        and entry.suffix != ".pyc"
    }
    paths.update(
        (
            Path("references") / "_shared" / entry.relative_to(SOURCE_ROOT / "shared")
        ).as_posix()
        for entry in (SOURCE_ROOT / "shared").rglob("*")
        if entry.is_file()
        and "__pycache__" not in entry.parts
        and entry.suffix != ".pyc"
    )
    paths.add("references/_shared/model-roles.default.yaml")
    return paths


def backup_path(target: Target, skill: str, backup_id: str) -> Path:
    if len(backup_id) != 32 or any(
        character not in "0123456789abcdef" for character in backup_id
    ):
        fail("invalid backup ID")
    return target.backups / f"{skill}-{backup_id}"


def owned_directory(path: Path, skill: str) -> bool:
    try:
        read_receipt(path, skill)
        return True
    except DeploymentError:
        return False


def pending_guidance(target: Target, pending: Path) -> None:
    if pending.is_symlink():
        fail(f"pending recovery record must not be a symlink: {pending}")
    try:
        record = json.loads(pending.read_text(encoding="utf-8"))
        if not isinstance(record, dict) or set(record) != {
            "op",
            "skill",
            "old",
            "new",
            "backup",
        }:
            raise ValueError
        operation, skill = record["op"], record["skill"]
        old, new, selected = record["old"], record["new"], record["backup"]
        if (
            operation not in {"reinstall", "uninstall", "restore"}
            or skill not in SKILL_NAMES
        ):
            raise ValueError
        if not all(
            isinstance(value, str) and "\x00" not in value
            for value in (old, new, selected)
        ):
            raise ValueError
        package = target.root / skill
        if Path(old) != package.absolute():
            raise ValueError
        new_path = Path(new)
        selected_path = Path(selected)
        for path in (new_path, selected_path):
            if path.parent != target.backups.absolute() or not path.name.startswith(
                skill + "-"
            ):
                raise ValueError
            backup_path(target, skill, path.name.removeprefix(skill + "-"))
    except (
        OSError,
        UnicodeDecodeError,
        json.JSONDecodeError,
        KeyError,
        TypeError,
        ValueError,
    ):
        fail(
            f"malformed pending recovery record at {pending}; inspect live packages under {target.root} "
            f"and owned backups under {target.backups}. Reconcile their receipts and contents before "
            "moving anything or removing this record; automatic recovery is unavailable"
        )
    package_ok = owned_directory(package, skill) if package.exists() else False
    new_ok = owned_directory(new_path, skill) if new_path.exists() else False
    selected_ok = (
        owned_directory(selected_path, skill) if selected_path.exists() else False
    )
    if operation in {"reinstall", "uninstall"}:
        if package_ok and new_ok:
            fail(
                f"completed {operation} is awaiting cleanup at {pending}; both owned trees are present. Remove only {pending}"
            )
        if not package.exists() and new_ok:
            fail(
                f"interrupted {operation} at {pending}; rename owned backup {new_path} to {package}, then remove {pending}"
            )
        if package_ok and not new_path.exists():
            fail(
                f"{operation} did not rename its package; remove only {pending}, then retry"
            )
    else:
        if package_ok and new_ok:
            fail(
                f"completed restore is awaiting cleanup at {pending}; package and displaced backup are owned. Remove only {pending}"
            )
        if package_ok and new_path == selected_path and not new_path.exists():
            fail(
                f"completed restore is awaiting cleanup at {pending}; remove only {pending}"
            )
        if not package.exists() and selected_ok:
            fail(
                f"interrupted restore at {pending}; rename selected owned backup {selected_path} to {package}, then remove {pending}"
            )
        if package_ok and not new_path.exists() and selected_ok:
            fail(
                f"restore did not displace its current package; remove only {pending}, then retry"
            )
    fail(
        f"pending recovery state at {pending} has unexpected owned-path state; do not retry or delete it"
    )


def preflight(
    operation: str, target: Target, specs: tuple[SkillSpec, ...], backup_id: str | None
) -> None:
    for area, label in ((target.state, "state"), (target.backups, "backup directory")):
        check_no_symlink_ancestors(area, label=label)
        if area.exists() and (area.is_symlink() or not area.is_dir()):
            fail(f"{label} is not a real directory: {area}")
    pending = target.state / "pending.json"
    if pending.exists() or pending.is_symlink():
        pending_guidance(target, pending)
    if operation != "uninstall":
        source_root = SOURCE_ROOT.resolve(strict=False)
        target_root = target.root.resolve(strict=False)
        if contained(target_root, source_root) or contained(source_root, target_root):
            fail("source and target overlap")
    for spec in specs:
        if operation in {"install", "reinstall"}:
            source_is_valid(spec)
        package = target.root / spec.name
        if package.exists() or package.is_symlink():
            if package.is_symlink():
                fail(f"target package is a symlink: {package}")
            if operation == "install":
                fail(f"target already exists for {spec.name}")
            receipt = read_receipt(package, spec.name)
            if operation == "reinstall":
                managed = set(receipt.managed_files)
                incoming = source_managed_paths(spec)
                for entry in package.rglob("*"):
                    relative = entry.relative_to(package).as_posix()
                    if relative in managed or relative == RECEIPT:
                        continue
                    if entry.is_dir() and any(
                        name.startswith(relative + "/") for name in managed
                    ):
                        continue
                    if any(
                        relative == path
                        or relative.startswith(path + "/")
                        or path.startswith(relative + "/")
                        for path in incoming
                    ):
                        fail(
                            f"reinstall of {spec.name} would overwrite unowned path: {relative}"
                        )
        elif operation in {"reinstall", "uninstall"}:
            fail(f"target for {spec.name} is absent or unowned")
        if operation == "restore":
            backup = backup_path(target, spec.name, backup_id or "")
            if not backup.exists() or backup.is_symlink():
                fail(f"backup not found for {spec.name}: {backup_id}")
            read_receipt(backup, spec.name)


def copy_tree(source: Path, destination: Path) -> None:
    shutil.copytree(
        source,
        destination,
        symlinks=False,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )


def rewrite_links(path: Path) -> None:
    if path.suffix != ".md":
        return
    text = path.read_text(encoding="utf-8")
    text = text.replace("](../../shared/", "](references/_shared/")
    text = text.replace("](../../../shared/", "](_shared/")
    text = text.replace(
        "](../config/model-roles.default.yaml)", "](model-roles.default.yaml)"
    )
    path.write_text(text, encoding="utf-8")


def managed_names(package: Path) -> list[str]:
    names = []
    for entry in package.rglob("*"):
        if entry.is_file() and entry.name != RECEIPT:
            names.append(entry.relative_to(package).as_posix())
    return sorted(names)


def build_package(spec: SkillSpec, target: Target, package_id: str) -> Path:
    target.root.parent.mkdir(parents=True, exist_ok=True)
    target.root.mkdir(exist_ok=True)
    stage = Path(
        tempfile.mkdtemp(
            prefix=f".preflight-stage-{spec.name}-", dir=target.root.parent
        )
    )
    try:
        copy_tree(spec.source, stage)
        shared_destination = stage / "references" / "_shared"
        shared_destination.parent.mkdir(parents=True, exist_ok=True)
        copy_tree(SOURCE_ROOT / "shared", shared_destination)
        shutil.copy2(
            SOURCE_ROOT / "config" / "model-roles.default.yaml", shared_destination
        )
        for entry in stage.rglob("*.md"):
            rewrite_links(entry)
        receipt = {
            "format": FORMAT,
            "skill": spec.name,
            "package_id": package_id,
            "managed_files": managed_names(stage),
        }
        (stage / RECEIPT).write_text(
            json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8"
        )
        return stage
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise


def preserve_unknown(old: Path, staged: Path, receipt: Receipt) -> None:
    managed = set(receipt.managed_files)
    for entry in old.rglob("*"):
        relative = entry.relative_to(old).as_posix()
        if relative in managed or relative == RECEIPT:
            continue
        destination = staged / relative
        if destination.exists():
            continue
        if entry.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
        elif entry.is_file():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(entry, destination)


def write_pending(
    target: Target,
    operation: str,
    skill: str,
    old: Path,
    new: Path,
    backup: Path | None = None,
) -> None:
    target.state.mkdir(parents=True, exist_ok=True)
    selected = backup or new
    record = {
        "op": operation,
        "skill": skill,
        "old": str(old.absolute()),
        "new": str(new.absolute()),
        "backup": str(selected.absolute()),
    }
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=target.state,
            prefix=".pending-",
            delete=False,
        ) as stream:
            temporary = Path(stream.name)
            json.dump(record, stream)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, target.state / "pending.json")
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def clear_pending(target: Target) -> None:
    (target.state / "pending.json").unlink(missing_ok=True)


def backup_id() -> str:
    return uuid.uuid4().hex


def replace_owned(target: Target, spec: SkillSpec, operation: str) -> str:
    package = target.root / spec.name
    staged = build_package(spec, target, uuid.uuid4().hex)
    try:
        if operation == "install":
            os.replace(staged, package)
            return "installed"
        receipt = read_receipt(package, spec.name)
        preserve_unknown(package, staged, receipt)
        identifier = backup_id()
        backup = backup_path(target, spec.name, identifier)
        target.backups.mkdir(parents=True, exist_ok=True)
        write_pending(target, operation, spec.name, package, backup)
        os.replace(package, backup)
        try:
            os.replace(staged, package)
        except OSError as exc:
            if not package.exists() and backup.exists():
                os.replace(backup, package)
                clear_pending(target)
            raise DeploymentError(f"replacement failed for {spec.name}: {exc}") from exc
        clear_pending(target)
        return f"reinstalled (backup {identifier})"
    finally:
        if staged.exists():
            shutil.rmtree(staged, ignore_errors=True)


def uninstall_owned(target: Target, spec: SkillSpec) -> str:
    package = target.root / spec.name
    read_receipt(package, spec.name)
    identifier = backup_id()
    backup = backup_path(target, spec.name, identifier)
    target.backups.mkdir(parents=True, exist_ok=True)
    write_pending(target, "uninstall", spec.name, package, backup)
    os.replace(package, backup)
    clear_pending(target)
    return f"uninstalled (backup {identifier})"


def restore_owned(target: Target, spec: SkillSpec, identifier: str) -> str:
    package = target.root / spec.name
    backup = backup_path(target, spec.name, identifier)
    read_receipt(backup, spec.name)
    displaced: Path | None = None
    if package.exists():
        read_receipt(package, spec.name)
        displaced = backup_path(target, spec.name, backup_id())
        write_pending(target, "restore", spec.name, package, displaced, backup)
        os.replace(package, displaced)
    else:
        write_pending(target, "restore", spec.name, package, backup, backup)
    try:
        os.replace(backup, package)
    except OSError as exc:
        if displaced is not None and not package.exists() and displaced.exists():
            try:
                os.replace(displaced, package)
                clear_pending(target)
            except OSError:
                pass
        raise DeploymentError(f"restore failed for {spec.name}: {exc}") from exc
    clear_pending(target)
    if displaced is not None:
        return f"restored (backup {identifier}; displaced backup {displaced.name.removeprefix(spec.name + '-')})"
    return f"restored (backup {identifier})"


def main(argv: list[str] | None = None) -> int:
    lock: Path | None = None
    lock_fd: int | None = None
    try:
        args = parse_args(argv)
        target = resolve_target(args)
        specs = select(args)
        specs, notices = applicable_specs(args, target, specs)
        user_roots = {
            Path.home() / ".agents/skills",
            Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex") / "skills",
        }
        if args.user or target.root in user_roots:
            if args.operation == "restore":
                fail(
                    "user installs are source links; inspect preserved copies outside the skill root instead of restoring a physical install"
                )
            # Isolated targets retain frozen packages for evaluation and recovery.
            sys.path.insert(0, str(Path(__file__).resolve().parent))
            from skill_install import install_links

            for notice in notices:
                print(notice)
            for result in install_links(
                args.operation, target.root, {spec.name: spec.source for spec in specs}
            ):
                print(result)
            return 0
        preflight(args.operation, target, specs, args.backup)
        for notice in notices:
            print(notice)
        if not specs:
            return 0
        target.root.parent.mkdir(parents=True, exist_ok=True)
        lock = target.root.parent / ".preflight.lock"
        try:
            lock_fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            fail(
                f"installer lock exists at {lock}; inspect the owning process before retrying"
            )
        preflight(args.operation, target, specs, args.backup)
        for spec in specs:
            if args.operation in {"install", "reinstall"}:
                result = replace_owned(target, spec, args.operation)
            elif args.operation == "uninstall":
                result = uninstall_owned(target, spec)
            else:
                result = restore_owned(target, spec, args.backup)
            print(f"{result} {spec.name} -> {target.root / spec.name}")
        return 0
    except (DeploymentError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    finally:
        if lock_fd is not None:
            os.close(lock_fd)
            assert lock is not None
            lock.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
