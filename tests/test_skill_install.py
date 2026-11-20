from pathlib import Path
import importlib.util
import sys
import tempfile
import unittest
from unittest.mock import patch

import skill_install as installer


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.source = self.base / "repo" / "example"
        self.source.mkdir(parents=True)
        (self.source / "SKILL.md").write_text(
            "---\nname: example\n---\nFirst version\n"
        )
        self.root = self.base / "profile" / "skills"
        self.skills = {"example": self.source}

    def run_install(self, operation="install", skills=None):
        return installer.install_links(operation, self.root, skills or self.skills)

    def test_link_reads_live_source_and_uninstall_leaves_source(self):
        self.run_install()
        dst = self.root / "example"
        self.assertTrue(dst.is_symlink())
        (self.source / "SKILL.md").write_text("---\nname: example\n---\nChanged\n")
        self.assertIn("Changed", (dst / "SKILL.md").read_text())
        self.run_install()
        self.run_install("uninstall")
        self.assertFalse(dst.is_symlink())
        self.assertTrue((self.source / "SKILL.md").is_file())

    def test_migration_preserves_every_local_file_in_backup(self):
        dst = self.root / "example"
        dst.mkdir(parents=True)
        (dst / "SKILL.md").write_text("---\nname: example\n---\nLocal revision\n")
        (dst / "local.yaml").write_text("custom: true\n")
        with self.assertRaises(ValueError):
            self.run_install()
        self.run_install("reinstall")
        backups = list((self.root.parent / ".preflight-link-backups").iterdir())
        self.assertEqual(1, len(backups))
        self.assertIn("Local revision", (backups[0] / "SKILL.md").read_text())
        self.assertEqual("custom: true\n", (backups[0] / "local.yaml").read_text())
        self.assertTrue(dst.is_symlink())

    def test_unrelated_link_stops_whole_selection(self):
        other = self.base / "other"
        other.mkdir()
        self.root.mkdir(parents=True)
        (self.root / "example").symlink_to(other)
        second = self.base / "second"
        second.mkdir()
        (second / "SKILL.md").write_text("---\nname: second\n---\nBody\n")
        with self.assertRaises(ValueError):
            self.run_install(skills={"second": second, **self.skills})
        self.assertFalse((self.root / "second").exists())
        self.assertEqual(other.resolve(), (self.root / "example").resolve())

    def test_failed_replacement_restores_copy(self):
        dst = self.root / "example"
        dst.mkdir(parents=True)
        text = "---\nname: example\n---\nLocal\n"
        (dst / "SKILL.md").write_text(text)
        rename = Path.rename

        def fail_staged(path, target):
            if path.is_symlink():
                raise OSError("simulated link publication failure")
            return rename(path, target)

        with patch.object(Path, "rename", fail_staged), self.assertRaises(OSError):
            self.run_install("reinstall")
        self.assertFalse(dst.is_symlink())
        self.assertEqual(text, (dst / "SKILL.md").read_text())
        self.assertFalse((self.root.parent / ".preflight-link-install.lock").exists())

    def test_installed_selection_does_not_reinstall_removed_skills(self):
        self.run_install()
        with patch.object(installer, "catalog", return_value=self.skills):
            self.assertEqual(
                0,
                installer.main(
                    ["uninstall", "--target", str(self.root), "--installed"]
                ),
            )
            self.assertEqual(
                0,
                installer.main(
                    ["reinstall", "--target", str(self.root), "--installed"]
                ),
            )
        self.assertFalse((self.root / "example").exists())

    def test_preparation_link_cli_has_no_external_workflow_dependency(self):
        source = self.base / "repo/skills/define-change"
        source.mkdir(parents=True)
        (source / "SKILL.md").write_text("---\nname: define-change\n---\nStandalone.\n")
        with (
            patch.object(installer, "REPO", self.base / "repo"),
            patch.object(Path, "home", return_value=self.base / "empty-home"),
        ):
            for operation in ("install", "reinstall"):
                self.assertEqual(
                    0,
                    installer.main(
                        [operation, "--target", str(self.root), "define-change"]
                    ),
                )
                self.assertEqual(
                    source.resolve(), (self.root / "define-change").resolve()
                )
            self.assertEqual(
                0,
                installer.main(
                    ["uninstall", "--target", str(self.root), "define-change"]
                ),
            )
        self.assertFalse((self.root / "define-change").exists())
        self.assertTrue((source / "SKILL.md").is_file())

    def test_linked_preflight_shared_guidance_and_defaults_resolve(self):
        source = installer.REPO / "skills/define-change"
        installer.install_links("install", self.root, {"define-change": source})
        linked = self.root / "define-change"
        self.assertTrue((linked / "../../shared/principles.md").is_file())
        self.assertTrue((linked / "../../config/model-roles.default.yaml").is_file())

    def test_symlink_directory_and_source_overlap_are_rejected(self):
        self.root.parent.mkdir(parents=True)
        self.root.symlink_to(self.source)
        with self.assertRaises(ValueError):
            self.run_install()
        self.root.unlink()
        with self.assertRaises(ValueError):
            installer.install_links("install", self.source, self.skills)

    def test_preflight_user_install_links_and_converts_existing_copy(self):
        spec = importlib.util.spec_from_file_location(
            "preflight_deploy", installer.REPO / "deploy.py"
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        with patch.object(Path, "home", return_value=self.base / "home"):
            self.assertEqual(0, module.main(["install", "--user", "define-change"]))
            dst = Path.home() / ".agents/skills/define-change"
            self.assertEqual(installer.REPO / "skills/define-change", dst.resolve())
            dst.unlink()
            dst.mkdir()
            (dst / "SKILL.md").write_text("---\nname: define-change\n---\nLocal\n")
            self.assertEqual(0, module.main(["reinstall", "--user", "define-change"]))
            self.assertTrue(dst.is_symlink())
            self.assertEqual(0, module.main(["uninstall", "--user", "define-change"]))
            self.assertFalse(dst.is_symlink())


if __name__ == "__main__":
    unittest.main()
