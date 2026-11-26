<a id="model-requirements"></a>
# Model requirements and domain meaning

Use this guidance during Draft and substantive Revise to select and include useful models from
the requirements and domain structure. Settled rules can need a model as much as ambiguous ones.
For Review and Validate, assess the adequacy of existing representations without editing. Read
the shared sections and selected techniques; do not apply every technique to every document. Requirements
own intended outcomes and domain models own business meaning. Technical topology, database
schemas and API contracts remain with design-solution.

## Interpret the request

Use ordinary language, not a required parameter form. Infer the subject, objective, scope and
operation from the request and governing sources. These examples illustrate distinct permissions:

| Request | Action |
| --- | --- |
| "Draft or substantively revise these requirements." | Select and include views that explain the covered business paths, decisions, lifecycles, concepts, timing or context relationships, within scope. |
| "Model these requirements throughout." | Select and add useful views across the document; replace overlapping notation where appropriate. |
| "Model the outcome rules." | Select suitable techniques for that concern only. |
| "Draw the context map for these domain models." | Supply a diagram of the relevant meaning boundaries and relationships. |
| "Suggest where context mapping would help." | Recommend views without creating a map. |
| "Draw the business flow, including unsuccessful outcomes." | Supply an activity diagram; do not substitute prose or a table alone. |
| "Suggest where modelling would help." | Recommend views and locations without generating or inserting them. |
| "Review the models against the requirements." | Assess meaning, omissions and consistency without editing. |
| "Validate the decision table for overlapping rules." | Check that property and directly affected consequences without editing. |
| "Update the models for these changes." | Revise affected views and check their immediate dependencies. |

An explicit request may name a technique or describe its recognisable output and takes precedence
over default selection. Mentioning a diagram in quoted source material alone does not select one.
A general requirements review stays read-only, including in chat; it can use examples and small
tables to explain findings. Modelling does not authorise implementation or accept new business rules.

## Choose a technique for the question

Inspect the covered behavior and domain relationships in the priority order below. Resolve
foundational meaning before models that depend on it. Raise a concern's priority when its risk
or uncertainty dominates the change. This is an order of attention, not a fixed authoring sequence
or a required diagram set. Settled rules still need useful representations. During assessment,
use the same triggers to identify missing coverage.

| Priority | Material requirements or domain content | Required explanatory coverage |
| --- | --- | --- |
| 1 | Concepts whose identity, meaning, relationships or cardinalities affect the rules | Conceptual domain model with definitions and relevant relationship constraints. Reuse adequate domain models; do not substitute database tables. |
| 2 | Permitted actions or event effects depend on a subject's lifecycle state | [Statechart](#state-transitions) with events, guards and effects for each distinct lifecycle. A status word alone does not trigger one. |
| 3 | Combinations of conditions determine permitted or required outcomes | Decision table with explicit inputs, outcomes and matching semantics, supported by domain rules and invariants. A simple isolated rule, such as eligibility at age 18, can use a boundary example. |
| 4 | Scope, external responsibilities, information restrictions or meanings differ across boundaries | System context for the system boundary and external participants; context map for meaning boundaries and translations. Use a responsibility matrix where role distinctions need it. These views answer different questions. |
| 5 | Business paths, ordering, branches or handoffs determine whether an outcome is reached | Outcome-oriented business flowchart, including material alternative and unsuccessful paths. |
| 6 | Externally observable exchanges, acknowledgements or ordering constrain participants | Black-box interaction sequence with relevant conditions and responses. Specify observable obligations without inventing internal components. |
| Supporting | Event timing or a time boundary determines an outcome | Precise time constraints and a revealing timeline. |
| Supporting | Necessary, alternative or shared results contribute to a larger outcome | Contribution graph with explicit grouping, distinguished from execution order. |
| Supporting | Obligations must be followed into particular output revisions or observations | A small traceability matrix when those relationships are material to the requested understanding. |

When a trigger applies, include the corresponding coverage or reuse an adequate representation.
One representation may answer several questions; several may be necessary for distinct questions.
Explain a material omission or substitution in the existing operation notes or result: identify
where equivalent coverage exists, the scope exclusion or the unresolved decision. Brevity alone
does not justify leaving material meaning unexplained. Simple rules need no omission checklist.

Use only the relevant technique guidance below. Select all materially distinct necessary views,
then remove redundant ones; do not limit selection to one view when several explain different rules.
Honour explicit diagram requests rather than substituting a table. Keep accepted meaning, observed
facts and proposed business choices distinct. Include selected views and revealing cases in their
owning document or chat result within the operation's scope. Use the existing reconciliation and
independent-review workflow for proposed revisions, without adding a separate modelling review gate.

## Select views and resolve necessary meaning first

Establish what the reader must understand or decide to achieve the stated objective. Select
the smallest set of views that explains that meaning within the requested scope. Base selection
on the structure of the requirements, not solely on unresolved questions or a user naming a
technique. Include multiple views when each explains a materially distinct concern; omit an empty
bundle or redundant diagrams for simple rules. Honour explicit format limits and requested views
without requiring another confirmation round.

Check consequential relationships as well as individual subjects. Use a revealing case to see
whether the selected views explain alternatives, shared results, handoffs and corrections,
revision-sensitive uses or the effects of changing only part of the scope, where relevant.
Having a concept diagram and a lifecycle view does not establish that those relationships are
understandable. Add or refine a view only for a material question the existing views do not answer.

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
case, options and recommendation. Wait for the required decision before publishing a settled model
of the affected meaning. A provisional representation may contrast clearly labelled alternatives
or assumptions to expose the choice, within the requested output and operation. Do not select a
default, turn unknown into false or prohibited, or present provisional guards as accepted rules.
Continue independent models whose meaning does not depend on the decision. Report factual
investigation limits separately; do not ask the user for facts
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

For contribution graphs, distinguish necessary results from alternatives and identify shared
children only when their outcome and criteria are the same. State what arrows and groupings
mean; contribution is not execution order or automatic proof of parent achievement. For material
traceability, relate the governing obligation to the identified output revision and relevant
observation. Expose a missing or stale link rather than treating artifact existence as proof.
Reference existing technical contracts where needed; do not design them to fill the matrix.

### Activities

Use a business flowchart or activity diagram when material business paths, ordering or handoffs
need that view, or for an explicitly requested business flow. Give each view one clear process
question and a consistent level of detail. Name the activity, actors, starting conditions and
observable end outcomes. Keep subordinate checks in their owning activity unless their branches
change the outcome shown here. Use concise action labels and explicit decision questions.
A "validate" or "process" box must not hide the rule that selects an outcome.
For example, distinguish "evidence missing" leading to "request evidence" from "evidence complete"
leading to the eligibility decision, when those paths are supported by the sources.

Include supported failure, incomplete work and retry paths when they affect the objective.
Distinguish returning one case's result from stopping a wider activity. Show loops only where
rules permit repeated work, with a change or progress condition and an exit. Distinguish a wait
for an identified input or decision from a plan that needs correction. Name handoffs and the next
responsible role, including upstream correction where relevant. Explain iteration and joins;
state whether a join waits for all paths or any one.
Do not make an arrow labelled "for each" imply an unspecified loop or parallel execution.
Show concurrency only where needed. An illustrative path must not impose a mandatory sequence;
name material omissions and point to the rules that cover them.

Check that material paths are reachable, branches lead to supported outcomes, and guards
distinguish alternatives and cover the relevant cases. Keep activities, conditions, states and
domain relationships consistent with their owning definitions. Expose consequential overlaps or
missing paths through the decision guidance above. Business responsibilities do not establish
component or deployment boundaries.

### State transitions

Before formalising a lifecycle, identify its subject and the question the view answers. Establish
which assessments, conditions, execution controls and reasons for ending vary independently of
that lifecycle. Keep those dimensions and other subjects' lifecycles separate unless their
interaction needs a combined view; retain the rules that connect them. A distinction belongs in
a state when it explains state-dependent behaviour or obligations; otherwise consider an attribute,
assessment, guard or completion reason. This does not prescribe particular states or make every
cancellation a code.

Use concise, conventional state names; identify the subject in the title and put triggering
events and guards on transitions. Make observable effects clear. Keep detailed explanations
beside the chart rather than in state labels.
Distinguish a state from an event or activity. For example,
"awaiting evidence" is a state, "evidence received" is an event, and "assess eligibility" is
an activity. Capture source-supported invariants and unresolved meaning separately. An invariant
must express a governing obligation, not merely restate the labels chosen for the model.
Check required transitions against accepted rules and revealing scenarios. Inspect consequential
missing transitions, repeated events and terminal-state behaviour where relevant. An omitted
transition does not establish prohibition. A diagram can still omit a required action, so syntax and rendering checks do not replace
this source-fidelity check.

When event effects depend on the subject's state, include a state-transition view during Draft
or substantive Revise without waiting for a diagram request. Supply editable Mermaid
`stateDiagram-v2` source when a diagram is selected. Preserve supported events, guards, effects
and revealing lifecycle scenarios. Use composite states, concurrent regions or choice states only when they express supported lifecycle behavior. Review guards, effects and terminal
behavior against the governing sources. Mermaid is the state-machine notation for this public
skill; it does not invoke pstack, TLA+ or another formal checker. Report syntax, rendering and
viewer checks separately without claiming exhaustive verification.

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

Before removing, replacing or simplifying a view, identify the question it answered and where
that coverage will remain. Update affected relationships when responsibilities or rules change.
A valid new view does not justify losing a different material question from the old one. Preserve
useful coverage or report the specific gap; an unresolved decision may need a provisional view.

## Verify and report

The author and independent reviewer first inspect the sources for material concepts, lifecycles,
conditions, boundaries and paths. Independently identify the coverage those concerns require before
judging the supplied models. Compare against the selection triggers, including adequate reused
views and material omissions. Keep the rationale in existing working notes or review findings;
no separate coverage report or review stage is required. Review and Validate retain their scope.

Then check the supplied models against governing sources and representative cases from the objective.
They must neither add unsupported behaviour nor omit behaviour necessary to their stated purpose.
Check shared concept identities and definitions, decision outcomes and transition guards, flow
outcomes and lifecycle effects, and contextual responsibilities and permitted information where
they describe the same concern. Different views need consistent meaning, not identical elements.
Apply the technique-specific checks above. Scenarios and acceptance examples exercise the models;
a few successful examples do not establish completeness.
Use the shared [comparison procedure](../../../shared/principles.md#compare-related-representations)
to select relevant relationships, reuse valid evidence and report the examined scope. Keep the
technique-specific criteria here; do not add a separate model review pass.

Keep editable source. Prefer repository-supported Mermaid for diagrams and Markdown for tables
and constraints unless the user requests another supported format. Follow the repository or user
convention for inline Mermaid and separate sources. Rendering for inspection does not require
retaining generated images in the document set; keep exports when the requested deliverable needs
them. Preserve required rendering checks even when their outputs are temporary. Describe Mermaid
class and flow diagrams as UML-style views where appropriate; do not claim full UML conformance.
Do not install a renderer or add dependencies merely to model. No external skill is required.

Report these checks separately:

- Semantic fidelity and the cases or decision combinations examined, with coverage limits.
- Syntax validity of the exact final embedded diagram source or table expressions.
- Rendering and visual inspection for readable labels, clipping, overlap and traceable connectors.
- Target-viewer compatibility, if checked in the intended publication environment.

Repeat affected checks after changes. A successful render does not prove meaning or target-viewer
compatibility. If tools are unavailable, report unperformed checks without treating settled
meaning as incomplete. Explicitly requested rendered output remains unmet until supplied.
Formal verification and executable decision engines are outside these preparation skills.

Return the created or revised views, locations and material gaps, or read-only findings for
Review and Validate. State what was checked and what remains unverified. Do not claim full
requirements coverage or general agent reliability from a few examples or syntactic validity.
