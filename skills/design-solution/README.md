# Use design-solution to make a change implementable

Use `design-solution` when you need architecture, a technical decision, a design, or an interface
contract that an implementer can use. It also supports recovery and review of an existing solution.
Start from the intended outcome, business meaning, constraints, and relevant project evidence.

Request the smallest useful result. You do not need an architecture document, decision record,
and detailed design for every change. Use [SKILL.md](SKILL.md) for the agent's instructions, or
invoke `$design-solution` after installation.

You can request C4 context, component, class, entity-relationship, sequence, activity, and state
models, including editable Mermaid diagrams. See [Supported models and Mermaid diagrams](#supported-models-and-mermaid-diagrams)
for the available views and short prompts. The skill chooses suitable models and notation; you do
not need to select diagram types yourself.

## Keep the request short

Name the change or design question and identify any sources not already clear from context.
The skill covers responsibilities, alternatives, contracts, failures, and verification expectations
where relevant. Name a particular model, format, or constraint when you need it. Reviews are
read-only by default.

## Choose a task

Use the skill for work such as:

- Explain a system's context, component responsibilities, information ownership, and interfaces.
- Compare consequential boundary or technology choices against requirements and constraints.
- Record an architectural decision, its alternatives, rationale, consequences, and scope.
- Define API behaviour, internal contracts, state transitions, failure handling, or recovery.
- Assess compatibility when an interface's representation or meaning changes.
- Recover the architecture and contracts evidenced by an existing implementation.
- Revise an accepted design or assess whether prose, diagrams, and interfaces describe one coherent solution.

If the required business behaviour or a domain term is unsettled, use `define-change` for that
question. If the requirements and design already suffice for implementation, use
your chosen implementation workflow. Routine private code changes do not automatically need new architecture work.

## Supply the outcome and constraints

Provide the sources needed to make and assess the design:

- State the requested result, affected scope, exclusions, and operation. Distinguish authoring from read-only review.
- Supply relevant requirements, domain definitions, architecture, architectural decision records, and interface contracts.
- Identify accepted sources, proposed material, and any decisions already made.
- Provide implementation access, known consumers, operational constraints, and relevant runtime evidence.
- Name any required models, formats, edit limits, or decisions you delegate to the agent.

The agent should reuse settled choices and investigate available evidence. Where missing business
meaning affects a mechanism, it must identify that dependency without inventing a rule. Independent
design work can continue.

## Design architecture without prescribing a style

For example:

> $design-solution Design attendance exports, including a context diagram.

Expect boundaries to follow responsibilities and constraints. Preflight does not prescribe an
architecture style or pattern. A logical component need not have its own process, host, or store.
Domain boundaries inform the design without automatically requiring separate services.

Architecture documents created or revised with the skill include an editable C4 system context
diagram. Other views are selected according to the task. Compare alternatives using the same
representative workflow, including failure and recovery where material. See the
[architecture guidance](references/architecture.md).

## Record an architectural decision

For example:

> $design-solution Draft an ADR comparing these persistence options.

Use an architectural decision record, or ADR, for an architectural choice that needs a durable
record. The skill follows repository conventions and groups commitments around the decision being
made. It does not require an ADR for every component, algorithm, or routine upgrade.

For historical recovery, ask for the evidence supporting the recorded rationale. Existing use of a
technology proves adoption, not why it was selected. See the [decision guidance](references/decisions.md).

## Define or assess a technical contract

For example:

> $design-solution Define the reservation command's contract.

Ask for the required behaviour as well as data shape. For Python interfaces, the guidance normally
uses typed signatures and records for in-process values, JSON Schema for serialized JSON boundaries,
and OpenAPI where appropriate for HTTP. Follow adequate existing project conventions.

For an API revision, request a compatibility assessment against the accepted baseline and known
consumers. Changes in units, meaning, authorization, and error behaviour can matter even when the
schema shape stays unchanged. A proposed breaking change must identify the necessary decision and
consumer impact. See the [contract guidance](references/technical-contracts.md).

## Supported models and Mermaid diagrams

The skill chooses models and routine notation according to the design question and useful level
of detail. Architecture documents include a C4 system context diagram. Other models are added
when they explain an important relationship better than prose. You can ask for appropriate models
without choosing diagram types. Naming a specific model makes that output a required deliverable.

The supported views include:

| Design question | Suitable model |
| --- | --- |
| Who uses the system, and what external systems interact with it? | C4 system context. |
| Which components own responsibilities, and how do they connect? | Component view. |
| Which concepts or entities relate? | Conceptual class or entity-relationship model. |
| Who interacts, and in what order? | Sequence diagram. |
| What steps and branches form the workflow? | Activity diagram. |
| Which transitions are legal, under what conditions? | State machine or transition table. |

Mermaid diagrams are supported, with editable source: C4 context, component flowcharts or C4 views,
class and entity-relationship diagrams, sequence diagrams, activity flowcharts, and state diagrams.
Rendering depends on your tools and viewer, so ask the agent to report any rendering checks it
could not complete.

For model selection by the skill:

> $design-solution Model this design using appropriate Mermaid diagrams.

To require a particular view:

> $design-solution Add a sequence diagram in Mermaid.

> $design-solution Draw this lifecycle as a Mermaid state diagram.

If you require a diagram rather than another representation, say so. A precise state model can
use a table, but a requested state diagram requires a diagram. Keep editable source. Check model meaning, exact-source syntax,
rendering, and viewer compatibility separately. See the [modelling guidance](references/models.md).

## Recover, revise, or review a solution

For recovery, ask the agent to describe what the inspected implementation establishes and identify
unexamined paths. An as-built description does not approve that implementation as the target design.

For a substantive revision, provide the accepted baseline and proposed change. Ask the agent to
check the combined result across responsibilities, contracts, workflows, and models. Preserve the
accepted baseline and history. Apply the repository's revision process or the
[design lifecycle guidance](references/lifecycle.md).

For read-only assessment, try:

> $design-solution Review this design against these requirements and evidence.

Use a bounded validation when you need a named property checked, such as compatibility of one API
change. Neither review nor validation authorizes repairs or accepts a proposal.

## Assess the design before implementation

Check that you can explain the problem, responsibilities, normal flow, and important exceptions.
An implementer should be able to identify inputs, conditions, expected outputs, and unresolved
choices without inventing business behaviour or relying on the original conversation.

Ask for the governing sources and revisions, proposed versus accepted choices, material assumptions,
verification expectations, and next action. Distinguish successful prototype behaviour from an
accepted design or a fully connected production implementation. A valid schema or rendered diagram
alone does not establish semantic correctness.

Work can proceed autonomously within the supplied sources and delegated decisions. New governing
choices remain proposed without approval or explicit delegated acceptance. Reopen only the part
whose decision is genuinely unsettled, while independent work continues. See the
[shared principles](../../shared/principles.md) and [handoff guidance](../../shared/execution-handoff.md).
