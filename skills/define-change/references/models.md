<a id="model-requirements"></a>
# Model requirements and domain meaning

Use this guidance for requested models and visualisations of requirements or domain meaning. Read the shared sections
and the selected techniques below; do not apply every technique to every document. Requirements
own intended outcomes and domain models own business meaning. Technical topology, database
schemas and API contracts remain with design-solution.

## Interpret the request

Use ordinary language, not a required parameter form. Infer the subject, objective, scope and
operation from the request and governing sources. These examples illustrate distinct permissions:

| Request | Action |
| --- | --- |
| "Model these requirements throughout." | Select and add useful views across the document; replace overlapping notation where appropriate. |
| "Model the outcome rules." | Select suitable techniques for that concern only. |
| "Draw the context map for these domain models." | Supply a diagram of the relevant meaning boundaries and relationships. |
| "Suggest where context mapping would help." | Recommend views without creating a map. |
| "Draw the business flow, including unsuccessful outcomes." | Supply an activity diagram; do not substitute prose or a table alone. |
| "Suggest where modelling would help." | Recommend views and locations without generating or inserting them. |
| "Review the models against the requirements." | Assess meaning, omissions and consistency without editing. |
| "Validate the decision table for overlapping rules." | Check that property and directly affected consequences without editing. |
| "Update the models for these changes." | Revise affected views and check their immediate dependencies. |

An explicit request may name a technique or describe its recognisable output. Mentioning a
diagram in quoted source material is not an instruction to create one. A general requirements
review does not request a model bundle, even in chat. It can still use examples and small tables
to explain findings. Modelling does not authorise implementation or accept new business rules.

## Select views and resolve necessary meaning first

Establish what the reader must understand or decide to achieve the stated objective. Select
the smallest set of views that explains that meaning within the requested scope. A request to
model a document throughout permits several useful views, not every technique by default.
For a broad "model this" with no further scope, start with one useful view. Honour explicitly
requested views without requiring another confirmation round.

Before creating models, check source support and necessary business decisions for the selected
scope. For requirements views, apply [decision-completeness checks](requirements.md#check-decision-completeness-against-the-objective).
For domain views, apply [domain semantic checks](domain-meaning.md#review), including context analysis
where relevant. Do not require a requirements brief or requirement IDs for a domain map. Use the
existing `domain` task for domain judgment through [model assignments](../../../shared/model-selection.md).
A prior review does not waive this focused check; a separate full review is not a prerequisite. Resolve information available in governing
sources first. Simplify the proposed view and omit detail that does not support the objective
or a governing constraint. Do not ask the user to define an irrelevant cardinality or deadline.

For a remaining consequential business decision, use the existing
[findings guidance](../../../shared/principles.md#actions-questions-and-scope) to explain the gap, contrasting
case, options and recommendation. Present it to the user before creating the affected models,
and wait for the required decision. Do not leave an unexplained question mark, choose a default
or turn an assumption into a rule. Continue independent models whose meaning does not depend
on the decision. Report factual investigation limits separately; do not ask the user for facts
available in the project. Route delegated questions through the active lead.

## Apply the selected techniques

### Context maps

Apply [context analysis](domain-meaning.md#contexts-and-relationships) before representing the
relationships. Show each relevant context's purpose and meaning scope, with links to local
definitions. Show supplying and consuming contexts and explain what each relationship means.
Distinguish information flow, semantic dependency and decision ownership where their directions
or participants differ. Label arrows or use a legend rather than making one unlabeled arrow
imply all three.

Include material translations, information restrictions, lost distinctions and shared agreements
beside their relationships or in linked explanations. Preserve source, proposed status and scope.
Do not duplicate detailed local rules or invent relationships to complete a diagram.

An explicit request to draw a context map requires a diagram. Use the existing supported Mermaid
and verification guidance below. A domain context map does not select software components, storage,
transport or deployment. A C4 system-context view does not substitute for its semantic relationships.

### Concepts and relationships

Show the business concepts needed to explain the decision, using UML-style conceptual class
notation or a repository-supported equivalent. Reuse governing terms and distinguish identity,
membership and association. Name relationships and their direction where it carries meaning.
Include supported cardinalities where they affect interpretation; omit irrelevant detail.

Check that concepts have a domain meaning independent of storage and that relationships preserve
their actual scope. Do not infer a whole-subject effect from a change to a subset. A conceptual
class does not prescribe a software class, table, foreign key or service.

### Activities

Identify the business activity, relevant actors, starting conditions and observable outcomes.
Show the necessary steps, decision guards and handoffs. Include exceptions, failure and
incomplete processing where they affect the objective. Distinguish returning one case's result
from stopping a wider activity; show loops only where the rules permit repeated work.

Check that branches lead to supported outcomes, material paths are reachable, and guards
distinguish alternatives. Resolve consequential overlaps or missing paths before drawing the
affected flow. Business responsibilities do not establish component or deployment boundaries.

### Decisions and coverage

Define the decision question, inputs, their meanings and possible values, and outputs. For
DMN-style tables, state how matching rows determine results through a supported hit policy.
For example, Unique permits at most one matching rule; require coverage of all applicable
inputs only where the objective requires a result for each. Do not invent precedence from row
order. Define symbols such as a wildcard and distinguish unknown facts from false conditions.

Check reachable overlaps, uncovered combinations, boundaries and excluded cases against the
governing rules. Enumerate finite combinations where tractable; otherwise explain the coverage
examined and its limits. Check that derived input qualifications preserve their source facts
and do not hide the decision inside unexplained labels. A case example for every row does not
prove that overlaps or remaining cases are covered. A Markdown table described as DMN-style
does not establish executable Decision Model and Notation conformance.

### Time constraints and timelines

Identify the events or states being ordered, relevant reference clock or timezone, precision,
durations and interval boundaries. State inclusive or exclusive limits where they affect a
result. Distinguish effective time from publication, observation and retrieval time. Distinguish
an event's uncertain date bounds from an effect lasting throughout that period.

Express necessary constraints precisely and use timeline examples for revealing boundaries
or event sequences. Check before, at and after a material boundary and same-time ordering
where relevant. Preserve date-only or uncertain precision; do not invent timestamps, durations
or thresholds. Illustration dates do not become requirements.

### Responsibilities

Use a matrix where it clarifies who performs an activity, supplies information or makes a
decision. Name the roles and the scope of each responsibility. Distinguish reporting a decision
from making it, and supplying evidence from deciding its meaning, where those differences matter.

Check necessary responsibilities for omissions, conflicts and unsupported assignments. Do not
force RACI categories, one accountable person, or technical ownership without a governing rule.

## Integrate without duplicating rules

Place each view beside the rules it explains or in the established owning domain document.
Keep requirement identities and terminology stable. State whether a view illustrates rules
maintained elsewhere or owns the rule under the repository's conventions. An explanatory view
does not amend accepted prose; a normative table can replace overlapping prose when that
revision is authorised. Preserve one maintained location for each obligation and link it from
other views. Follow [artifact conventions](../../../shared/artifacts.md) for accepted baselines.

Keep necessary context, but replace redundant notation and summaries rather than stacking
equivalent descriptions. Reconcile discrepancies with surrounding text and affected models;
do not silently let the new representation override governing meaning.

## Verify and report

Check the selected models against governing sources and representative cases from the objective.
They must neither add unsupported behaviour nor omit behaviour necessary to their stated purpose.
Apply the technique-specific checks above and check consistency across affected views.

Keep editable source. Prefer repository-supported Mermaid for diagrams and Markdown for tables
and constraints unless the user requests another supported format. Describe Mermaid class and
flow diagrams as UML-style views where appropriate; do not claim full UML conformance.
Do not install a renderer, add dependencies or require formal verification merely to model.

Report these checks separately:

- Semantic fidelity and the cases or decision combinations examined, with coverage limits.
- Syntax validity of the exact final embedded diagram source or table expressions.
- Rendering and visual inspection for readable labels, clipping, overlap and traceable connectors.
- Target-viewer compatibility, if checked in the intended publication environment.

Repeat affected checks after changes. A successful render does not prove meaning or target-viewer
compatibility. If tools are unavailable, report unperformed checks without treating settled
meaning as incomplete. Explicitly requested rendered output remains unmet until supplied.
Solver checks, executable decision engines and formal verification require a separate request.

Return the created or revised views, locations and material gaps, or read-only findings for
Review and Validate. State what was checked and what remains unverified. Do not claim full
requirements coverage or general agent reliability from a few examples or syntactic validity.
