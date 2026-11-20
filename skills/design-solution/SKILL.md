---
name: design-solution
description: Recover, establish or assess architecture and technical contracts, including component boundaries, ADRs, technical designs, API contracts and requested models. Use for documenting an existing implementation, a bounded solution or its review. Not for free-form exploration, routine code structure, execution planning or implementation.
---

# Design solution

Explain how the intended behavior can be delivered, with clear boundaries, contracts and
proof. Produce the fewest useful artifacts. Do not require an ADR, architecture overview
and detailed design for every change.

Read [working principles](../../shared/principles.md) on every invocation. Read
[artifact conventions](../../shared/artifacts.md) before creating or revising durable documents,
or checking their identity or lifecycle.
Use its [default front matter](../../shared/artifacts.md#default-front-matter) for governing
documents when the repository has no convention. Descriptions, indexes, evidence and diagrams are exempt.
Read [model assignments](../../shared/model-selection.md) when selecting a model for Preflight work.

For Draft or substantive Revise, read and start [independent challenge](../../shared/independent-review.md)
before authoring. It includes complete chat proposals and substantive as-built recovery. Arrange
source-only reviewer framing first, then candidate challenge and any final correction check.
Meaning-preserving editorial changes are exempt. Review and Validate do not recursively delegate.

Before drafting or revising deliverables, apply the local [writing guidance](../../shared/writing.md).
Preserve repository artifact conventions, technical meaning and acceptance boundaries.

## Approach

### Establish scope and authority

Establish the requested outcome, operation and affected scope. Inspect governing requirements,
domain meanings, ADRs, architecture, designs, protocols and implementation. For recovery,
use the shared artifact conventions to distinguish an as-built description from a governing
contract or proposal. Check authority, scope and exclusions, not just the presence of a citation.
Report a missing domain decision before choosing mechanics that would invent it.
Independent design work may continue.

Read any existing project glossary and the terminology in relevant governing requirements.
Use those terms consistently in prose, contracts and diagram labels, preserving their meanings
and distinctions. If sources conflict or leave a material term unclear, identify the ambiguity
and the affected design decision instead of silently redefining it.

Write for humans and implementing agents who do not have the originating conversation. Explain
the problem, purpose, responsibilities and normal behavior before detailed mechanics. Make
consequential inputs, conditions, actions and outcomes explicit. Organize for the artifact: an
ordered flow can explain a workflow, context and responsibilities explain architecture, and
operations and semantics explain an interface. Preserve required templates and diagrams without
imposing one universal outline. Use the shared [concept explanations](../../shared/principles.md#useful-explanations)
before schemas or algorithms. Check that a domain-facing operation has a purpose and appropriate
decision authority independently of its presence in code.

### Select the relevant guidance

Separate architectural choices from their technical realization. Reuse settled contracts;
propose only the missing change. Select and read the relevant reference before working on it:

- [Architecture](references/architecture.md) for component boundaries, interfaces, main technology choices and decomposition. Every architecture document created or revised includes the system context diagram defined there.
- [Decisions](references/decisions.md) for ADR analysis, authoring, substantive revision or assessment, including decision boundaries and verification obligations.
- [Technical contracts](references/technical-contracts.md) for technical designs, protocols, HTTP contracts and consequential execution dependencies.
- [Models](references/models.md) for the required architecture context diagram and other requested or useful models.
- [Lifecycle](references/lifecycle.md) for changes to accepted designs and retained amendments.
- [Execution handoff](../../shared/execution-handoff.md) when handing work to an execution lead or changing in-flight work.

For internal Python contracts, apply the [representation defaults](references/technical-contracts.md#internal-python-contracts)
when choosing contract artifacts.

### Use research and implementation evidence

When research motivates a new or amended governing contract, inspect the completed bounded
inquiry result, the decision its evidence supports, and the specific behavior or contract change.
Establish why existing governing contracts do not cover that outcome; reuse an adequate
contract rather than amending it to mirror the experiment. A new capability can require a new
contract without a defect in the old one. Experimental rules, schemas and sketches remain
inquiry material until a justified proposal follows the existing acceptance process.
This entry check does not require a prerequisite spike for an explicitly requested design
task or prevent an experimental sketch within an inquiry.

For descriptive recovery, check the inspected implementation, revision, scope and evidence
limits. Recovery does not need a proposed contract change or a reason to replace existing authority.
Inspect material executable dependencies when code or experimental work informs the design.
Distinguish tested behavior, manual inputs and limitations from accepted intent. Use the shared
[investigation guidance](../../shared/principles.md#investigate-disputed-premises) for consequential
disputed factual premises, using available read-only tools to research a framed uncertainty. Do not treat research,
existing packages or prototype success as approval of an architectural choice.
If an amendment was accepted after a premature recommendation, preserve its acceptance and
identify the earlier evidence or sequencing error; do not silently revoke the accepted contract.

## Finish the requested operation

### Draft or revise

For Draft or substantive Revise, complete [independent challenge](../../shared/independent-review.md)
for the affected concern.
Report unavailable independent review explicitly rather than claiming reviewed completion.

For substantive revision, reread and consolidate the complete affected section instead of appending
successive clarifications. Give each rule one owning location and reference it elsewhere. Remove
repetition while preserving conditions, exceptions, safeguards, governing references and stable link
targets. Keep the detail needed to explain and implement the design; no fixed document length is a target.

For Draft or substantive Revise, inspect the complete result against its supporting evidence
and a representative end-to-end scenario. Check governing claims against accepted sources.
Check as-built descriptions against the inspected implementation. Report discrepancies with
governing sources without silently resolving them. Check responsibility and interface fit,
supported mechanisms, verification obligations and each explicit deliverable. Supply each
requested model, adequately reuse it or report it unresolved. Do not silently replace or omit it.

When a revision changes a name, responsibility, owner, hosting choice or interface, follow
[change consistency](references/technical-contracts.md#changes-and-completion) through the affected artifacts.

Check comprehension from both perspectives:

- Can a human reading in order explain the problem, responsibilities, normal behavior and important exceptions?
- Can an implementing agent determine the inputs, next action, decision conditions, expected output
  and unresolved choices without inventing behavior or consulting the conversation?

Where interpretation is still necessary, report the specific missing explanation, rule or decision,
the affected behavior and the next action. These checks need no score or new approval gate.
Independent challenge covers the coherent concern, without requiring a reviewer for every document.

### Review or validate

For general Review, use broad read-only judgment over the requested concern. Do not turn it
into a fixed validation checklist or author a replacement. In an architecture Review, identify a
missing or incorrect system context diagram without editing it. For bounded Validate, check only
the named properties and directly affected consequences. Apply the composition, consolidation and
comprehension considerations above proportionately within that boundary. Report concrete gaps;
neither operation revises or accepts artifacts.

### Return the result

Return the result, evidence-backed findings, independent work that can continue and any
prepared user decision. State what is proposed, governed and unverified. A complete proposal
must identify the governing revisions, affected contracts and proof, and any remaining
acceptance dependency in a lead handoff. Use the execution-handoff guidance above. A proposal
is not implementation authority. Missing or conflicting accepted decisions or designs block
only dependent implementation readiness. Return delegated questions to the lead. Do not start
a second coordinator or a new execution plan.
