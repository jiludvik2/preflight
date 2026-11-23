# Requirements

Describe the required outcome independently of a preferred solution. Include the affected
users and activities, observable behavior, material constraints, exclusions and enough
examples to distinguish success from failure. Keep rationale and assumptions distinguishable
from obligations. Avoid a requirement for every existing function or table.

Keep obligations independently verifiable. Separate outcomes that can succeed or fail
independently when that makes their scope and verification clearer. Keep shared conditions
explicit and preserve guarantees that require outcomes to happen together; do not split an
atomic update into unrelated obligations. Sentence count and the word "and" alone do not
determine whether a requirement needs splitting. Preserve accepted identity through the
revision rules below.

Label behavior recovered from code as observed behavior. Inferred intent and acceptance
examples remain proposed unless an approved source or authorized decision supports them.
An observed constraint is not automatically a required constraint.

Work from the supplied problem even if the domain is still being discovered. A local
definition can clarify the brief; move shared business meaning to its domain owner only when
other concerns need it. Link that definition rather than duplicating a domain rulebook.
Functional and quality requirements both need observable meaning; investigate vague terms
such as “fast” or “reliable” only as far as the next decision requires.

Where wording leaves applicability unclear, distinguish a continuing state (while it holds)
from a triggering event (when it occurs), and name the responsible system and required
response. For an invalid or unwanted condition, state what must happen if it occurs.
Refine the existing prose, user stories or Gherkin in place; these distinctions do not add
another format. Resolve material unclear referents, quantities, units and time boundaries
against governing sources. Do not invent a threshold or replace "should" with "must" merely
to make a statement sound precise. Check terminology and readability separately from meaning,
using the existing writing guidance and scoped domain definitions.

For new or materially changed scope, check which cross-cutting needs apply: security and
privacy, accessibility, compliance, performance, reliability, migration and operational
support or recovery. Use the activities, affected users and project evidence to identify
material obligations or unanswered questions. Do not invent targets or policies, require
a questionnaire for every category, or add boilerplate for concerns that do not apply.

Honor requested formats and project conventions. Prose or user stories can explain the
user's purpose and outcome; Gherkin can express concrete conditions, events and observable
results. Formulas with units and worked examples can specify calculations.
During Draft and substantive Revise, use the
[question-to-technique aid](models.md#choose-a-technique-for-the-question) to select and include
representations based on the covered behavior, including settled rules. Use the smallest useful
set in the owning brief or chat result; simple rules can use boundary examples. During Review
and Validate, assess model adequacy and explain findings without editing. Follow
[requirements modelling](models.md) for construction and checks, respecting explicit format and scope limits.
Use only representations that add meaning; do not restate every rule in
several formats or force a user story around a system obligation. API and message schemas belong to
design-solution; reference governing external contracts as constraints rather than designing
them here.

Acceptance examples should expose the important normal case, boundary or failure, including
what the user or external consumer observes. Make the governing rule clear rather than
leaving it to be guessed from selected examples. When using Gherkin, state the relevant
preconditions, event and expected outcome in Given/When/Then steps, without prescribing UI
clicks or implementation mechanics unless those are themselves required behavior.
Preserve governing verification policy when carrying these into design. A requirement says
what must hold; later execution work binds it to commands and test files. Gherkin text alone
does not establish that an executable acceptance test exists or has passed.

Separate missing facts from product choices. For example, whether a clinic's current code
blocks cancellations within 24 hours is inspectable. Whether patients should be allowed to
cancel inside that window is a product decision if no governing policy settles it. Explain
the effects of the alternatives; do not silently turn the current implementation into policy.

If useful, propose independently valuable slices. Do not call every brief an epic or impose
an agile hierarchy. Slicing does not approve scope, determine component boundaries or create
a delivery schedule.

## Durable identity

Use [artifact conventions](../../../shared/artifacts.md) and the repository's existing IDs.
Without a convention, a durable brief is `REQUIREMENTS-NNN` in
`requirements-NNN-<scope>.md`, and its requirements are `REQ-NNN-001`, `REQ-NNN-002`, etc.
Allocate one unique brief number, not a global counter for every individual requirement.
Transient conversation does not need IDs.

Candidate requirement IDs can change before initial acceptance. Acceptance establishes the
brief revision and permanent requirement identities. Thereafter keep an ID when the same
obligation survives clarification. Give a genuinely new or replacement obligation a new
local number. Record replacement, split, merge and withdrawal relationships without recycling
accepted IDs or erasing their history. Presentation order is not identity.

For an accepted brief's substantive revision, keep the accepted file governing and use its
adjacent `.draft.md` or the established review mechanism. A rejected draft never changes the
accepted requirements. Approval of a design or working code is not acceptance of the brief.

## Quality of the result

During drafting, use the objective-support and requirement-boundary checks below as obligations
are formed. Identify each obligation's protected outcome or governing constraint, applicable
conditions and independently observable result. Test overall sufficiency with a revealing case
before elaborating the catalogue. Reuse this analysis in review rather than creating a second
record. A later review does not replace applying these criteria during construction.

Check that the brief conveys what changes, why it matters, what remains outside scope and
what observations would show success. Trace supported obligations to their evidence without
requiring a traceability matrix for routine work. Name affected unknowns rather than calling
the whole brief “not ready.” Preserve enough context for an agent to investigate or prepare
a proposal and for the user to make an actual choice.

For drafting or substantive revision, use the review protocol below on the affected
requirements and their interactions. A meaning-preserving editorial correction does not
require a fresh specification review.

## Review requirements

Assess whether the requirements specify the intended outcomes, provide sufficient and
proportionate obligations, and can be interpreted consistently by humans and agents.
General Review examines the requirements together with their governing rules. Bounded
Validate selects only the requested properties and directly affected consequences.
Keep either operation read-only unless revision is also requested.

### Establish scope and governing intent

Identify the reviewed documents and revisions, affected users and activities, objectives,
constraints and exclusions. Establish intent from the user's instructions and governing
sources independently of the document under review. Keep accepted decisions, proposals,
assumptions and observed behaviour distinguishable. Neither internal consistency nor
matching the current implementation establishes that the document specifies the right outcome.
If sources disagree or the objective is missing, report the affected uncertainty and continue
checks that do not depend on settling it.

### Check objective support, necessity and proportionality

Review in both directions. For each requirement, identify the accepted objective or governing
constraint it protects. Ask what could go wrong if it were removed and whether its applicability
is conditional. Include legal, contractual, integrity and operational obligations even when
they have no directly visible product benefit. Flag unnecessary implementation prescriptions.

For the requirements collectively, ask whether every requirement could be satisfied while
an accepted objective still fails. Use a concrete counterexample to identify the missing
obligation. Conversely, identify obligations that pursue an objective outside the agreed scope
or impose work beyond what the objectives and governing constraints justify.

Distinguish necessary obligations, obligations needed under stated conditions, unknown
justification, and demonstrably unnecessary or disproportionate demands. Missing rationale
is not permission to delete a requirement. Explain the practical burden and the protected
outcome before calling a requirement excessive. Assess relevant quality requirements using
the cross-cutting guidance above, without inventing targets or a questionnaire.

### Check requirement boundaries and identifiers

Identify observable obligations within each requirement, including those embedded in lists,
tables and paragraphs. Do not assume the author's headings, existing IDs or requested edit
location establish suitable boundaries.

Before judging the boundaries, make a short working decomposition of the obligations in the
reviewed scope, including normative tables and unnumbered prose. Associate each obligation
with its owning requirement or source location. Mark missing ownership rather than inventing
it. Compare the verdicts the obligations within each affected requirement or statement could
receive: could one hold while another fails, or could one change without changing the other?
Use a concrete case where that distinction matters. For effects retained together, establish
why their conditions and responses define one required behaviour. Make this decomposition inspectable in the existing review result: give a compact map from
the affected requirements or statements to their obligations and boundary conclusions.
Group simple items where one explanation applies, but keep every reviewed item's coverage
identifiable and material unowned obligations visible. Use this map to check coverage before
reporting the boundary review complete. It is review evidence, not a separate ledger or a
target requirement count.

Where obligations can succeed, fail, be verified or change independently, assess whether they
need separate requirement IDs. Keep conditions, exceptions and jointly necessary guarantees
together where separating them would obscure the required behavior. Do not allocate an ID
mechanically to every sentence or list item.

Before recommending a split, check whether another requirement already owns the obligation.
In proposed corrections, replace duplicated rules with references and give distinct obligations
their own maintained location.
Where the document uses IDs, check that readers can identify each resulting requirement for
verification, reference and later revision. Apply [durable identity](#durable-identity) to additions,
clarifications, splits and replacements. Preserve existing identities, not a fixed total count.

Check that acceptance criteria and examples identify the requirements they verify, including
cases covering several requirements. Use existing IDs where present and otherwise clear section
references. Do not require IDs for every assertion or impose a separate traceability table.
Report bundled obligations, duplicate ownership, ambiguous criterion attribution and affected
references as findings. Briefly identify the boundary coverage and the revealing cases in the
existing review result, including material obligations found outside the numbered statements.
When a plausible split was examined but its effects were retained together, explain the
combined guarantee. A simple obligation needs no invented split analysis. Distinguish mechanical
checks of ID uniqueness and reference integrity
from judgment about suitable boundaries and coverage; an unchanged ID count proves neither.

### Check terms and individual obligations

Inspect terms that affect applicability, decisions or outcomes against the governing glossary
and domain definitions. Identify missing specialist meanings and inconsistent names. Propose
clarifications in the owning location rather than duplicating shared definitions. Ordinary
language needs no extra glossary.

Apply the guidance above to each obligation's actor, object, conditions, required behaviour,
exceptions and observable result. Check quantities, units and time boundaries. Flag circular
criteria, hidden assumptions and unsupported thresholds. Preserve the distinctions between
permission, obligation and prohibition, and between necessary and sufficient conditions.
Do not invent a business decision to make a rule appear precise.

For each outcome-driving rule, identify whether it applies to an individual member, a subset,
or the whole assessed subject. Where scope can change the outcome, test a revealing case with
only part affected. Do not infer an effect on the whole from changes to some members unless
an applicable governing rule establishes that effect. Distinguish an explicit governing
condition from an intended condition supplied by the reviewer. If a missing qualification
permits materially different outcomes, report the decision gap rather than treating it as
optional wording. Do not demand repeated qualifications when governing definitions already
settle the scope unambiguously.

### Check decision completeness against the objective

For each required outcome, trace the inputs, conditions and business decisions needed to reach
it. Apply the checks below where a missing distinction could change that outcome, an obligation
or necessary understanding. Include governing constraints even when they have no visible user benefit.

| Aspect | Required check |
| --- | --- |
| Subjects and relationships | Identify which people or objects a rule concerns and how they relate. Apply the individual, subset and whole-subject check above. Check cardinality where the number of related subjects changes required behaviour. |
| Inputs and evidence | Identify necessary inputs and the required response to missing, ambiguous or contradictory information. |
| Conditions and outcomes | Check whether the conditions distinguish the required outcomes, including exceptions and boundaries. Preserve necessary versus sufficient conditions. |
| Interacting rules | Find reachable cases where several rules apply. If they demand different results, check whether precedence or another resolution rule settles the result. |
| Timing | Where timing changes the result, check the trigger, effective time, relevant ordering and interval boundaries. |
| Responsibilities | Where responsibility affects an obligation or decision, establish who performs the activity, supplies information or decides the result. |
| Failure and incomplete work | Check whether failed, deferred and incomplete processing are distinguished from completed business outcomes where that distinction matters. |
| Overall sufficiency | Test whether all stated requirements could hold while the objective still fails. Show the missing obligation with a concrete case. |

Do not seek completeness beyond the objective and governing constraints. A notation having a
place for a cardinality, actor or deadline does not make that detail necessary. Leave out
irrelevant relationships and elements; do not report their omission as a requirements defect.

Before reporting a gap, inspect governing definitions, linked rules, accepted decisions and
relevant examples. Determine whether they already settle the affected case. If not, construct
a realistic case in which plausible interpretations lead to different outcomes or obligations.
Explain why the difference matters to the objective or a governing constraint. A missing detail
is not automatically a consequential gap. An unresolved factual question needs investigation;
a business choice needs an authorised decision. Neither permits an invented default.

### Check combined logic

Trace the relevant activity from its starting conditions to its required observable outcome.
Check that prerequisites, decisions and exceptions fit together, including truthful reporting
of incomplete or failed processing where relevant. Outcomes must be distinct or exhaustive
where the objective requires those properties, not by an assumed universal rule.

Compare rules that apply to the same actors, objects, states or events, including quantities
and timing. Before reporting a contradiction, check source precedence, applicability and
explicit exceptions. Cite the conflicting statements and describe a reachable case in which
they demand incompatible outcomes under the same conditions. Different outcomes in different
scopes are not a contradiction. For material ambiguity, show plausible interpretations and
a case where the difference changes an obligation or observable result; use the
[domain-rule review guidance](domain-meaning.md#review) for source support and boundary cases.
Check source fidelity even when no outcomes conflict: permission is not an obligation,
and a necessary condition alone does not establish sufficient permission.
An unresolved source conflict remains a finding, not permission to choose a business rule.

Where conditions interact or lifecycle transitions matter, inspect applicable combinations
and outcomes using the [technique selection aid](models.md#choose-a-technique-for-the-question).
Assess whether the representations make those rules understandable. Review and Validate report
inadequate or missing views without editing. During Draft or substantive Revise, selected
state-transition views follow the [statechart route](models.md#state-transitions).
Distinguish missing behavior from deliberate
exclusions, combinations ruled out by governing constraints and behavior explicitly left
unconstrained. An example of each rule does not establish that their overlaps or remaining
cases are covered. Check material boundaries, failures, recovery and concurrent events where
the activity and evidence make them relevant; do not enumerate every imaginable combination.
For a gap, name the uncovered case, its consequence and the missing fact or product decision.
Do not fill it with an assumed default or treat silence as permission or prohibition.

### Test representative cases

Apply the rules to realistic cases and material boundaries, exceptions and combinations.
Use expected outcomes supported by accepted intent or independent governing sources, not
derived solely from the wording being tested. Prefer the smallest case that reveals a defect.
Include missing inputs, conflicting information, failure or recovery when relevant to the
activity. No fixed case count or exhaustive enumeration is required.

### Check readability and independent comprehension

Check meaning separately from wording. Use the shared writing guidance to inspect document
order, concrete subjects, clear referents, dense paragraphs and table cells. Put purpose, scope
and constraints before detail. As reusable domain meaning or substantial examples make obligations
hard to locate, separate them into their existing artifact locations and provide a short reading
route. Carry necessary meanings and cross-cutting constraints into selective reading; a split
does not make them optional. Keep short, self-contained changes together rather than imposing
a file template or word limit. Give each normative rule one maintained owner, linking instead of
duplicating it. Preserve useful summaries and clearly illustrative examples that apply the rule
without changing it.

A reader with the document and its declared references must be able to explain the objective,
determine applicable obligations, and reach a supported result or identify the precise unresolved
fact or choice without the author's conversation history. Where material uncertainty remains,
an optional reader exercise can test this. Provide the necessary inputs without revealing
the expected answer. No particular model or separate agent is required for every review.

### Report findings and limits

Use the existing findings mechanism rather than imposing another report format. For each
material finding, identify its location, defect or uncertainty, concrete consequence, affected
objective or constraint, and bounded proposed correction. For a consequential decision gap,
state what the sources establish, what remains undecided, and the concrete case exposing the
difference. Present available corrections, their consequences and a recommendation. Identify
which subsequent work depends on resolution and which can proceed independently. State whether
resolution needs research, clarification or an authorised product decision. Prioritise by effect on outcomes
and distinguish demonstrated defects, unsupported assumptions and editorial judgments.

State what was examined and what remains unverified. Do not claim completeness or absence
of contradictions from a few examples, a language check or passing tests. If revision follows,
recheck changed rules and their interactions against the revealing cases. After substantive expansion,
also recheck affected requirement boundaries, IDs and acceptance references against their existing
owners. Approval of content or its location does not waive this check. Review or rewriting
does not accept new requirements or authorise implementation.
