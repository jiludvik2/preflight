# Existing systems and experimental work

Inspect the executable path, not just a report about it. Relevant inputs include code,
tests, build and deployment entry points, configuration, stored examples, operator steps
and local changes. Follow material dependencies across prototypes. Mark what was inspected,
what was run and what remains an inference. Within the requested recovery scope, identify
which material user or system activities the recovered requirements cover and which remain
unexamined or only partly traced. Keep this in the existing result; do not require a
repository-wide inventory or imply coverage from a few representative paths.

Apply the shared [evidence guidance](../../../shared/principles.md#proof-proportional-to-the-claim)
and choose the [document purpose](../../../shared/artifacts.md#purpose-and-maintenance).
For recovered stories, rules and acceptance examples, retain references to the supporting
implementation or execution evidence and identify any inferred user purpose. Preserve useful
observations in the descriptive result; route inferred obligations through the
[requirements guidance](requirements.md). Do not invent the historical reason for an implementation choice.

Distinguish reusable tested capability from experiment-only orchestration, diagnostics and
human input. Do not imply that migrating code automates human judgments it depended on. For
each material capability, explain whether the proposal reuses, extracts, adapts, replaces or
leaves it experimental. Prefer a suitable tested implementation to an unexplained rewrite.
If the intended production boundary is unclear, explain the alternatives and uncertainties
and ask the authorized user before treating one as settled scope.

Transfer obligations may include dependency setup, configuration, an actual production entry
point, recovery and offline replay where relevant. These are not routine coding details when
they materially affect scope or proof. Design-solution governs needed technical contracts;
the implementation lead owns transfer sequencing and execution.

Retain representative inputs, outputs and provenance for characterization and semantic
comparison. Explain deliberate corrections. Packaging or schema changes need not preserve
whole-file fingerprints; original fingerprints remain provenance. Preserve experimental
evidence when retiring duplicate executable paths under the task's authority.

If work has already started, read [execution handoff](../../../shared/execution-handoff.md).
Do not erase completed progress, rely on another worktree's uncommitted changes, or create
a competing status record while backfilling requirements.
