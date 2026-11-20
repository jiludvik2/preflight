import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def load_resolver(path):
    spec = importlib.util.spec_from_file_location("model_resolver", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.repo = self.root / "project"
        self.repo.mkdir()
        self.user = self.root / ".config/preflight/model-roles.yaml"
        self.repo_config = self.repo / ".preflight/model-roles.yaml"
        self.resolver = load_resolver(ROOT / "shared/resolve_model.py")
        self.home_patch = patch.object(
            self.resolver.Path, "home", return_value=self.root
        )
        self.home_patch.start()

    def tearDown(self):
        self.home_patch.stop()
        self.temporary.cleanup()

    def write(self, path, content):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def resolve(self, workflow="domain", role="author", complexity="complex"):
        return self.resolver.resolve(workflow, role, complexity, self.repo)

    def test_shipped_task_assignments_for_both_profiles(self):
        standard_medium = ("gpt-6-sol", "medium", "standard")
        standard_high = ("gpt-6-sol", "high", "standard")
        judgment_medium = ("gpt-6-astra", "medium", "judgment")
        judgment_high = ("gpt-6-astra", "high", "judgment")
        complexity_levels = (None, "routine", "complex", "high-risk")
        assignments = {
            ("requirements", "author"): (
                standard_medium,
                standard_medium,
                standard_high,
                judgment_high,
            ),
            ("requirements", "reviewer"): (
                standard_medium,
                standard_medium,
                standard_high,
                judgment_high,
            ),
            ("domain", "author"): (
                judgment_high,
                standard_medium,
                judgment_medium,
                judgment_high,
            ),
            ("domain", "reviewer"): (
                judgment_high,
                standard_medium,
                judgment_high,
                judgment_high,
            ),
            ("architecture", "author"): (
                judgment_high,
                standard_high,
                judgment_high,
                judgment_high,
            ),
            ("architecture", "reviewer"): (
                judgment_high,
                standard_high,
                judgment_high,
                judgment_high,
            ),
            ("decision", "analyst"): (
                standard_high,
                standard_high,
                judgment_high,
                judgment_high,
            ),
            ("decision", "author"): (
                standard_high,
                standard_medium,
                standard_high,
                judgment_high,
            ),
            ("decision", "reviewer"): (
                standard_high,
                standard_high,
                standard_high,
                judgment_high,
            ),
            ("design", "author"): (
                standard_high,
                standard_medium,
                standard_high,
                judgment_high,
            ),
            ("design", "reviewer"): (
                standard_high,
                standard_medium,
                standard_high,
                judgment_high,
            ),
            ("api", "author"): (
                standard_high,
                standard_medium,
                standard_high,
                judgment_high,
            ),
            ("api", "reviewer"): (
                standard_high,
                standard_medium,
                standard_high,
                judgment_high,
            ),
        }
        shipped = self.resolver.read_yaml(ROOT / "config/model-roles.default.yaml")
        self.assertEqual(set(complexity_levels[1:]), set(self.resolver.COMPLEXITIES))
        self.assertEqual(
            set(assignments),
            {
                (task, role)
                for task, workflow in shipped["workflows"].items()
                for role in workflow["roles"]
            },
        )
        for profile in ("baseline", "optimised"):
            self.write(self.user, f"version: 2\nprofile: {profile}\n")
            for (task, role), expected_levels in assignments.items():
                for level, expected in zip(
                    complexity_levels, expected_levels, strict=True
                ):
                    with self.subTest(
                        profile=profile, task=task, role=role, level=level
                    ):
                        if (profile, task, role, level) == (
                            "optimised",
                            "domain",
                            "author",
                            "complex",
                        ):
                            expected = standard_high
                        actual = self.resolve(task, role, level)
                        self.assertEqual(
                            (*expected, profile),
                            tuple(
                                actual[field]
                                for field in (
                                    "model",
                                    "reasoning_effort",
                                    "alias",
                                    "profile",
                                )
                            ),
                        )

    def test_optimised_has_only_one_ported_difference(self):
        self.assertEqual(
            ("judgment", "medium"),
            (self.resolve()["alias"], self.resolve()["reasoning_effort"]),
        )
        self.write(self.repo_config, "version: 2\nprofile: optimised\n")
        self.assertEqual(
            ("standard", "high"),
            (self.resolve()["alias"], self.resolve()["reasoning_effort"]),
        )
        self.assertEqual("judgment", self.resolve(complexity="high-risk")["alias"])
        self.assertEqual("judgment", self.resolve(role="reviewer")["alias"])

    def test_repo_overrides_user_without_merging_them(self):
        self.write(
            self.user,
            "version: 2\nprofile: optimised\nmodels:\n  standard: user-model\n",
        )
        self.assertEqual("user-model", self.resolve()["model"])
        self.write(self.repo_config, "version: 2\nmodels:\n  judgment: project-model\n")
        result = self.resolve()
        self.assertEqual(
            ("project-model", "baseline", str(self.repo_config)),
            (result["model"], result["profile"], result["config_path"]),
        )

    def test_alias_swap_and_fieldwise_profile_overrides(self):
        self.write(
            self.repo_config,
            """version: 2
profile: optimised
models:
  standard: custom-standard
  judgment: custom-judgment
workflows:
  domain:
    roles:
      author:
        complexity:
          complex: {model: judgment}
profiles:
  optimised:
    workflows:
      domain:
        roles:
          author:
            complexity:
              complex: {reasoning_effort: max}
""",
        )
        result = self.resolve()
        self.assertEqual(
            ("custom-judgment", "max"), (result["model"], result["reasoning_effort"])
        )
        self.assertEqual("custom-standard", self.resolve("api")["model"])
        self.assertEqual("custom-standard", self.resolve("requirements")["model"])

    def test_invalid_config_never_falls_back(self):
        for content in (
            "version: 1\n",
            "version: 2\nmodles: {}\n",
            "version: 2\nprofile: cheaper\n",
            "version: 2\nmodels: {standard: ''}\n",
            "version: 2\nmodels: {standard: judgment}\n",
            "version: 2\nmodels:\n  standard: first\n  standard: second\n",
            "version: 2\nworkflows: {design: {roles: {auther: {}}}}\n",
            "version: 2\nworkflows: {unknown: {roles: {author: {}}}}\n",
            "version: 2\nworkflows: {domain: {roles: {author: {complexity: {tiny: {}}}}}}\n",
            "version: 2\nprofiles: {optimised: {defaults: {model: missing}}}\n",
            "version: 2\nprofiles: {optimised: {models: {standard: other}}}\n",
            "version: 2\ndefaults: {reasoning_effort: [high]}\n",
        ):
            with self.subTest(content=content):
                self.write(self.repo_config, content)
                with self.assertRaises(self.resolver.ConfigError):
                    self.resolve()

    def test_broken_link_missing_yaml_and_unknown_task_are_reported(self):
        with self.assertRaises(self.resolver.ConfigError):
            self.resolve("missing")
        with patch.object(self.resolver, "yaml", None):
            with self.assertRaisesRegex(self.resolver.ConfigError, "PyYAML"):
                self.resolve()
        self.repo_config.parent.mkdir()
        self.repo_config.symlink_to(self.root / "absent.yaml")
        with self.assertRaisesRegex(self.resolver.ConfigError, "cannot read"):
            self.resolve()

    def test_legacy_config_is_not_read_or_changed(self):
        for legacy in (
            self.repo / ".delivery-readiness/model-roles.yaml",
            self.root / ".config/delivery-readiness/model-roles.yaml",
        ):
            self.write(legacy, "unrelated settings\n")
        self.assertEqual("default", self.resolve()["source"])
        self.assertEqual("unrelated settings\n", legacy.read_text())

    def test_installed_resolver_works_independently_and_preserves_external_config(self):
        self.write(
            self.user,
            "version: 2\nprofile: optimised\nmodels:\n  standard: operator-model\n",
        )
        original = self.user.read_bytes()
        target = self.root / "installed/skills"
        for skill in ("define-change", "design-solution"):
            for operation in ("install", "reinstall"):
                subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / "deploy.py"),
                        operation,
                        "--target",
                        str(target),
                        skill,
                    ],
                    check=True,
                    capture_output=True,
                )
                resolver = target / skill / "references/_shared/resolve_model.py"
                result = subprocess.run(
                    [
                        sys.executable,
                        str(resolver),
                        "--repo",
                        str(self.repo),
                        "--user-config",
                        str(self.user),
                        "--workflow",
                        "domain",
                        "--role",
                        "author",
                        "--complexity",
                        "complex",
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual("operator-model", json.loads(result.stdout)["model"])
                self.assertFalse(list((target / skill).rglob("__pycache__")))
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "deploy.py"),
                    "uninstall",
                    "--target",
                    str(target),
                    skill,
                ],
                check=True,
                capture_output=True,
            )
            self.assertEqual(original, self.user.read_bytes())


if __name__ == "__main__":
    unittest.main()
