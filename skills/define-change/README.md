# Use define-change to establish behaviour and business meaning

Use `define-change` when you need to explain what a change should achieve and what its business
concepts mean. Start with a problem, examples, policies, existing documents, or an existing system.
You do not need a complete specification or glossary before you begin.

The skill can produce a requirements brief, a domain model, requested models, or an assessment.
Choose the result needed by the next decision or task. Use [SKILL.md](SKILL.md) for the agent's
instructions, or invoke `$define-change` after installation.

Supported models include conceptual class models, activity diagrams, decision tables, timelines,
and responsibility matrices. Mermaid diagrams and Markdown tables provide editable source.
See [Supported models and Mermaid diagrams](#supported-models-and-mermaid-diagrams) for examples.

## Keep the request short

Name the operation and business subject. Identify the relevant sources if the agent does not
already have them. The skill covers terminology, exceptions, acceptance examples, and distinctions
between accepted rules, observations, and proposals. Ask for modelling when you need visual or
tabular views; the skill can choose suitable models and notation. Name a separate domain model or
particular diagram when you require that output. Reviews are read-only by default.

## Choose a task

Use the skill for work such as:

- Define the required behaviour of a new feature, including exceptions and acceptance examples.
- Explain domain concepts, terminology, identity, relationships, events, and business rules.
- Recover requirements and domain meaning from code while distinguishing observations from intended behaviour.
- Review requirements for gaps, conflicting rules, unclear conditions, or outcomes that do not achieve the objective.
- Revise requirements after an accepted policy change while preserving unaffected obligations and identities.
- Establish what a business term or measure means before an investigation or experiment relies on it.

If the business behaviour is settled and you need components, interfaces, algorithms, or storage
choices, use `design-solution`. For implementation under settled requirements and design, use
your chosen implementation workflow. You do not need to run every skill in sequence.

## Supply the problem and relevant sources

Give the agent enough context to investigate:

- State the problem, affected people, desired outcome, and exclusions.
- Supply relevant policies, examples, existing requirements, domain definitions, and implementation access.
- Identify which sources govern the work and which contain proposals or observations.
- Specify whether to draft, revise, review, or validate. Name the files or concerns the agent may change.
- Set decision boundaries, practical limits, and any required format or models.

If you can provide only a problem and a few examples, ask the agent to identify the missing
information. It should inspect available sources before asking you for facts already recorded there.

## Define requirements for a change

For example:

> $define-change Define cancellation requirements from this policy and code.

Expect a brief that explains the outcome, scope, required behaviour, material constraints, and
acceptance examples. Relevant quality needs can include privacy, accessibility, performance, or
recovery. The agent should derive them from the activity and evidence rather than invent targets.

Ask for examples that distinguish success from failure. A user story or Given/When/Then scenario
can help, but the governing rule must remain clear. Written acceptance examples are not evidence
that executable checks exist or have passed. See the [requirements guidance](references/requirements.md).

## Develop a domain model

For example:

> $define-change Model return requests, items, and refunds. Include a conceptual diagram.

Expect an explanation of the real activity before a list of fields or names. The model can address
which objects are distinct, what one record or quantity represents, and which rules must always hold.
Aggregates can help identify related changes that must remain consistent.

For contextual differences, the skill examines local meanings, decision ownership, translations and
permitted information. To inspect those relationships visually, ask it to draw the context map.
A different term, department or service does not automatically establish a new bounded context.
Domain boundaries do not prescribe services, databases or deployment units. See the
[context guidance](references/domain-meaning.md#contexts-and-relationships).

## Recover or assess existing material

To recover an existing system's behaviour, try:

> $define-change Recover cancellation rules from this system. Compare them with this policy.

Ask for supporting code or execution references and clear inspection limits. A dependency, status
name, or existing validation rule does not establish why it was introduced or whether it is required.
See the [existing-system guidance](references/existing-systems.md).

For a general review, ask the agent to assess whether the requirements achieve the objective and
can be interpreted consistently. For a bounded validation, name the property, such as overlapping
eligibility rules or preserved time boundaries. Both operations remain read-only unless you request edits.

## Supported models and Mermaid diagrams

When you ask for modelling, the skill selects the smallest useful set of views for your question.
You do not need to choose diagram types. A broad "model this" starts with one useful view;
a request to model the requirements throughout can produce several. Naming a specific model
makes that output a required deliverable. A general review does not request a model bundle.

The supported views include:

| Business question | Suitable model |
| --- | --- |
| How do domain meanings and decisions relate across contexts? | Context map |
| What business concepts exist, and how do they relate? | UML-style conceptual class model. |
| What happens, who acts, and where can work branch or fail? | Activity diagram. |
| Which conditions determine a result? | DMN-style decision table with explicit rule-matching behaviour. |
| Which events, intervals, or deadlines affect the result? | Timeline or temporal constraints. |
| Who performs an activity, supplies information, or makes a decision? | Responsibility matrix. |

Mermaid diagrams are supported, with editable source: use class diagrams for concepts and
relationships, and flowcharts for activities. Decision tables, responsibility matrices, and
precise time constraints can use Markdown. These views explain business meaning; they do not
require full UML or executable DMN notation.

For model selection by the skill:

> $define-change Model these requirements using appropriate diagrams and tables.

To require a particular view or format:

> $define-change Draw this business flow in Mermaid.

> $define-change Add a conceptual class diagram in Mermaid.

You can ask in ordinary language, such as "Draw the business flow, including incomplete cases."
The skill chooses routine notation. Requested models are deliverables, while an ordinary review
does not request a model bundle. Ask for editable source and separate checks of meaning, syntax,
and rendering. See the [modelling guidance](references/models.md).

## Work autonomously and assess the result

State which choices the agent may make. Routine investigation can proceed within that scope.
New governing content remains proposed unless you approve it or explicitly delegate acceptance.
A consequential unresolved choice blocks only the work that depends on it. Ask the agent to
continue independent work and explain what would settle the remaining choice.

Before relying on the result, check that you can explain the intended outcome, terms, applicable
rules, and exceptions. Compare representative examples with the supplied sources. Check that the
result distinguishes accepted rules, observations, assumptions, and proposals.

For a handoff, request the governing source revisions, unresolved decisions, affected work, and
verification expectations. Requirements describe what must hold. Technical designs and execution
records carry that meaning into mechanisms and actual checks. See the
[shared principles](../../shared/principles.md) and [handoff guidance](../../shared/execution-handoff.md).
