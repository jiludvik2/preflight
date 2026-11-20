# Working principles

Preflight helps establish what a change should do and how it should work. Use the smallest
set of explanations, decisions and contracts that lets the next person act correctly.
Do not turn a small change into a document production exercise.

## Writing skills

Apply the local [writing guidance](writing.md) when authoring or reviewing prose, requirements,
domain models, architecture, designs, contracts and inquiry results. It is available within this
package and requires no separate writing skill. Preserve repository formats, meaning, permission
boundaries and evidence limits. Writing review adds no document or approval round.

## Investigate disputed premises

For a disputed factual premise that could change a consequential decision, inspect existing sources
and use permitted read-only research tools. No particular search service, browser, provider or helper
skill is required. Never install a service or disclose private evidence merely to fill a source gap.
State the disputed claim, compare credible explanations, and seek evidence that could support or
refute them. Apply the [evidence guidance](#proof-proportional-to-the-claim). Keep unsupported claims
unresolved and explain which conclusions depend on them. Continue independent preparation without
inventing facts or treating missing evidence as acceptance.

## Meaning and authority

Start from the problem, concrete activities and the intended outcome. Distinguish product
users, document readers and people authorized to make business decisions. They need not
be the same people or known in advance.

Inspect project instructions, relevant requirements, domain definitions, decisions,
architecture, designs, contracts and implementation. Establish which sources govern the
affected scope, including their status and exclusions. A citation is not proof of coverage.
Resolve conflicts against authority, not whichever source is newest or easiest to implement.

Keep observed behavior, intended behavior, a proposal and an accepted commitment distinct.
Implementation evidence does not grant product or design authority. Match claims to the
[evidence guidance](#proof-proportional-to-the-claim). An outcome clarification does not approve
the technical choices needed to realize it. Never infer acceptance from a review, implementation
or downstream use.

New governing artifacts and substantive changes require explicit human approval before
acceptance, unless the user has explicitly delegated acceptance for that scope. Permission
to work autonomously, draft, revise or implement does not itself delegate acceptance.
Respect the delegation's limits and repository approval requirements. Without approval or
applicable delegation, keep the result proposed. Independent preparation work may continue.

Put each obligation in its owning artifact:

- Requirements own required outcomes.
- Domain definitions own business meaning.
- ADRs own architectural choices.
- Designs and API contracts own technical behavior.
- Execution plans own delivery order and proof.

Cite inherited obligations rather than issuing them again. Preserve repository conventions
and accepted identities.

## Useful explanations

Explain what a central concept does, why it exists, who uses it and which outcome it enables
before its mechanics. Describe the activity before choosing a name. Inspect project usage
and use established practitioner terminology when it fits. A missing glossary is not a
reason to invent one. Necessary engineering terms belong in technical artifacts.

For a material new or renamed term, compare the closest established concept and explain the
substantive distinction that needs a separate name. Otherwise use that term or plain prose.
Check ordinary-looking phrases as well as formal names. Keep contested meaning visible.
Research consequential uncertainty rather than claiming unsupported industry usage.

When passing work to another specialist or an execution lead, carry the concrete activity,
governing terms with their scoped meanings and source links, justified local or proposed
terms, and unresolved meaning questions. Include an explicit reader perspective when known.
Use relevant excerpts and links in the existing task record or operation result, not a
second glossary. Recipients preserve those meanings and distinctions or identify a proposed
change to the owning source. Summaries must not turn tentative terminology into accepted meaning.
If work proceeds despite unsettled wording because other rules settle the affected cases,
carry those rules and their scope. Proceeding does not settle the wording's broader meaning.

Engineering names may differ when their relationship to the domain concept is clear. Check
that mapping rather than requiring identical spelling everywhere. A code or wire name does
not redefine business meaning. Vocabulary alignment alone does not authorize a breaking rename.

Keep domain and design narratives about the subject. Detailed review classifications,
dispatch instructions and execution bookkeeping belong in the existing operation result
or supporting evidence. Do not make a new ledger document solely for this guidance.

## Actions, questions and scope

For each material unresolved finding, explain the concrete uncertainty, evidence, affected
work, next action and what would settle it. Preserve the existing finding classification.
Distinguish a confirmed blocker from unverified risk or a non-blocking improvement. Naming
an owner such as "domain" or "ADR" does not explain the finding. State what can continue.

Separate facts the agent can investigate, missing proposals it can prepare, choices needing
user judgment and settled content awaiting acceptance. Perform authorized investigation and
proposal work before asking a decision question. A genuine question gives context, concrete
alternatives, consequences and a supported recommendation where possible. State whether user
action is needed now. Do not ask the user to perform repository inspection for you.

One lead owns coordination. A delegated specialist returns contextual findings to that lead
and asks the user only if direct interaction was delegated. A standalone specialist reports
and asks directly. Neither starts another coordinator merely to hand off a finding.

Respect the requested operation:

| Operation | Scope and limits |
| --- | --- |
| Draft or Revise | Edit only within the caller's authorized scope. Identifying an artifact as the owner of a finding does not authorize editing it. |
| Review | Apply broad professional judgment. Keep the review read-only. |
| Validate | Check the named properties and directly affected consequences. |

Neither Review nor Validate silently repairs, accepts or expands scope. A request to create
or update an artifact authorizes its ordinary edits. Without permission to persist, return
proposed content and a suggested location. Missing authority blocks the dependent claim.
Useful independent investigation or drafting may continue.

Revisit work when new evidence, changed inputs or a specific unresolved defect warrants it.
Another pass needs a credible investigation or correction, not the same inputs and approach
repeated without progress. Preserve the unresolved finding and what would settle it. Optional
improvements do not keep the requested operation open.

## Upstream changes and return checks

When downstream work needs an upstream change, make the finding above an actionable request.
Identify the owning artifact or concern and its current revision and status where available,
the needed change or question, and the dependent work that cannot proceed. State what result
would settle that dependency. Send the request and relevant source links to the active lead.
The lead dispatches only work within the authorized scope. A read-only review recommends the
next operation rather than starting repairs.

The receiving specialist returns the actual artifact or proposed content, its revision and
acceptance status, what changed in response to the request, and any remaining uncertainty.
If it could not make the change, explain why and what bounded next action would help. A
message saying "done" is not enough. Identify local-only changes that another checkout cannot use.

Before closing the finding, check the returned content against the stated dependency and
current governing sources. The originating specialist performs this check, or the lead does
so with the same downstream context. Recheck the affected contract or claim, not every
completed task. An accepted artifact can still leave the requested issue unresolved. A useful
proposal can settle proposal work without supplying accepted authority for implementation.
Report any remaining gap and its next action rather than treating a response as resolution.

The lead records the result and any changed execution prerequisites or resume point in the
existing task record. Link the changed artifact and recheck evidence rather than copying
its status into competing records. A standalone specialist performs the same return check
and reports directly. Use existing operation output when no task record exists. This does
not require a separate handoff document, fixed form, extra approval or new coordinator.

## Proof proportional to the claim

Code shows implemented logic. Test source shows defined checks, not passing results.
Retained execution output shows observations from that run. Approved documents and authorized
decisions establish intended behavior. A later rerun cannot establish an unrecorded historical
result. Record the inspected revision, relevant local changes, coverage and material limits
where needed to interpret a claim. Partial inspection does not establish whole-system coverage.
Keep useful code and evidence links. Put detail in a short evidence section or existing supporting
record when it would crowd the main document, preserving consequential limits in the explanation.

If implementation contradicts an approved source, record the discrepancy and identify the
correction or authorized decision needed. Do not rewrite the approved source to match code.
Route the finding through the existing upstream-change mechanism. Scope its blocking effect
and continue independent authorized work.

Inspect the actual result. Check meaning against governing evidence, terminology against
applicable usage, and comprehension with a representative scenario. These are different
questions. Agent review is not human practitioner validation.

For affected domain concepts, inspect the resulting documents, contracts and domain-facing
code within the operation's scope. Check for renamed or conflated concepts and lost scope
distinctions against the governing meanings, not merely a claim of consistent vocabulary.
Report material discrepancies through the existing findings and upstream-change mechanism.

Check that each explicit deliverable was supplied, sufficiently reused or left unresolved
for a specific reason. Explain what the result enables for the requested next activity,
which current sources and checks support that conclusion, and what remains unresolved or
unverified with its consequence and next action. A completed review, an accepted document
and permission to implement are separate facts. Useful partial work need not wait for every
dependency. Use the existing operation result, not a new readiness status, form or gate.
References to evidence are better than claims of rigor. Acceptance remains a separate authorized act.
