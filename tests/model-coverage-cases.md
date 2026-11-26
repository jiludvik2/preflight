# Model coverage regression cases

Run each task with the named skill in a disposable project. Give the author only the task and
project facts, then inspect the actual result against the expected behavior. These cases test
selection and semantic consistency; metadata or diagram rendering alone cannot establish a pass.

## Simple requirement

Task: use define-change to specify an existing form's age rule. Applicants aged 18 or older may
apply. The form already supplies age in whole years; no other rule changes.

Expected: preserve inclusive age 18 and useful 17/18/19 examples. Do not require a diagram bundle
or an omission checklist for this isolated rule.

## Lifecycle and conditional requirements

Task: use define-change to specify work requests owned by requesters. Draft requests may be
edited and submitted. Submission changes Draft to Submitted. Review closes a Submitted request;
it approves only when active clearance and valid entitlement are both true, and otherwise rejects.
The requester may withdraw before review closes it. Closed requests are immutable. Approved,
Rejected and Withdrawn are completion outcomes, not lifecycle states.

Expected: make identity and ownership explicit, cover all four Boolean input pairs, and supply
consistent lifecycle and decision representations without a diagram request. Preserve the
status/outcome distinction and do not invent a priority for simultaneous review and withdrawal.
Use Mermaid state models; no external statechart skill or formal checker is required. Report
source review, syntax, rendering and viewer checks separately.

## Collaborating components

Task: use design-solution to specify a local import package. SourceReader reads bytes;
DocumentParser parses supplied bytes without file access; ImportCoordinator calls these and
sends valid records to RecordRepository. The repository commits all records atomically or rolls
back. Read/parse errors cause no writes. The caller receives success only after commit. All four
components run in one process.

Expected: show responsibilities, boundaries and material invocation/data connections in a
component view without an explicit diagram request. A sequence or activity flow may supplement
that structural explanation. Preserve parsing purity, no-write failures, atomicity and completion.

## Revise contracts without losing useful views

Task: start with a design containing component and normal-sequence views for EntryPoint,
Validator and Calculator. Validator currently loads referenced source snapshots. Revise it so
EntryPoint loads the snapshots and passes exact bytes to pure Validator. Validator returns
CheckedInput or Rejection; Calculator accepts CheckedInput and returns Calculation or Failure.
EntryPoint emits one structured result. Keep the same local process and remaining responsibilities.

Expected: update contracts and affected views while preserving both structural explanation and
scenario ordering. Move file-access connections to EntryPoint. A sequence-only replacement of
the component view fails even when its calls are correct. Additional error decisions must remain
proposed when the source does not settle them.
