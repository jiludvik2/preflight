---
name: define-change
description: Establish or revise the intended behavior and domain meaning of a bounded product change, including recovering requirements and domain models from an existing system. Use for requirements briefs, domain models and context relationships, their assessment, or requested requirements and domain visualisations. Not for free-form exploration, implementation planning, or technical design.
---

# Define change

Help the user and implementer agree what should happen and what it means in the domain.
Start from a problem, objective or concrete examples. An existing glossary, domain model,
specialist profile or fixed discovery sequence is not a prerequisite.

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

## Approach

### Understand the request

Understand the requested outcome and operation. Inspect the relevant project sources and
their authority before treating an existing behavior as a requirement. Identify product users,
readers and people authorized to make business decisions only as far as the task and evidence support.

For recovery, distinguish observed behavior from a proposal to change it. Use the shared
artifact conventions to keep descriptions separate from governing requirements.

Work through representative activities and examples. Establish observable outcomes, business
meaning, boundaries and exceptions together where that is useful. Separate confirmed facts,
proposals and consequential unknowns. Investigate available evidence before asking about a
product choice. Do not ask the user for facts available in the repository.

When an investigation or spike depends on unsettled intended behavior or domain meaning,
establish that meaning here before its method or metric is chosen. Name the practical decision,
affected users, relevant practitioner views, actual decision authority, and what would count as
credible evidence and material impact for that decision. Record consequential interpretations
agreed in discussion with their rationale and sources. Expert assessment of evidence does not
accept a product rule. If existing accepted meanings already settle the question, point the
investigation to them instead of reopening the model.

### Choose the output and supporting guidance

Choose the smallest durable result that serves the next activity. A requirements brief
describes intended behavior and acceptance examples. A domain model explains reusable business
meaning and rules. Use both only when both have distinct work to do. The domain model does not
own UI design, software components or database schemas. The brief does not become a delivery plan.

Read the relevant guidance before authoring or assessing that content:

- [Requirements](references/requirements.md) for outcomes, acceptance criteria, scope and identity.
- [Domain meaning](references/domain-meaning.md) for concepts, rules, terminology, context relationships and examples.
- [Existing systems](references/existing-systems.md) when code, experiments or prior delivery are inputs.
- [Execution handoff](../../shared/execution-handoff.md) when handing work to an execution lead or changing in-flight work.

Apply [context analysis](references/domain-meaning.md#contexts-and-relationships) when material contextual
relationships or information restrictions affect the requested outcome, even without a map request.

<a id="model-requirements-when-requested"></a>
### Model requirements and domain meaning when requested

Apply [modelling guidance](references/models.md) when the user requests models or visualisations
of requirements or domain meaning, including ordinary requests such as "draw the business flow". The request can
cover one concern or the whole document: "model these requirements throughout" lets you select
suitable views across that scope. Do not require the user to name a notation or list artefacts.

Generate modelling deliverables only when requested, in chat as well as files. An ordinary
review can reason through combinations and use small explanatory tables without producing a
model bundle. "Suggest where modelling would help" asks for recommendations, not model creation.
Preserve Draft, Revise, Review and Validate semantics; modelling is a requested output, not a
new lifecycle operation. Before creating affected models, check the necessary business decisions
against the objective and flag consequential gaps to the user as the modelling guidance specifies.

### Investigate disputed premises

Use the shared [investigation guidance](../../shared/principles.md#investigate-disputed-premises)
for consequential disputed factual premises. Use available read-only tools for a framed evidence
question that needs external or codebase investigation, and state evidence limits.
Research informs the proposal. It does not settle the user's business choice or grant authority.

## Finish the requested operation

### Draft or revise

For Draft or substantive Revise, complete [independent challenge](../../shared/independent-review.md)
for the affected concern.
Report unavailable independent review explicitly rather than claiming reviewed completion.

For Draft or substantive Revise, inspect the resulting artifact against the governing sources
and a representative scenario. Check semantic correctness, terminology fit and reader
comprehension separately. Confirm that explicit requested outputs are supplied, uncertainty
and proposed status are visible, and the next specialist can proceed without the conversation.
For requirements, apply the [requirement-boundary and ID check](references/requirements.md#check-requirement-boundaries-and-identifiers)
to the changed obligations, their existing owners and affected acceptance criteria. This scoped check
does not require a full review of unrelated requirements.

### Review or validate

For a general Review, use professional judgment over the whole concern and report useful
findings without editing. For bounded Validate, test the requested properties and directly
affected consequences. Neither requires a fixed report or an extra approval round.
For requirements, follow the [requirements review protocol](references/requirements.md#review-requirements).
It checks objective support, necessity, meaning, decision logic and comprehensibility for humans
and agents. Apply its checks to the requested scope, not as a mandatory full audit for validation.

### Return the result

Return the artifact or assessment, material unresolved findings with actionable context,
what can proceed and whether user action is needed now. Preserve accepted IDs and baselines.
For a lead handoff, include the current sources and status, the affected work and proof,
and any limits on the next activity through the execution-handoff guidance above.
Return delegated questions to the active lead; ask directly when invoked standalone. Do not
start another coordinator, invent technical decisions or claim acceptance without authority.
