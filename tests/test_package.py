from pathlib import Path
import json
import re
import subprocess
import sys
import tempfile
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("define-change", "design-solution")
LINK = re.compile(r"\]\(([^)]+)\)")


class PackageTests(unittest.TestCase):
    def assert_local_links(self, content_root, boundary):
        for document in content_root.rglob("*.md"):
            for link in LINK.findall(document.read_text()):
                if "://" in link or link.startswith("#"):
                    continue
                destination = (document.parent / link.split("#", 1)[0]).resolve()
                with self.subTest(document=document, link=link):
                    self.assertTrue(destination.is_relative_to(boundary.resolve()))
                    self.assertTrue(destination.is_file(), str(destination))

    def test_source_links_resolve_within_the_pack(self):
        self.assert_local_links(ROOT / "skills", ROOT)
        self.assert_local_links(ROOT / "shared", ROOT)

    def test_pack_navigation_resolves(self):
        documents = (ROOT / "README.md",)
        for document in documents:
            for link in LINK.findall(document.read_text()):
                if "://" in link or link.startswith("#"):
                    continue
                with self.subTest(document=document, link=link):
                    self.assertTrue((document.parent / link.split("#", 1)[0]).exists())

    def test_real_packages_install_individually_with_self_contained_references(self):
        for name in SKILLS:
            with self.subTest(skill=name), tempfile.TemporaryDirectory() as temporary:
                target = Path(temporary) / "skills"
                result = subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / "deploy.py"),
                        "install",
                        "--target",
                        str(target),
                        name,
                    ],
                    env={
                        "HOME": str(Path(temporary) / "empty-home"),
                        "CODEX_HOME": str(Path(temporary) / "empty-codex"),
                        "PYTHONDONTWRITEBYTECODE": "1",
                    },
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual({name}, {path.name for path in target.iterdir()})
                package = target / name
                self.assert_local_links(package, package)
                self.assertFalse((package / "tests").exists())
                self.assertFalse((package / "evaluations").exists())
                self.assertFalse((package / "deploy.py").exists())
                self.assertTrue(
                    (package / "references/_shared/principles.md").is_file()
                )

    def test_preparation_cli_lifecycle_preserves_config_and_metadata(
        self,
    ):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "skills"
            package = target / "design-solution"

            def run(operation, *extra):
                result = subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / "deploy.py"),
                        operation,
                        "--target",
                        str(target),
                        *extra,
                        "design-solution",
                    ],
                    env={
                        "HOME": str(Path(temporary) / "empty-home"),
                        "CODEX_HOME": str(Path(temporary) / "empty-codex"),
                        "PYTHONDONTWRITEBYTECODE": "1",
                    },
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(0, result.returncode, result.stderr)

            run("install")
            metadata = yaml.safe_load((package / "agents/openai.yaml").read_text())
            self.assertEqual(
                yaml.safe_load(
                    (ROOT / "skills/design-solution/agents/openai.yaml").read_text()
                ),
                metadata,
            )
            self.assertIn("$design-solution", metadata["interface"]["default_prompt"])
            receipt = json.loads((package / ".preflight-owner.json").read_text())
            self.assertEqual("design-solution", receipt["skill"])
            self.assertIn("agents/openai.yaml", receipt["managed_files"])
            self.assert_local_links(package, package)

            config = package / "preferences.yaml"
            config.write_bytes(b"retain: true\n")
            run("reinstall")
            self.assertEqual(b"retain: true\n", config.read_bytes())
            self.assertEqual(
                metadata, yaml.safe_load((package / "agents/openai.yaml").read_text())
            )
            before = {
                path.relative_to(package): path.read_bytes()
                for path in package.rglob("*")
                if path.is_file()
            }
            backups = target.parent / ".preflight-backups"
            existing = set(backups.iterdir())
            run("uninstall")
            self.assertFalse(package.exists())
            (backup,) = set(backups.iterdir()) - existing
            identifier = backup.name.removeprefix("design-solution-")
            run("restore", "--backup", identifier)
            self.assertEqual(
                before,
                {
                    path.relative_to(package): path.read_bytes()
                    for path in package.rglob("*")
                    if path.is_file()
                },
            )


if __name__ == "__main__":
    unittest.main()
