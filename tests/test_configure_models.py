"""Configuration behavior through disposable files and a fake app-server process."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shared"))
import configure_models as configure  # noqa: E402


class ConfigurationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.repo = self.root / "project"
        self.repo.mkdir()
        self.user = self.root / "user/model-roles.yaml"
        self.target = self.repo / ".preflight/model-roles.yaml"
        self.defaults = self.root / "defaults.yaml"
        shutil.copyfile(ROOT / "config/model-roles.default.yaml", self.defaults)
        self.catalog = self.root / "catalog.json"
        self.plan = self.root / "plan.json"
        self.catalog_data = {
            "version": 1,
            "runtime": "codex",
            "observed_at": "2026-11-20T12:00:00Z",
            "provenance": "user-confirmed",
            "models": [
                {"selector": model, "supported_reasoning_efforts": ["medium", "high"]}
                for model in ("gpt-6-sol", "gpt-6-astra", "available")
            ],
        }
        self.save_catalog()

    def save_catalog(self):
        self.catalog.write_text(json.dumps(self.catalog_data))

    def preview(self, models=None, efforts=None, scope="project"):
        return configure.preview(
            self.catalog,
            self.repo,
            scope,
            models or {},
            efforts or {},
            user_config=self.user,
            defaults=self.defaults,
        )

    def save_plan(self, result):
        self.plan.write_text(json.dumps(result))

    def config(self, path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def cli(self, *arguments, script=None):
        return subprocess.run(
            [
                sys.executable,
                str(script or ROOT / "shared/configure_models.py"),
                *map(str, arguments),
            ],
            text=True,
            capture_output=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )

    def test_preview_is_read_only_and_enumerates_every_assignment(self):
        before = self.defaults.read_bytes()
        result = self.preview({"standard": "available", "judgment": "available"})
        self.assertFalse(self.target.parent.exists())
        self.assertFalse(self.user.parent.exists())
        self.assertEqual(before, self.defaults.read_bytes())
        self.assertEqual(104, len(result["assignments"]))
        self.assertEqual(
            {"baseline", "optimised"}, {a["profile"] for a in result["assignments"]}
        )
        self.assertEqual(
            {None, "routine", "complex", "high-risk"},
            {a["complexity"] for a in result["assignments"]},
        )
        self.assertEqual({"available"}, {a["model"] for a in result["assignments"]})

    def test_new_project_inherits_user_customization_and_profile(self):
        self.config(
            self.user,
            "version: 2\nprofile: optimised\ndefaults:\n  reasoning_effort: high\n"
            "profiles:\n  baseline:\n    workflows:\n      domain:\n        roles:\n          author:\n            reasoning_effort: medium\n",
        )
        self.save_plan(self.preview({"standard": "available"}))
        configure.write_plan(self.plan, self.catalog)
        result = configure.read_yaml(self.target)
        self.assertEqual("optimised", result["profile"])
        self.assertEqual("high", result["defaults"]["reasoning_effort"])
        self.assertEqual(
            "medium",
            result["profiles"]["baseline"]["workflows"]["domain"]["roles"]["author"][
                "reasoning_effort"
            ],
        )

    def test_project_override_does_not_merge_user_override(self):
        self.config(self.user, "version: 2\nmodels: {standard: unavailable}\n")
        self.config(self.target, "version: 2\n")
        self.assertTrue(self.preview()["assignments"])

    def test_user_preview_discloses_project_shadow(self):
        self.config(self.target, "version: 2\n")
        result = self.preview(scope="user")
        self.assertTrue(any("shadows" in warning for warning in result["warnings"]))
        self.save_plan(result)
        configure.write_plan(self.plan, self.catalog)
        self.assertTrue(self.user.is_file())
        self.assertEqual("version: 2\n", self.target.read_text())

    def test_existing_file_backup_is_exact_and_update_preserves_mode(self):
        original = b"# custom comment\nversion: 2\nprofile: optimised\n"
        self.target.parent.mkdir()
        self.target.write_bytes(original)
        self.target.chmod(0o640)
        plan = self.preview({"standard": "available"})
        self.assertTrue(any("normalizes" in warning for warning in plan["warnings"]))
        self.save_plan(plan)
        result = configure.write_plan(self.plan, self.catalog)
        self.assertEqual(original, Path(result["backup"]).read_bytes())
        self.assertEqual(0o640, self.target.stat().st_mode & 0o777)
        self.assertEqual(
            "available", configure.read_yaml(self.target)["models"]["standard"]
        )
        self.assertFalse(self.target.with_name(self.target.name + ".lock").exists())

    def test_noop_preserves_exact_bytes_and_creates_no_backup(self):
        original = "# retain comments\nversion: 2\nmodels: {standard: available}\n"
        self.config(self.target, original)
        self.save_plan(self.preview({"standard": "available"}))
        result = configure.write_plan(self.plan, self.catalog)
        self.assertEqual("unchanged", result["status"])
        self.assertEqual(original, self.target.read_text())
        self.assertEqual([self.target], list(self.target.parent.iterdir()))

    def test_changed_default_catalog_target_and_inherited_user_are_refused(self):
        for name in ("defaults", "catalog", "target", "user"):
            with self.subTest(name=name):
                self.config(self.user, "version: 2\n")
                self.target.unlink(missing_ok=True)
                self.save_plan(self.preview({"standard": "available"}))
                path = getattr(self, name)
                old = path.read_bytes() if path.exists() else None
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes((old or b"") + b"\n")
                with self.assertRaisesRegex(configure.ConfigError, "changed"):
                    configure.write_plan(self.plan, self.catalog)
                if old is None:
                    path.unlink()
                else:
                    path.write_bytes(old)

    def test_changed_project_shadow_is_refused_for_user_plan(self):
        self.save_plan(self.preview(scope="user"))
        self.config(self.target, "version: 2\n")
        with self.assertRaisesRegex(configure.ConfigError, "changed"):
            configure.write_plan(self.plan, self.catalog)
        self.assertFalse(self.user.exists())

    def test_tampered_plan_is_refused(self):
        plan = self.preview()
        plan["proposed_yaml"] = "version: 2\nmodels: {standard: unavailable}\n"
        self.save_plan(plan)
        with self.assertRaisesRegex(configure.ConfigError, "does not match"):
            configure.write_plan(self.plan, self.catalog)
        self.assertFalse(self.target.exists())

    def test_missing_model_and_effort_capability_are_refused(self):
        with self.assertRaisesRegex(configure.ConfigError, "absent"):
            self.preview({"standard": "unknown"})
        self.catalog_data["models"][0]["supported_reasoning_efforts"] = ["high"]
        self.save_catalog()
        with self.assertRaisesRegex(
            configure.ConfigError, "does not support effort 'medium'"
        ):
            self.preview()
        self.catalog_data["models"][0].pop("supported_reasoning_efforts")
        self.save_catalog()
        with self.assertRaisesRegex(configure.ConfigError, "explicit supported"):
            self.preview()

    def test_empty_effort_capability_never_implies_support(self):
        self.catalog_data["models"][0]["supported_reasoning_efforts"] = []
        self.save_catalog()
        with self.assertRaisesRegex(configure.ConfigError, "does not support"):
            self.preview()

    def test_catalog_requires_a_valid_timezone_aware_rfc3339_timestamp(self):
        for timestamp in (
            "not-a-date",
            "2026-11-20T12:00:00",
            "2026-11-31T12:00:00Z",
            "2026-11-20 12:00:00+00:00",
            "2026-11-20T12:00:00+01:99",
        ):
            with self.subTest(timestamp=timestamp):
                self.catalog_data["observed_at"] = timestamp
                self.save_catalog()
                with self.assertRaisesRegex(configure.ConfigError, "RFC3339"):
                    self.preview()
        for timestamp in ("2000-01-01T12:00:00Z", "2026-11-20T12:00:00.123456+05:30"):
            with self.subTest(timestamp=timestamp):
                self.catalog_data["observed_at"] = timestamp
                self.save_catalog()
                self.assertTrue(self.preview()["assignments"])

    def test_defaults_and_catalog_cannot_be_configuration_targets(self):
        for target in (self.defaults, self.catalog):
            with (
                self.subTest(target=target),
                self.assertRaisesRegex(configure.ConfigError, "separate"),
            ):
                configure.preview(
                    self.catalog,
                    self.repo,
                    "project",
                    {},
                    {},
                    user_config=self.user,
                    defaults=self.defaults,
                    target=target,
                )

    def test_inactive_profile_and_unspecified_complexity_are_checked(self):
        for override in (
            "version: 2\nprofiles:\n  optimised:\n    defaults: {reasoning_effort: ultra}\n",
            "version: 2\nworkflows:\n  domain:\n    roles:\n      author:\n        reasoning_effort: ultra\n",
        ):
            self.config(self.target, override)
            with self.assertRaisesRegex(configure.ConfigError, "does not support"):
                self.preview()

    def test_explicit_effort_leaf_edit_and_unknown_alias_path(self):
        result = self.preview(
            efforts={
                "profiles.optimised.workflows.domain.roles.author.reasoning_effort": "medium"
            }
        )
        selected = [
            a
            for a in result["assignments"]
            if a["profile"] == "optimised"
            and a["workflow"] == "domain"
            and a["role"] == "author"
            and a["complexity"] is None
        ]
        self.assertEqual("medium", selected[0]["reasoning_effort"])
        with self.assertRaisesRegex(configure.ConfigError, "unknown model alias"):
            self.preview({"typo": "available"})
        with self.assertRaisesRegex(configure.ConfigError, "unknown"):
            self.preview(
                efforts={"workflows.domain.roles.typo.reasoning_effort": "medium"}
            )

    def test_claude_confirmed_literal_aliases_are_not_expanded(self):
        self.catalog_data.update(runtime="claude-code", provenance="user-confirmed")
        self.catalog_data["models"] = [
            {"selector": "sonnet", "supported_reasoning_efforts": ["medium", "high"]}
        ]
        self.save_catalog()
        result = self.preview({"standard": "sonnet", "judgment": "sonnet"})
        self.assertEqual({"sonnet"}, {a["model"] for a in result["assignments"]})
        self.catalog_data["provenance"] = "codex-app-server"
        self.save_catalog()
        with self.assertRaisesRegex(configure.ConfigError, "user-confirmed"):
            self.preview()

    def test_symlink_file_ancestor_and_nonregular_targets_are_refused(self):
        self.target.parent.mkdir()
        self.target.symlink_to(self.user)
        with self.assertRaisesRegex(configure.ConfigError, "symlinks"):
            self.preview()
        self.target.unlink()
        self.target.mkdir()
        with self.assertRaisesRegex(configure.ConfigError, "regular"):
            self.preview()
        self.target.rmdir()
        self.target.parent.rmdir()
        self.user.parent.mkdir()
        self.target.parent.symlink_to(self.user.parent, target_is_directory=True)
        with self.assertRaisesRegex(configure.ConfigError, "symlinks"):
            self.preview()

    def test_actual_macos_tmp_alias_supports_preview_and_write(self):
        alias, destination = Path("/tmp"), Path("/private/tmp")
        if not alias.is_symlink() or alias.resolve() != destination:
            self.skipTest("verified macOS /tmp system alias is unavailable")
        with tempfile.TemporaryDirectory(dir=destination) as temporary:
            physical = Path(temporary).resolve()
            project = alias / physical.relative_to(destination) / "project"
            project.mkdir()
            result = self.cli(
                "preview",
                "--catalog",
                self.catalog,
                "--repo",
                project,
                "--scope",
                "project",
                "--user-config",
                self.user,
                "--defaults",
                self.defaults,
                "--plan",
                self.plan,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(str(project), json.loads(result.stdout)["repo"])
            result = self.cli("write", "--plan", self.plan, "--catalog", self.catalog)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual("written", json.loads(result.stdout)["status"])
            self.assertEqual(
                {"version": 2},
                configure.read_yaml(project / ".preflight/model-roles.yaml"),
            )

    def test_actual_macos_var_alias_passes_read_only_path_guard(self):
        alias, destination = Path("/var"), Path("/private/var")
        if not alias.is_symlink() or alias.resolve() != destination:
            self.skipTest("verified macOS /var system alias is unavailable")
        control = alias / "tmp" / self.root.name / "model-roles.yaml"
        self.assertFalse(control.parent.exists())
        self.assertEqual(
            {"path": str(control), "sha256": None}, configure.snapshot(control)
        )
        self.assertFalse(control.parent.exists())

    def test_writer_lock_refuses_update_without_overwriting(self):
        self.config(self.target, "version: 2\n")
        self.save_plan(self.preview({"standard": "available"}))
        lock = self.target.with_name(self.target.name + ".lock")
        lock.write_text("another writer")
        with self.assertRaisesRegex(configure.ConfigError, "lock exists"):
            configure.write_plan(self.plan, self.catalog)
        self.assertEqual("version: 2\n", self.target.read_text())
        self.assertEqual("another writer", lock.read_text())

    def test_cli_preview_write_resolve_and_nonoverwriting_plan(self):
        args = (
            "preview",
            "--catalog",
            self.catalog,
            "--repo",
            self.repo,
            "--scope",
            "project",
            "--model",
            "standard=available",
            "--user-config",
            self.user,
            "--defaults",
            self.defaults,
            "--plan",
            self.plan,
        )
        result = self.cli(*args)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertFalse(self.target.exists())
        self.assertNotEqual(0, self.cli(*args).returncode)
        result = self.cli("write", "--plan", self.plan, "--catalog", self.catalog)
        self.assertEqual(0, result.returncode, result.stderr)
        result = self.cli(
            "--workflow",
            "requirements",
            "--role",
            "author",
            "--repo",
            self.repo,
            "--defaults",
            self.defaults,
            script=ROOT / "shared/resolve_model.py",
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("available", json.loads(result.stdout)["model"])

    def test_cli_saved_plan_reconstructs_multiple_models_and_efforts_deterministically(
        self,
    ):
        result = self.cli(
            "preview",
            "--catalog",
            self.catalog,
            "--repo",
            self.repo,
            "--scope",
            "project",
            "--model",
            "standard=available",
            "--model",
            "judgment=available",
            "--effort",
            "workflows.requirements.roles.reviewer.reasoning_effort=medium",
            "--effort",
            "workflows.requirements.roles.author.reasoning_effort=high",
            "--user-config",
            self.user,
            "--defaults",
            self.defaults,
            "--plan",
            self.plan,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertFalse(self.target.exists())
        result = self.cli("write", "--plan", self.plan, "--catalog", self.catalog)
        self.assertEqual(0, result.returncode, result.stderr)
        config = configure.read_yaml(self.target)
        self.assertEqual(
            {"standard": "available", "judgment": "available"}, config["models"]
        )
        roles = config["workflows"]["requirements"]["roles"]
        self.assertEqual("high", roles["author"]["reasoning_effort"])
        self.assertEqual("medium", roles["reviewer"]["reasoning_effort"])

    def test_installed_sibling_defaults_and_helper_are_self_contained(self):
        installed = self.root / "installed"
        installed.mkdir()
        for name in ("configure_models.py", "resolve_model.py"):
            shutil.copyfile(ROOT / "shared" / name, installed / name)
        shutil.copyfile(self.defaults, installed / "model-roles.default.yaml")
        result = self.cli(
            "preview",
            "--catalog",
            self.catalog,
            "--repo",
            self.repo,
            "--scope",
            "project",
            "--user-config",
            self.user,
            "--plan",
            self.plan,
            script=installed / "configure_models.py",
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            str(installed / "model-roles.default.yaml"),
            json.loads(result.stdout)["defaults_path"],
        )

    def test_claude_discover_explains_manual_path_without_writing(self):
        result = self.cli(
            "discover", "--runtime", "claude-code", "--output", self.root / "new.json"
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("user-confirmed JSON catalog", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertFalse((self.root / "new.json").exists())


class CodexDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.log = self.root / "requests.jsonl"
        self.fake = self.root / "codex"
        self.fake.write_text(
            "#!"
            + sys.executable
            + "\n"
            + """
import json, os, sys, time
from pathlib import Path
log = Path(os.environ['FAKE_LOG'])
assert sys.argv[1:] == ['app-server', '--listen', 'stdio://']
for line in sys.stdin:
    request = json.loads(line)
    with log.open('a') as output:
        output.write(json.dumps(request) + '\\n')
    mode = os.environ.get('FAKE_MODE', '')
    if mode == 'timeout':
        time.sleep(5)
    if mode == 'malformed':
        print('secret-malformed-protocol', flush=True)
        continue
    if mode == 'large':
        print('X' * 2200000, flush=True)
        continue
    if request['method'] == 'initialize':
        result = {'userAgent': 'fixture'}
    elif request['method'] == 'initialized':
        continue
    else:
        cursor = request['params']['cursor']
        if mode == 'error':
            print(json.dumps({'id': request['id'], 'error': {'message': 'SECRET_TOKEN'}}), flush=True)
            continue
        record = {'id': 'other-id', 'model': 'literal-one'} if cursor is None else {'id': 'literal-two'}
        record['supportedReasoningEfforts'] = [{'reasoningEffort': 'medium'}, {'reasoningEffort': 'high'}]
        result = {'data': [record], 'nextCursor': 'page-two' if cursor is None else None}
        if mode == 'repeat':
            result['nextCursor'] = 'page-two'
    print(json.dumps({'id': request['id'], 'result': result}), flush=True)
"""
        )
        self.fake.chmod(0o755)
        self.environment = patch.dict(
            os.environ,
            {
                "PATH": str(self.root) + os.pathsep + os.environ["PATH"],
                "FAKE_LOG": str(self.log),
                "FAKE_MODE": "",
            },
        )
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def test_handshake_pagination_literal_selectors_and_no_inference(self):
        catalog = configure.discover_codex()
        self.assertEqual(
            ["literal-one", "literal-two"],
            [model["selector"] for model in catalog["models"]],
        )
        requests = [json.loads(line) for line in self.log.read_text().splitlines()]
        self.assertEqual(
            ["initialize", "initialized", "model/list", "model/list"],
            [r["method"] for r in requests],
        )
        self.assertEqual("page-two", requests[-1]["params"]["cursor"])
        self.assertEqual("codex-app-server", catalog["provenance"])

    def test_timeout_protocol_error_output_limit_and_pagination_fail_closed(self):
        for mode, message in (
            ("timeout", "timed out"),
            ("malformed", "invalid message"),
            ("error", "rejected"),
            ("large", "output limit"),
            ("repeat", "pagination cursor"),
        ):
            with self.subTest(mode=mode), patch.dict(os.environ, {"FAKE_MODE": mode}):
                with self.assertRaisesRegex(configure.ConfigError, message) as caught:
                    configure.discover_codex(timeout=0.2)
                self.assertNotIn("SECRET_TOKEN", str(caught.exception))
                self.assertNotIn("secret-malformed-protocol", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
