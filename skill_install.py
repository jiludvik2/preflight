#!/usr/bin/env python3
"""Install selected custom skills as links to this checkout."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import sys
import uuid

REPO = Path(__file__).resolve().parent


def catalog() -> dict[str, Path]:
    return {p.parent.name: p.parent for p in REPO.glob("skills/*/SKILL.md")}


def real_directory_path(path: Path) -> None:
    for entry in (path, *path.parents):
        if entry.is_symlink() and not (
            entry == Path("/tmp")
            and entry.resolve() == Path("/private/tmp")
            or entry == Path("/var")
            and entry.resolve() == Path("/private/var")
        ):
            raise ValueError(f"directory path contains a symlink: {entry}")
        if entry.exists() and not entry.is_dir():
            raise ValueError(f"not a directory: {entry}")


def skill_name(source: Path) -> str:
    text = (source / "SKILL.md").read_text()
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
    name = (
        re.search(r"(?m)^name:\s*['\"]?([\w-]+)['\"]?\s*$", match[1]) if match else None
    )
    if not name:
        raise ValueError(f"missing skill name: {source}")
    return name[1]


def install_links(operation: str, root: Path, skills: dict[str, Path]) -> list[str]:
    """Precheck the selection; preserve replaced directories outside skill discovery."""
    root = root.expanduser().absolute()
    real_directory_path(root)
    root = root.resolve()
    backups = root.parent / ".preflight-link-backups"
    real_directory_path(backups)
    sources = {name: source.resolve(strict=True) for name, source in skills.items()}
    for name, source in sources.items():
        if name != source.name or skill_name(source) != name:
            raise ValueError(f"skill identity does not match: {name}: {source}")
        if source.is_relative_to(root) or root.is_relative_to(source):
            raise ValueError(f"source and destination overlap: {source}, {root}")
    root.parent.mkdir(parents=True, exist_ok=True)
    lock = root.parent / ".preflight-link-install.lock"
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        for name, source in sources.items():
            dst = root / name
            if dst.is_symlink():
                if dst.resolve() != source:
                    raise ValueError(f"refusing unrelated symlink: {dst}")
            elif dst.exists():
                if not dst.is_dir() or skill_name(dst) != name:
                    raise ValueError(f"refusing unrelated destination: {dst}")
                if operation == "install":
                    raise ValueError(
                        f"physical copy exists: {dst}; use reinstall to back it up and link"
                    )
            elif operation == "reinstall":
                raise ValueError(f"skill is not installed: {dst}")
        root.mkdir(exist_ok=True)
        results = []
        for name, source in sources.items():
            dst = root / name
            if dst.is_symlink():
                if operation == "uninstall":
                    dst.unlink()
                    results.append(f"unlinked {name}")
                elif dst.resolve() == source:
                    results.append(f"already linked {name} -> {source}")
                else:
                    staged = root / f".{name}-{uuid.uuid4().hex}"
                    try:
                        staged.symlink_to(source, target_is_directory=True)
                        staged.replace(dst)
                    finally:
                        staged.unlink(missing_ok=True)
                    results.append(f"relinked {name} -> {source}")
                continue
            if operation == "uninstall" and not dst.exists():
                results.append(f"already absent {name}")
                continue
            staged = root / f".{name}-{uuid.uuid4().hex}"
            backup = None
            try:
                if operation != "uninstall":
                    staged.symlink_to(source, target_is_directory=True)
                if dst.exists():
                    backups.mkdir(mode=0o700, exist_ok=True)
                    backup = backups / f"{name}-{uuid.uuid4().hex}"
                    dst.rename(backup)
                if operation != "uninstall":
                    staged.rename(dst)
            except OSError:
                if backup is not None and not dst.exists() and not dst.is_symlink():
                    backup.rename(dst)
                raise
            finally:
                staged.unlink(missing_ok=True)
            result = f"{'uninstalled' if operation == 'uninstall' else 'linked'} {name} -> {source}"
            if backup:
                result += f" (previous copy: {backup})"
            results.append(result)
        return results
    finally:
        os.close(fd)
        lock.unlink()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "operation", choices=("list", "install", "reinstall", "uninstall")
    )
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--user", action="store_true", help="use ~/.agents/skills")
    target.add_argument("--target", type=Path, help="explicit skill directory")
    parser.add_argument(
        "--installed", action="store_true", help="select only existing custom entries"
    )
    parser.add_argument("skills", nargs="*")
    args = parser.parse_intermixed_args(argv)
    available = catalog()
    root = args.target or Path.home() / ".agents/skills"
    if args.installed and args.skills:
        parser.error("choose names or --installed")
    if set(args.skills) - available.keys() or len(set(args.skills)) != len(args.skills):
        parser.error("unknown or duplicate skill name")
    names = args.skills or (
        sorted(available) if args.operation == "list" or args.installed else []
    )
    if not names and args.operation != "list" and not args.installed:
        parser.error("choose names or --installed; no skills are installed implicitly")
    if args.installed:
        names = [n for n in names if (root / n).exists() or (root / n).is_symlink()]
    try:
        if args.operation == "list":
            for name in names:
                dst = root / name
                state = (
                    "linked"
                    if dst.is_symlink() and dst.resolve() == available[name].resolve()
                    else (
                        "other link"
                        if dst.is_symlink()
                        else "copy"
                        if dst.exists()
                        else "absent"
                    )
                )
                print(f"{name}: {state} -> {available[name]}")
        else:
            for result in install_links(
                args.operation, root, {n: available[n] for n in names}
            ):
                print(result)
        return 0
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
