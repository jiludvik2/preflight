# Model routing

Use these settings for Preflight delegation, including the required
[independent challenge](independent-review.md) for Draft and substantive Revise. Routing itself
neither launches agents nor changes edit, acceptance or review permissions. Honor an explicit
user assignment first. Keep serial authoring in the current session and report a material model
mismatch. Do not add an author merely to match a preset. Other workflows retain their own
execution and panel settings.

## Activities and presets

The [default configuration](../config/model-roles.default.yaml) owns the activity matrix. It routes
each role and complexity through model aliases such as `standard` and `judgment`.

| Skill | Activity key | Roles |
| --- | --- | --- |
| define-change | `requirements` | `author`, `reviewer` |
| define-change | `domain` | `author`, `reviewer` |
| design-solution | `architecture` | `author`, `reviewer` |
| design-solution | `decision` | `analyst`, `author`, `reviewer` |
| design-solution | `design` | `author`, `reviewer` |
| design-solution | `api` | `author`, `reviewer` |

Use author for drafting or substantive revision, reviewer for Review or semantic Validate, and
analyst for framing architectural options. Use scripts for deterministic checks. Classify the
assigned work as `routine`, `complex` or `high-risk` according to its interacting concerns,
uncertainty and consequences. Use the base assignment when complexity is not established. Do not
use a routine writing assignment to bypass consequential judgment.

Both `baseline` and `optimised` profiles are retained. Baseline is the default. Optimised changes
complex domain authoring to `standard` at high effort; other task assignments are unchanged.
These are configurable presets, not proof of equal quality or measured savings. Model selectors
in the defaults are initial GPT choices, not a claim that every recipient has access to them.

## Configure your environment

Use [configure_models.py](configure_models.py) with Python 3.10 or later and PyYAML. The helper is
beside the resolver in source and installed snapshots. No search service or provider SDK is needed.
It changes only Preflight configuration, never provider credentials or the current execution host.

For Codex, collect the installed runtime's model catalog:

```sh
python3 shared/configure_models.py discover --runtime codex --output catalog.json
```

Discovery uses the documented app-server model-list operation, including returned reasoning
efforts. It starts no model thread or inference turn. A discovered name does not guarantee future
availability, sufficient quota or that a different agent can dispatch to it. Catalogs contain
model selectors and capability metadata, not credentials.

Choose selectors from that catalog for the aliases, then preview all effective activity assignments:

```sh
python3 shared/configure_models.py preview --catalog catalog.json --repo /path/to/project \
  --scope project --model standard=YOUR_STANDARD_SELECTOR \
  --model judgment=YOUR_JUDGMENT_SELECTOR --plan model-plan.json
python3 shared/configure_models.py write --plan model-plan.json --catalog catalog.json
```

Preview leaves configuration unchanged and writes only the requested reviewable plan. Write
validates that its inputs have not changed. Existing configuration is backed up before an explicit
update. Unchanged or unsupported inputs are reported; no model or effort is silently substituted.
The preview contains the proposed YAML and warns that a real update may normalize comments and
formatting. Compare it with the existing target before writing. Original bytes remain in the backup.
Keep generated catalogs and plans private.

For Claude Code, use the runtime's `/model` picker and effort controls to confirm available
selectors and supported effort levels. Automatic discovery is not supported by this helper.
Create a user-confirmed catalog with those observations, for example:

```json
{
  "version": 1,
  "runtime": "claude-code",
  "observed_at": "2026-11-20T12:00:00Z",
  "provenance": "user-confirmed",
  "models": [
    {"selector": "sonnet", "supported_reasoning_efforts": ["medium", "high"]},
    {"selector": "opus", "supported_reasoning_efforts": ["medium", "high"]}
  ]
}
```

This is a format example, not evidence that those selectors or efforts are available to you.
Replace it with your observations and actual UTC observation time. Runtime aliases can change
underlying models; use a pinned selector when reproducibility requires it. Do not infer effort
support from an alias or a provider's public model list. Use one runtime per catalog and setup.

The helper checks every effective role at unspecified, routine, complex and high-risk complexity
under both profiles. Unknown models and unsupported efforts prevent writing. Existing role and
profile customizations remain intact. When an effort needs changing, make an explicit supported
leaf change with repeated `--effort` options; inspect `--help` and the full preview before writing.
An available model need not be suitable for every role: the user chooses the alias assignments.

## Resolve an assignment

Run [resolve_model.py](resolve_model.py) before a configured dispatch, with the target project root:

```sh
python3 shared/resolve_model.py --repo /path/to/project \
  --workflow domain --role author --complexity complex
```

From a skill linked to this checkout, the resolver is `../../shared/resolve_model.py` relative to
the skill directory. In a self-contained snapshot it is `references/_shared/resolve_model.py`.
Both preparation skills use the same external configuration, in this order:

1. `<target-project>/.preflight/model-roles.yaml`, if present.
2. Otherwise `~/.config/preflight/model-roles.yaml`, if present.
3. Otherwise the shipped defaults.

Select one external file; do not merge project and user files. Creating a new project configuration
through the helper preserves the effective user customization before applying the requested changes.
A user-level preview warns when a project configuration will continue to take precedence.

Within the selected configuration, merge shipped common settings, shipped selected profile,
external common settings and external selected profile, then resolve defaults, role and matching
complexity settings. A broad default does not erase a more specific setting. Invalid selected
files, undefined aliases and invalid inactive profiles are errors, not permission to fall back.
Set `profile: optimised` in your override to select that profile; keep existing activity overrides
unless you intend to change them.

## Use the result honestly

The resolver reports profile, activity, role, complexity, model selector, effort and configuration
source. Check the actual dispatch tool's supported models and efforts. A catalog or resolved
assignment does not switch hosts or prove a model invocation occurred. Do not silently replace
an unavailable assignment, raise spending or claim an unperformed review. Continue independent
work and report any required review that cannot run. Independent review needs a fresh context
even if author and reviewer use the same model.

If PyYAML or runtime catalog access is unavailable, report that limitation and use a permitted
existing environment or the explicit manual catalog path. Do not install dependencies automatically.
Serial work may continue. Record the selected and actual assignment, including overrides or material
mismatches, in the existing result or delegation message; no separate report is required.

Provider references: [Codex app-server](https://developers.openai.com/codex/app-server) and
[Claude Code model configuration](https://code.claude.com/docs/en/model-config).
