---
name: define-change
description: Establish or revise the intended behavior and domain meaning of a bounded product change, including recovering requirements and domain models from an existing system. Use for requirements briefs, domain models and context relationships, their assessment, and requirements and domain visualisations. Not for free-form exploration, implementation planning, or technical design.
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

Establish the intended outcome from the request and governing sources before organising
obligations. Work through representative activities and success cases. Test whether apparently
successful local work could still fail that outcome. Use the existing
[objective-support and obligation-boundary checks](references/requirements.md#quality-of-the-result)
while drafting. Establish business meaning, boundaries and exceptions together where useful.
Separate confirmed facts, proposals and consequential unknowns. Investigate available evidence
before asking about a product choice. Do not ask for facts available in the repository.

When an investigation or spike depends on unsettled intended behavior or domain meaning,
establish that meaning here before its method or metric is chosen. Name the practical decision,
affected users, relevant practitioner views, actual decision authority, and what would count as
credible evidence and material impact for that decision. Record consequential interpretations
agreed in discussion with their rationale and sources. Expert assessment of evidence does not
accept a product rule. If existing accepted meanings already settle the question, point the
investigation to them instead of reopening the model.

### Develop through focused rounds

During Draft and substantive Revise, develop relevant domain meaning, obligations and selected
models together, using the guidance below. Start with a coherent account sufficient to test the
intended outcome. Refine it when a concrete defect, new evidence or user input warrants another
round; do not wait for a complete catalogue before applying the quality criteria.

Match user involvement to the requested working style. In interactive work, offer early feedback
on outcome framing, central domain distinctions or substantive alternatives when it could change
direction. In autonomous work, continue authorised drafting and refinement without routine approval
checkpoints. A consequential product choice not delegated to the agent, or missing permission,
blocks only dependent work. Prepare the concrete choice and consequences through the existing
findings guidance; continue independent permitted work. Distinguish feedback, a required decision
and acceptance. Silence supplies neither a decision nor acceptance.

Apply feedback at its owning source, then reconcile affected requirements, definitions, models
and examples through the existing consistency comparison. Preserve settled decisions and
unaffected valid work. Use the existing independent challenge procedure for the coherent
candidate and substantive corrections; refinement does not require a new reviewer or full review
for every round. Finish the requested operation when its result supports the intended next use
and required checks, material findings and limits are accounted for. Further rounds need a named
defect, changed input or requested improvement; optional polish does not keep the task open.

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
During Draft and substantive Revise, use the
[question-to-technique aid](references/models.md#choose-a-technique-for-the-question) to select and include
useful representations from the requirements and domain structure, including already settled rules.
Apply its priorities and content triggers; reuse adequate views and account for material omissions.
Use the smallest set that explains materially distinct concerns. Review and Validate assess model
adequacy within their read-only scope.

<a id="model-requirements-when-requested"></a>
### Model requirements and domain meaning

Apply [modelling guidance](references/models.md) during Draft and substantive Revise. Select useful
views based on what the requirements cover, without waiting for a diagram request or an ambiguity.
Include selected views beside their owning rules in the document or chat result, within the original
scope; do not create a separate modelling portfolio or ledger by default. Simple isolated rules may
need only a boundary example. Honour explicit format and scope limits and explicitly requested views.

"Suggest where modelling would help" asks for recommendations only. Review and Validate remain
read-only: evaluate whether the representations adequately explain the affected meaning and report
findings without adding or revising models. Before creating affected models, check necessary business
decisions against the objective. Follow the modelling guidance for provisional alternatives and
decisions that block a settled view. A selected state-transition view uses the
[state-transition guidance](references/models.md#state-transitions).

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

For Draft or substantive Revise, use the [model coverage checks](references/models.md#verify-and-report)
to identify missing representations before assessing supplied models. Apply those checks in the
existing independent review too. On revision, preserve the explanatory purpose of removed or
replaced views. Inspect the resulting artifact against governing sources and a representative
scenario. Apply [consistency comparison](../../shared/principles.md#compare-related-representations)
to selected models and their material relationships within this check. Check semantic correctness, terminology fit and reader
comprehension separately. Confirm that selected views and explicitly requested outputs are supplied, uncertainty
and proposed status are visible, and the next specialist can proceed without the conversation.
For requirements, apply the [requirement-boundary and ID check](references/requirements.md#check-requirement-boundaries-and-identifiers)
to the changed obligations, their existing owners and affected acceptance criteria. This scoped check
does not require a full review of unrelated requirements.
The initial whole-draft review covers all proposed obligations. For a revision or a later
correction check, cover changed meaning, affected obligations and unresolved findings, even
when their IDs stay unchanged. The author and independent reviewer use the obligation-level
analysis in the linked check; a list of valid IDs does not establish semantic coverage.

### Review or validate

For a general Review, use professional judgment over the whole concern and report useful
findings without editing. For bounded Validate, test the requested properties and directly
affected consequences. Neither requires a fixed report or an extra approval round.
For requirements, follow the [requirements review protocol](references/requirements.md#review-requirements).
It checks objective support, necessity, meaning, decision logic and comprehensibility for humans
and agents. Apply its checks to the requested scope, not as a mandatory full audit for validation.
Use [consistency comparison](../../shared/principles.md#compare-related-representations) within that scope.
"Validate consistency" checks supplied requirements and domain models through this existing operation;
it does not require a current edit or authorise repairs.

### Return the result

Return the artifact or assessment, material unresolved findings with actionable context,
what can proceed and whether user action is needed now. Preserve accepted IDs and baselines.
For a lead handoff, include the current sources and status, the affected work and proof,
and any limits on the next activity through the execution-handoff guidance above.
Return delegated questions to the active lead; ask directly when invoked standalone. Do not
start another coordinator, invent technical decisions or claim acceptance without authority.
