# Technical contracts

Write for a reader who needs to understand and implement one coherent concern. Select only the
applicable views, such as responsibilities, interactions, data, lifecycle, recovery, security and
compatibility. Put each model beside the contract it explains rather than in a detached diagram
gallery. A small interface change can be a short operation description; headings serve the content.

## Compose an implementable contract

Use the [governing terminology and reader context](../SKILL.md#establish-scope-and-authority).
Explain unfamiliar contract concepts and their practical roles before their fields, encodings or
mechanics. Scale the following detail to the contract's consequential behavior, not a fixed outline.

Connect inputs to the decisions they inform, the component responsible for each action, any records
retained and the resulting outputs. Explain what those records mean and how later steps use them.
State normal behavior before exceptions and recovery. Where interpretations could change behavior,
specify the applicable conditions and rule precedence. If an execution limit depends on a count,
define what one unit counts, its scope and when that count advances or resets. Do not invent a
limit or counting rule that the governing sources leave undecided.

Where a design includes a workflow and conceptual model, trace a representative case through
its consequential steps. Make clear which component coordinates or permits the work and which
performs it, which conceptual information the step uses, what information or relationship it
produces or changes, and which later operation or decision uses that output. Explain engineering
aliases such as "case", "context" or "result" where their relationship to the conceptual model
is unclear. Use the existing workflow prose or a short table; do not require a separate mapping
register or CRUD matrix.

At consequential handoffs, distinguish permission, execution, interpretation, state writes and
result delivery. A component heading does not assign every action beneath it to that component.
Check those actions against the responsibility model. When an operation interprets, reconciles
or publishes information, explain its output's meaning and retained basis. Preserve relevant
distinctions between observations, interpreted claims, conclusions, real-world subjects and
published records. Do not impose a fixed interpretation pipeline on unrelated designs.

Apply the walkthrough within the requested scope. A focused workflow need not handle every
conceptual entity, and conceptual models need not include every supporting technical record.

Use an example when it resolves a material ambiguity, such as two conditions applying together or
a recovery step using a retained result. Check that examples, diagrams and prose describe the same
rules and exceptions. An example must not silently establish behavior missing from the contract.
Keep unresolved meanings and decisions explicit with their affected cases. Separate wording-only
improvements from proposed behavioral changes; editing for clarity does not settle an open choice.

## Internal Python contracts

Choose the representation from how the contract is consumed. Reuse an adequate existing definition
and follow the repository's conventions. Apply these defaults when defining or revising a contract:

- For ordinary in-process interfaces, use typed signatures and records. Document semantics,
  invariants and failure behavior in docstrings or existing contract prose. A separate JSON Schema
  is unnecessary when callers exchange Python values through that interface.
- For serialized JSON boundaries, use JSON Schema with concise Markdown describing semantics,
  invariants and failure behavior. This includes model inputs and outputs, subprocess messages,
  and records persisted as JSON for later consumption. Python dictionaries alone do not imply
  serialization. Define the schema alongside the prose rather than deferring it to implementation.
- For HTTP interfaces, follow the [HTTP contract guidance](#http-and-external-contracts).

Give record structure one canonical definition. State which artifact owns it and whether schemas
are generated from owning types, or types and projections are derived from an owning schema.
Generate or verify the other representations against that definition. Keep semantics and behavior
that the structural definition cannot express in the interface's docstrings or companion prose.
Keep fields and structural constraints in their owning definition rather than duplicating them
in prose.

When another representation is appropriate, explain how it serves the actual producer and consumer
and why the default is unnecessary or unsuitable. These defaults do not add an enforcement workflow
or require a standalone document for every Python function.

## Establish execution realization

For consequential execution steps, trace the caller to the actual API, command or process
that performs the action. Identify the inputs, returned or retained results, completion signal
and constraints needed by the next step. Name the owner of invocation and recovery. Detail
only the execution dependencies that affect feasibility or the contract, not every internal call.

Distinguish an instruction package that guides an agent, an adapter that connects interfaces,
and an executable runtime that performs work. A package name or an arrow to a tool does not
establish that the required process exists or runs in the proposed host. Explain the connection
or leave its realization unresolved rather than implying autonomous execution.

Separate documented capability, local availability, tested integration and suitability for the
intended workload and constraints. Inspect relevant entrypoints, manifests, documentation and
retained output. Use bounded permitted checks to resolve consequential uncertainty. A local
command check can establish availability without proving integration or suitability. Do not
introduce a paid call, installation or external mutation as a prerequisite without authorization.
Report the
remaining uncertainty and the smallest permitted check that would resolve it.

## Establish scope and obligations

Trace material behavior to accepted requirements, domain definitions, decisions and architecture.
Keep that mapping in this design or contract, using relevant source IDs, scopes and governing
revisions where needed. A concise explanation can suffice; no reciprocal upstream list or
traceability matrix is required unless repository policy requires one.
For each new persisted structure, cross-component/public interface, transition, trust rule,
aggregation, compatibility or recovery mechanism, establish who owns its meaning and whether
this design is authorized to propose it. Inspect negative scope as well as positive scope.
Plans can schedule such mechanisms but cannot invent them to repair missing design authority.

Define inputs, outputs, invariants, normal behavior and material failure paths precisely
enough to implement without making new product or architecture decisions. Cover concurrency,
idempotency, persistence, recovery and compatibility only where consequential. Do not infer
production automation from prototype code that depended on human judgment. Preserve tested
behavior and provenance or explain intended corrections and transfer obligations.

Check contracts together. Does a producer supply what its consumer needs? Do states and
failure results agree across components? Does the design fit responsibility boundaries and
interface ownership? If not, propose the architectural change in its proper artifact.
Acceptance of a design does not accept an unresolved ADR, domain rule or requirement.

Where interpretation could materially change behavior, establish a discriminating example
from governing requirements or an accepted decision. State its expected meaning and consumer
disposition before treating implementation output as the expected result. Check that legitimate
results, including incomplete results, can be represented truthfully. Distinguish an inadequate
representation from a producer failing to follow an adequate contract. All layers can agree on
the same wrong interpretation; agreement alone does not settle the meaning.

Give each material rule one owner and link its realizations in instructions, types, schemas and
validators. Identify which constraints generation enforces, which later checks enforce, and which
need substantive judgment. A generated schema does not establish semantic correctness. Treat a
downstream transformation that emits replacement records as another producer, even when its input
was valid.

Keep inherited verification policy intact. Define what observations would demonstrate each
material contract, including important negative cases. Preserve any mandated assurance level
or independence instead of replacing it with generic “add tests.” Execution work binds these
obligations to commands, test files and run evidence. Do not invent whole-system obligations
solely to make this design's validation seem complete.

For each material ambiguity, preserve the governing meaning, representative input, expected
interpretation and disposition, affected producer/consumer path, and observation needed to prove
correct handling. Use existing prose or tests; no fixed case count or separate document is required.
Include a relevant distinction or adverse case where it could defeat the intended behavior.
Structural checks and constructed consumer examples do not establish live producer reliability.
Carry untested behavior and unresolved expected results into the handoff as such.

## HTTP and external contracts

Keep wire behavior in the established API contract, using OpenAPI when appropriate. Define
the operation's purpose and authority, request/response shapes, validation, status and public
error semantics, authorization boundary and relevant version/compatibility rules. Show useful
examples without inventing settled domain meaning from an existing endpoint name.

Use [artifact conventions](../../../shared/artifacts.md) for each API family's stable ID and
location. Compatible evolution retains the family ID. Allocate another only for independently
governed authority, ownership, lifecycle or consumers, not merely a new wire version.

Without an established lifecycle mechanism, keep `api-contract.md` beside `openapi.yaml` or
coexisting `openapi-vN.yaml` files. The companion records rationale, contract paths, lifecycle,
accepted revision and evidence, or proposal baseline. Do not duplicate operations and schemas.
Use the shared [API companion front matter](../../../shared/artifacts.md#default-front-matter)
when there is no repository convention.
OpenAPI remains the wire contract, with `info.version` for the published wire version.
Availability such as `planned`, `active`, `deprecated` or `retired` is separate from acceptance.
Describe version coexistence or replacement explicitly when relevant.

When OpenAPI is generated, edit the owning source and follow its publication process. Do not
hand-edit or independently accept generated files, or add custom lifecycle fields to OpenAPI.

For a change to an existing API, compare the affected behavior with its accepted baseline and
known consumer expectations. Explain which changes are compatible, breaking or not yet
established, why, and which consumers are affected or unexamined. Include changes in meaning,
units, errors and authorization, not only wire shape. Record material impact and the needed
disposition in the existing contract rationale or operation result; a short note can suffice.
An uninspected consumer or a passing schema check does not establish compatibility.

Permission to edit, authorization for a compatibility break and acceptance are separate. Keep
an unauthorized break proposed and identify the decision and any migration, deprecation or
versioning work needed before dependent delivery can proceed. Acceptance alone does not
authorize implementation, deployment or migration execution. Editorial changes with no
contract effect do not require a new compatibility assessment.

Reuse repository validators and report unavailable checks rather than installing tools.
Check the composed contract when tooling supports it. Passing syntax checks does not prove
semantic completeness or acceptance.

## Changes and completion

Apply the entrypoint's [revision and comprehension checks](../SKILL.md#draft-or-revise).
Read [lifecycle](lifecycle.md) before changing accepted designs. Examine the resulting combined
design, not only the patch: changed responsibilities, producer/consumer contracts, models,
failure paths and verification obligations must still describe one integrated solution.
An amendment is not complete merely because each added section is individually plausible.

Assess requirements coverage and design coherence separately. Distinguish missing required
behavior from behavior that is supported but insufficiently explained across responsibilities,
workflow and data models.

Follow each changed name, responsibility, owner, hosting choice or interface through affected
current prose, contracts and diagrams. Find dependencies by their relationships as well as names,
including references that do not link back. Compare who calls whom, who owns state, where work
runs and what each interface supplies. A global rename alone cannot correct a missing call or
wrong owner. Update the permitted affected artifacts and repeat the relevant consistency checks.
Preserve historical records and accepted baselines under their lifecycle rules. Report any
out-of-scope dependency, remaining contradiction and responsible owner instead of silently
editing it or claiming closure. In Review, identify these consequences without revising artifacts.

Check every explicit requested output and distinguish a useful proposed contract from
accepted implementation authority. Report missing facts, missing proposals, unresolved
choices and content awaiting acceptance with concrete next actions. Independent work may
continue. A broad Review remains read-only; bounded Validate does not grow into unrelated
contract checks or repairs.
