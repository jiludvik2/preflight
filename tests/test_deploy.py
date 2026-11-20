import importlib.util
from contextlib import redirect_stderr, redirect_stdout
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


DEPLOY = Path(__file__).parents[1] / "deploy.py"


def load_module():
    spec = importlib.util.spec_from_file_location("preflight_deploy", DEPLOY)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class DeployTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.source = self.base / "source"
        for name in ("define-change", "design-solution"):
            skill = self.source / "skills" / name / "references"
            skill.mkdir(parents=True)
            (skill.parent / "SKILL.md").write_text(
                f"---\nname: {name}\n---\n[common](../../shared/common.md)\n"
            )
            (skill / "child.md").write_text("[common](../../../shared/common.md)\n")
        (self.source / "shared").mkdir()
        (self.source / "shared" / "common.md").write_text("original\n")
        (self.source / "config").mkdir()
        (self.source / "config/model-roles.default.yaml").write_text("version: 2\n")
        self.target = self.base / "target" / "skills"
        self.output = io.StringIO()
        self.home = self.base / "home"
        home_patch = patch.object(Path, "home", return_value=self.home)
        home_patch.start()
        self.addCleanup(home_patch.stop)
        environment_patch = patch.object(os, "environ", {})
        environment_patch.start()
        self.addCleanup(environment_patch.stop)

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args):
        copied = self.source / "deploy.py"
        copied.write_text(DEPLOY.read_text())
        return subprocess.run(
            ["python3", str(copied), *args],
            text=True,
            capture_output=True,
            env={"PATH": "/usr/bin:/bin"},
        )

    def install_source(self, *args):
        module = load_module()
        old = module.SOURCE_ROOT
        module.SOURCE_ROOT = self.source
        try:
            with redirect_stdout(self.output), redirect_stderr(self.output):
                return module.main(list(args))
        finally:
            module.SOURCE_ROOT = old

    def test_install_all_stages_shared_and_rewrites_links(self):
        self.assertEqual(
            0, self.install_source("install", "--target", str(self.target), "--all")
        )
        self.assertEqual(
            {"define-change", "design-solution"},
            {path.name for path in self.target.iterdir()},
        )
        package = self.target / "define-change"
        self.assertTrue((package / "references" / "_shared" / "common.md").is_file())
        self.assertIn(
            "references/_shared/common.md", (package / "SKILL.md").read_text()
        )
        self.assertIn(
            "_shared/common.md", (package / "references" / "child.md").read_text()
        )
        receipt = json.loads((package / ".preflight-owner.json").read_text())
        self.assertIn("SKILL.md", receipt["managed_files"])

    def test_existing_single_skill_install_can_add_second_then_update_all(self):
        self.assertEqual(
            0,
            self.install_source(
                "install",
                "--target",
                str(self.target),
                "define-change",
            ),
        )
        before = {
            path.relative_to(self.target): path.read_bytes()
            for path in self.target.rglob("*")
            if path.is_file()
        }
        self.assertEqual(
            2, self.install_source("reinstall", "--target", str(self.target), "--all")
        )
        self.assertEqual(
            before,
            {
                path.relative_to(self.target): path.read_bytes()
                for path in self.target.rglob("*")
                if path.is_file()
            },
        )
        self.assertEqual(
            0,
            self.install_source(
                "install", "--target", str(self.target), "design-solution"
            ),
        )
        self.assertEqual(
            0, self.install_source("reinstall", "--target", str(self.target), "--all")
        )
        self.assertEqual(
            0, self.install_source("uninstall", "--target", str(self.target), "--all")
        )
        self.assertEqual([], list(self.target.iterdir()))

    def test_without_pstack_all_installs_updates_and_uninstalls_every_skill(self):
        self.assertFalse(self.home.exists())
        self.assertEqual(
            0, self.install_source("install", "--target", str(self.target), "--all")
        )
        self.assertEqual(
            {"define-change", "design-solution"},
            {path.name for path in self.target.iterdir()},
        )
        self.assertEqual(
            0, self.install_source("reinstall", "--target", str(self.target), "--all")
        )
        self.assertEqual(
            0, self.install_source("uninstall", "--target", str(self.target), "--all")
        )
        self.assertEqual([], list(self.target.iterdir()))
        self.assertFalse(self.home.exists())

    def test_removed_execution_skill_is_rejected_before_installing_anything(self):
        self.assertEqual(
            2,
            self.install_source(
                "install",
                "--target",
                str(self.target),
                "define-change",
                "preflight-execution",
            ),
        )
        self.assertFalse(self.target.parent.exists())

    def test_without_pstack_reinstall_updates_preparation_and_preserves_config(self):
        self.assertEqual(
            0, self.install_source("install", "--target", str(self.target), "--all")
        )
        package = self.target / "design-solution"
        (package / "preferences.yaml").write_text("keep: true\n")
        for name in ("define-change", "design-solution"):
            (self.source / "skills" / name / "SKILL.md").write_text(
                f"---\nname: {name}\n---\nUpdated.\n"
            )
        for selection in (("--all",), ("design-solution",)):
            self.assertEqual(
                0,
                self.install_source(
                    "reinstall", "--target", str(self.target), *selection
                ),
            )
            for name in ("define-change", "design-solution"):
                self.assertIn("Updated.", (self.target / name / "SKILL.md").read_text())
            self.assertEqual("keep: true\n", (package / "preferences.yaml").read_text())

    def test_preparation_uninstall_and_restore_do_not_require_pstack(self):
        self.assertEqual(
            0, self.install_source("install", "--target", str(self.target), "--all")
        )
        package = self.target / "design-solution"
        original = {
            path.relative_to(package): path.read_bytes()
            for path in package.rglob("*")
            if path.is_file()
        }
        self.assertEqual(
            0,
            self.install_source(
                "uninstall", "--target", str(self.target), "design-solution"
            ),
        )
        self.assertFalse(package.exists())
        self.assertEqual(
            {"define-change"},
            {path.name for path in self.target.iterdir()},
        )
        (backup,) = (self.target.parent / ".preflight-backups").iterdir()
        identifier = backup.name.removeprefix("design-solution-")
        self.assertEqual(
            0,
            self.install_source(
                "restore",
                "--target",
                str(self.target),
                "--backup",
                identifier,
                "design-solution",
            ),
        )
        self.assertEqual(
            original,
            {
                path.relative_to(package): path.read_bytes()
                for path in package.rglob("*")
                if path.is_file()
            },
        )
        self.assertEqual(
            0, self.install_source("uninstall", "--target", str(self.target), "--all")
        )
        self.assertEqual([], list(self.target.iterdir()))

    def test_without_pstack_project_and_user_installs_preserve_other_skills(self):
        project = self.base / "project"
        project.mkdir()
        (project / ".git").write_text("gitdir: worktree-metadata\n")
        unrelated = self.home / ".agents/skills/other/SKILL.md"
        unrelated.parent.mkdir(parents=True)
        unrelated.write_bytes(b"Keep this skill exactly.\n")
        with patch.object(os, "environ", {"CODEX_HOME": str(self.base / "codex")}):
            for destination in (("--repo", str(project)), ("--user",)):
                for operation in ("install", "reinstall"):
                    self.assertEqual(
                        0,
                        self.install_source(operation, *destination, "design-solution"),
                    )
        self.assertTrue((project / ".agents/skills/design-solution/SKILL.md").is_file())
        self.assertEqual(
            (self.source / "skills/design-solution").resolve(),
            (self.home / ".agents/skills/design-solution").resolve(),
        )
        self.assertEqual(b"Keep this skill exactly.\n", unrelated.read_bytes())

    def test_uninstall_all_skips_absent_but_refuses_unowned_packages(self):
        self.assertEqual(
            0, self.install_source("uninstall", "--target", str(self.target), "--all")
        )
        self.assertFalse(self.target.parent.exists())
        self.assertEqual(
            2,
            self.install_source(
                "uninstall", "--target", str(self.target), "design-solution"
            ),
        )
        self.assertEqual(
            0,
            self.install_source(
                "install",
                "--target",
                str(self.target),
                "define-change",
            ),
        )
        unowned = self.target / "design-solution"
        unowned.mkdir()
        (unowned / "keep.txt").write_text("Unowned.\n")
        self.assertEqual(
            2, self.install_source("uninstall", "--target", str(self.target), "--all")
        )
        self.assertTrue((self.target / "define-change").is_dir())
        self.assertEqual("Unowned.\n", (unowned / "keep.txt").read_text())

    def test_reinstall_preserves_unknown_configuration_and_refuses_collision(self):
        self.assertEqual(
            0,
            self.install_source(
                "install", "--target", str(self.target), "define-change"
            ),
        )
        package = self.target / "define-change"
        config = package / "config" / "local.yaml"
        config.parent.mkdir()
        config.write_bytes(b'{"keep": true}\n')
        (self.source / "skills" / "define-change" / "SKILL.md").write_text(
            "---\nname: define-change\n---\nchanged\n"
        )
        self.assertEqual(
            0,
            self.install_source(
                "reinstall", "--target", str(self.target), "define-change"
            ),
        )
        self.assertEqual(b'{"keep": true}\n', config.read_bytes())
        (package / "extra.txt").write_text("local")
        (self.source / "skills" / "define-change" / "extra.txt").write_text("source")
        self.assertEqual(
            2,
            self.install_source(
                "reinstall", "--target", str(self.target), "define-change"
            ),
        )
        self.assertEqual("local", (package / "extra.txt").read_text())

    def test_uninstall_then_explicit_restore(self):
        self.assertEqual(
            0,
            self.install_source(
                "install", "--target", str(self.target), "define-change"
            ),
        )
        package = self.target / "define-change"
        (package / "preferences.yaml").write_bytes(b"retain: true\n")
        original = {
            str(path.relative_to(package)): path.read_bytes()
            for path in package.rglob("*")
            if path.is_file()
        }
        self.assertEqual(
            0,
            self.install_source(
                "uninstall", "--target", str(self.target), "define-change"
            ),
        )
        backups = list((self.target.parent / ".preflight-backups").iterdir())
        identifier = backups[0].name.removeprefix("define-change-")
        self.assertEqual(
            0,
            self.install_source(
                "restore",
                "--target",
                str(self.target),
                "--backup",
                identifier,
                "define-change",
            ),
        )
        self.assertTrue((self.target / "define-change" / "SKILL.md").exists())
        restored = {
            str(path.relative_to(package)): path.read_bytes()
            for path in package.rglob("*")
            if path.is_file()
        }
        self.assertEqual(original, restored)
        self.assertFalse(backups[0].exists())

    def test_restore_uses_backup_when_incoming_source_is_unusable(self):
        for index, damaged in enumerate(
            ("skills/define-change", "shared", "config/model-roles.default.yaml")
        ):
            for current_present in (False, True):
                with self.subTest(damaged=damaged, current_present=current_present):
                    target = self.base / f"restore-{index}-{current_present}" / "skills"
                    self.assertEqual(
                        0,
                        self.install_source(
                            "install", "--target", str(target), "define-change"
                        ),
                    )
                    package = target / "define-change"
                    (package / "preferences.yaml").write_bytes(b"retain: true\n")
                    original = {
                        path.relative_to(package): path.read_bytes()
                        for path in package.rglob("*")
                        if path.is_file()
                    }
                    operation = "reinstall" if current_present else "uninstall"
                    self.assertEqual(
                        0,
                        self.install_source(
                            operation, "--target", str(target), "define-change"
                        ),
                    )
                    backups = target.parent / ".preflight-backups"
                    (backup,) = backups.iterdir()
                    identifier = backup.name.removeprefix("define-change-")
                    if current_present:
                        (package / "SKILL.md").write_bytes(
                            b"displaced current content\n"
                        )
                        current = {
                            path.relative_to(package): path.read_bytes()
                            for path in package.rglob("*")
                            if path.is_file()
                        }
                    source = self.source / damaged
                    saved = self.base / "saved-source"
                    source.rename(saved)
                    if damaged == "shared":
                        source.symlink_to(saved, target_is_directory=True)
                    try:
                        self.assertEqual(
                            0,
                            self.install_source(
                                "restore",
                                "--target",
                                str(target),
                                "--backup",
                                identifier,
                                "define-change",
                            ),
                            self.output.getvalue(),
                        )
                    finally:
                        if source.is_symlink():
                            source.unlink()
                        saved.rename(source)
                    self.assertEqual(
                        original,
                        {
                            path.relative_to(package): path.read_bytes()
                            for path in package.rglob("*")
                            if path.is_file()
                        },
                    )
                    self.assertFalse(backup.exists())
                    if current_present:
                        (displaced,) = backups.iterdir()
                        self.assertEqual(
                            current,
                            {
                                path.relative_to(displaced): path.read_bytes()
                                for path in displaced.rglob("*")
                                if path.is_file()
                            },
                        )
                    else:
                        self.assertEqual([], list(backups.iterdir()))

    def test_restore_refuses_source_target_overlap_without_mutation(self):
        self.assertEqual(
            0,
            self.install_source(
                "install", "--target", str(self.target), "define-change"
            ),
        )
        self.assertEqual(
            0,
            self.install_source(
                "uninstall", "--target", str(self.target), "define-change"
            ),
        )
        backups = self.target.parent / ".preflight-backups"
        (backup,) = backups.iterdir()
        identifier = backup.name.removeprefix("define-change-")
        original = {
            path.relative_to(backups): path.read_bytes()
            for path in backups.rglob("*")
            if path.is_file()
        }
        for source in (self.target.parent, self.target / "nested-source"):
            with self.subTest(source=source), patch.object(self, "source", source):
                self.assertEqual(
                    2,
                    self.install_source(
                        "restore",
                        "--target",
                        str(self.target),
                        "--backup",
                        identifier,
                        "define-change",
                    ),
                )
                self.assertFalse((self.target / "define-change").exists())
                self.assertEqual(
                    original,
                    {
                        path.relative_to(backups): path.read_bytes()
                        for path in backups.rglob("*")
                        if path.is_file()
                    },
                )

    def test_reinstall_fault_restores_old_package(self):
        self.assertEqual(
            0,
            self.install_source(
                "install", "--target", str(self.target), "define-change"
            ),
        )
        module = load_module()
        original_root, original_replace = module.SOURCE_ROOT, module.os.replace
        module.SOURCE_ROOT = self.source

        def fail_stage_replace(source, destination):
            if (
                Path(destination) == self.target / "define-change"
                and ".preflight-stage-" in Path(source).name
            ):
                raise OSError("injected replacement failure")
            return original_replace(source, destination)

        module.os.replace = fail_stage_replace
        try:
            self.assertEqual(
                2,
                module.main(
                    ["reinstall", "--target", str(self.target), "define-change"]
                ),
            )
        finally:
            module.SOURCE_ROOT, module.os.replace = original_root, original_replace
        self.assertTrue((self.target / "define-change" / "SKILL.md").is_file())
        self.assertFalse(
            (self.target.parent / ".preflight-state" / "pending.json").exists()
        )

    def test_restore_fault_rolls_back_displaced_current_bytes(self):
        self.assertEqual(
            0,
            self.install_source(
                "install", "--target", str(self.target), "define-change"
            ),
        )
        current = self.target / "define-change" / "SKILL.md"
        (self.source / "skills" / "define-change" / "SKILL.md").write_text(
            "---\nname: define-change\n---\nnew\n"
        )
        self.assertEqual(
            0,
            self.install_source(
                "reinstall", "--target", str(self.target), "define-change"
            ),
        )
        expected = current.read_bytes()
        backup = next((self.target.parent / ".preflight-backups").iterdir())
        identifier = backup.name.removeprefix("define-change-")
        module = load_module()
        original_root, original_replace = module.SOURCE_ROOT, module.os.replace
        module.SOURCE_ROOT = self.source

        def fail_promotion(source, destination):
            if (
                Path(destination) == self.target / "define-change"
                and Path(source) == backup
            ):
                raise OSError("injected restore failure")
            return original_replace(source, destination)

        module.os.replace = fail_promotion
        try:
            self.assertEqual(
                2,
                module.main(
                    [
                        "restore",
                        "--target",
                        str(self.target),
                        "--backup",
                        identifier,
                        "define-change",
                    ]
                ),
            )
        finally:
            module.SOURCE_ROOT, module.os.replace = original_root, original_replace
        self.assertEqual(expected, current.read_bytes())
        self.assertTrue(backup.exists())
        self.assertFalse(
            (self.target.parent / ".preflight-state" / "pending.json").exists()
        )
        self.assertEqual(
            0,
            self.install_source(
                "restore",
                "--target",
                str(self.target),
                "--backup",
                identifier,
                "define-change",
            ),
        )
        self.assertFalse(backup.exists())
        self.assertGreaterEqual(
            len(list((self.target.parent / ".preflight-backups").iterdir())), 1
        )

    def test_rejects_parent_links_malformed_receipts_and_ancestor_collisions(self):
        actual = self.base / "actual"
        actual.mkdir()
        linked = self.base / "linked"
        linked.symlink_to(actual, target_is_directory=True)
        self.assertEqual(
            2,
            self.install_source(
                "install", "--target", str(linked / "skills"), "define-change"
            ),
        )
        self.assertEqual(
            0,
            self.install_source(
                "install", "--target", str(self.target), "define-change"
            ),
        )
        package = self.target / "define-change"
        receipt = package / ".preflight-owner.json"
        payload = json.loads(receipt.read_text())
        original_payload = dict(payload)
        payload["managed_files"] = [{}]
        receipt.write_text(json.dumps(payload))
        self.assertEqual(
            2,
            self.install_source(
                "reinstall", "--target", str(self.target), "define-change"
            ),
        )
        receipt.write_text(json.dumps(original_payload))
        (package / "new").mkdir()
        (package / "new" / "keep").write_bytes(b"KEEP")
        (self.source / "skills" / "define-change" / "new").write_text("managed")
        self.assertEqual(
            2,
            self.install_source(
                "reinstall", "--target", str(self.target), "define-change"
            ),
        )
        self.assertEqual(b"KEEP", (package / "new" / "keep").read_bytes())

    def test_refuses_symlink_overlap_and_pending_without_mutation(self):
        outside = self.base / "outside"
        outside.mkdir()
        self.target.parent.mkdir(parents=True)
        (self.target.parent / "skills").symlink_to(outside, target_is_directory=True)
        self.assertEqual(
            2,
            self.install_source(
                "install", "--target", str(self.target), "define-change"
            ),
        )
        self.target.unlink()
        self.assertEqual(
            0,
            self.install_source(
                "install", "--target", str(self.target), "define-change"
            ),
        )
        state = self.target.parent / ".preflight-state"
        state.mkdir()
        (state / "pending.json").write_text("{}")
        self.assertEqual(
            2,
            self.install_source(
                "reinstall", "--target", str(self.target), "define-change"
            ),
        )
        self.assertTrue((self.target / "define-change").exists())
        self.assertEqual(
            2,
            self.install_source(
                "install", "--target", str(self.source / "skills"), "design-solution"
            ),
        )

    def test_pending_recovery_guidance_accepts_only_bounded_owned_paths(self):
        self.assertEqual(
            0,
            self.install_source(
                "install", "--target", str(self.target), "define-change"
            ),
        )
        package = self.target / "define-change"
        backups = self.target.parent / ".preflight-backups"
        backups.mkdir()
        backup = backups / ("define-change-" + "0" * 32)
        package.rename(backup)
        state = self.target.parent / ".preflight-state"
        state.mkdir()
        (state / "pending.json").write_text(
            json.dumps(
                {
                    "op": "reinstall",
                    "skill": "define-change",
                    "old": str(package.absolute()),
                    "new": str(backup.absolute()),
                    "backup": str(backup.absolute()),
                }
            )
        )
        self.assertEqual(
            2,
            self.install_source(
                "reinstall", "--target", str(self.target), "define-change"
            ),
        )
        self.assertTrue(backup.exists())
        (state / "pending.json").write_text(
            json.dumps(
                {
                    "op": "reinstall",
                    "skill": "define-change",
                    "old": "/tmp/not-ours",
                    "new": str(backup.absolute()),
                    "backup": str(backup.absolute()),
                }
            )
        )
        self.assertEqual(
            2,
            self.install_source(
                "reinstall", "--target", str(self.target), "define-change"
            ),
        )

    def test_real_cli_rejects_unknown_and_duplicate_selection(self):
        result = self.run_cli("install", "--target", str(self.target), "nope")
        self.assertNotEqual(0, result.returncode)
        result = self.run_cli(
            "install", "--target", str(self.target), "design-solution"
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("installed design-solution", result.stdout)
        module = load_module()
        old = module.SOURCE_ROOT
        module.SOURCE_ROOT = self.source
        try:
            self.assertEqual(
                2,
                module.main(
                    [
                        "install",
                        "--target",
                        str(self.target),
                        "define-change",
                        "define-change",
                    ]
                ),
            )
        finally:
            module.SOURCE_ROOT = old

    def test_unknown_file_survives_incoming_directory_refusal(self):
        self.assertEqual(
            0,
            self.install_source(
                "install", "--target", str(self.target), "define-change"
            ),
        )
        local = self.target / "define-change" / "local"
        local.write_bytes(b"KEEP")
        incoming = self.source / "skills" / "define-change" / "local"
        incoming.mkdir()
        (incoming / "content.md").write_text("new")
        self.assertEqual(
            2,
            self.install_source(
                "reinstall", "--target", str(self.target), "define-change"
            ),
        )
        self.assertEqual(b"KEEP", local.read_bytes())

    def test_malformed_receipts_are_refused_without_changing_package(self):
        self.assertEqual(
            0,
            self.install_source(
                "install", "--target", str(self.target), "define-change"
            ),
        )
        package = self.target / "define-change"
        receipt = package / ".preflight-owner.json"
        original = json.loads(receipt.read_text())
        for invalid in (
            [{}],
            [[]],
            ["../escape"],
            ["references"],
            ["./SKILL.md"],
            ["SKILL.md", "SKILL.md"],
        ):
            with self.subTest(managed=invalid):
                receipt.write_text(json.dumps({**original, "managed_files": invalid}))
                self.assertEqual(
                    2,
                    self.install_source(
                        "reinstall", "--target", str(self.target), "define-change"
                    ),
                )
                self.assertTrue((package / "SKILL.md").is_file())
        receipt.write_bytes(b"\xff")
        self.assertEqual(
            2,
            self.install_source(
                "uninstall", "--target", str(self.target), "define-change"
            ),
        )
        self.assertTrue(package.is_dir())

    def test_existing_lock_refuses_changes_and_is_not_removed(self):
        self.assertEqual(
            0,
            self.install_source(
                "install", "--target", str(self.target), "define-change"
            ),
        )
        lock = self.target.parent / ".preflight.lock"
        lock.write_text("external owner")
        self.assertEqual(
            2,
            self.install_source(
                "uninstall", "--target", str(self.target), "define-change"
            ),
        )
        self.assertEqual("external owner", lock.read_text())
        self.assertTrue((self.target / "define-change").is_dir())

    def test_restore_requires_one_skill_and_valid_backup_id(self):
        for selection in (("--all",), ("define-change", "design-solution")):
            result = self.run_cli(
                "restore",
                "--target",
                str(self.target),
                "--backup",
                "0" * 32,
                *selection,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn("exactly one", result.stderr)
        for identifier in ("../escape", "bad", " " * 32):
            result = self.run_cli(
                "restore",
                "--target",
                str(self.target),
                "--backup",
                identifier,
                "define-change",
            )
            self.assertEqual(2, result.returncode)
            self.assertNotIn("Traceback", result.stderr)

    def test_all_prechecks_do_not_partly_install_on_selection_error(self):
        existing = self.target / "design-solution"
        existing.mkdir(parents=True)
        (existing / "unowned.txt").write_text("not ours")
        self.assertEqual(
            2, self.install_source("install", "--target", str(self.target), "--all")
        )
        self.assertFalse((self.target / "define-change").exists())
        self.assertEqual("not ours", (existing / "unowned.txt").read_text())

    def test_partial_pending_write_leaves_current_package_recoverable(self):
        self.assertEqual(
            0,
            self.install_source(
                "install", "--target", str(self.target), "define-change"
            ),
        )
        package = self.target / "define-change"
        original = {
            str(path.relative_to(package)): path.read_bytes()
            for path in package.rglob("*")
            if path.is_file()
        }
        module = load_module()

        def interrupted_write(record, stream):
            stream.write('{"op":')
            raise OSError("interrupted pending write")

        with (
            patch.object(module, "SOURCE_ROOT", self.source),
            patch.object(module.json, "dump", interrupted_write),
        ):
            with redirect_stdout(self.output), redirect_stderr(self.output):
                self.assertEqual(
                    2,
                    module.main(
                        ["reinstall", "--target", str(self.target), "define-change"]
                    ),
                )
        actual = {
            str(path.relative_to(package)): path.read_bytes()
            for path in package.rglob("*")
            if path.is_file()
        }
        self.assertEqual(original, actual)
        self.assertFalse(
            (self.target.parent / ".preflight-state/pending.json").exists()
        )
        self.assertEqual([], list((self.target.parent / ".preflight-state").iterdir()))
        self.assertFalse((self.target.parent / ".preflight.lock").exists())
        self.assertEqual(
            0,
            self.install_source(
                "reinstall", "--target", str(self.target), "define-change"
            ),
        )


if __name__ == "__main__":
    unittest.main()
