# Independent challenge

For a new Draft or substantive Revise, the lead arranges independent challenge before reporting
the preparation complete. Read this procedure before authoring so the reviewer can frame the
concern from sources before seeing the candidate. Keep the owning skill's substantive checks.

## Select the review scope

Review requirements, domain models, architecture, ADRs and technical contracts intended for
acceptance or downstream work, including complete proposals in chat. A revision is substantive
when it changes an outcome, meaning, condition, exception, responsibility, architectural choice,
interface, dependency, guarantee or verification obligation. A one-line semantic change qualifies.

Meaning-preserving editorial edits, exploratory discussion and ordinary explanations are exempt.
Substantive as-built recovery qualifies, with source fidelity and evidence limits as its review
concern. Do not invent alternatives or reopen accepted decisions merely to find a disagreement.
Standalone Review and bounded Validate keep their requested scope and do not recursively delegate.

Review one coherent concern or bundle, not each file separately. In combined requirements and
design work, review requirements before freezing the design baseline. Select a suitable reviewer
for each concern. Related artifacts provide context without becoming additional review targets.

## Assign responsibilities

The existing lead coordinates scope, permissions, dispatch, sequencing, finding assessment and
the final handoff. It may also draft. Reuse an existing delegated author instead of adding another
drafter or controller. The drafter reads the full relevant skill guidance, owns candidate edits,
self-checks and finding dispositions, and returns the actual result to the lead.

The reviewer is a separate fresh context that has not authored or edited the reviewed material.
It frames from sources, challenges read-only and checks corrections. It does not edit, implement,
accept product decisions, lead delivery or spawn reviews of its own findings. Give it the owning
skill's Review operation and relevant references, rather than another Draft assignment.

Keep one writer per candidate. When authoring is delegated, the lead returns semantic changes to
that drafter. A lead making substantive edits becomes a coauthor whose changes also need review.
Freeze the content while it is under review. Human acceptance and permission to implement remain
separate from reviewer agreement.

## Dispatch through the host

Apply [model assignments](model-selection.md) for the activity, role and complexity. Honor explicit
user assignments first. Check the host's actual model and effort support before dispatch. Do not
silently substitute an unavailable assignment or pretend the active session switched models.
Do not create an extra author solely to match a preset. The same model can draft and review, but
the contexts must be independent. Report material assignment mismatches.

Use native agent creation and continuation, without a debate executable or orchestration service.
For example, Codex uses `spawn_agent` with `fork_turns="none"` and the resolved model and effort.
Retain its identifier for `followup_task`. Other hosts use equivalent fresh-context facilities.
Continue the same eligible reviewer where the active workflow permits reuse. If recreation is
necessary, supply governing sources, prior framing, current content and unresolved findings.
Do not claim context continuity that was lost.

Supply applicable project rules, permissions and exclusions explicitly. Review permits read-only
source inspection within those limits. It does not itself authorize installation, code execution,
additional paid services or disclosure of unrelated private material. Honor separately authorized
checks and execution exclusions. State inaccessible evidence instead of inventing observations.
A path and hash do not establish that the reviewer can read its contents.

## Exchange sources, candidate and corrections

1. The lead gives the reviewer the original request, governing sources and their status/revisions,
   accepted decisions, relevant evidence, exclusions and uncertainties. Withhold the new candidate
   and its persuasive narrative. Preserve governing facts and rationale. Name withheld paths in a
   shared checkout. This is instruction-based withholding, not enforced filesystem isolation.
   The drafter may work concurrently with this source-only framing.

   Ask the reviewer to identify the required outcome, constraints, unresolved decisions and
   concrete ways a superficially satisfactory proposal could fail. Require a short framing note,
   not a replacement specification. Pass useful source questions back to the drafter.

2. The drafter returns a coherent candidate, referenced sources/status, choices and open questions.
   The lead supplies its exact content and bounded review scope to the reviewer. Identify
   uncommitted content as well as the commit when applicable. The reviewer applies the owning
   skill's relevant Review guidance against the sources and independent framing.

   For each material finding, request a location, evidence or revealing case, practical consequence,
   and bounded correction or decision needed. Examine unsupported assumptions, unnecessary
   obligations and material alternatives. State coverage and limits. No score, finding quota,
   mandatory disagreement or replacement proposal is required. The lead passes material findings
   to the drafter without hiding inconvenient concerns.

3. The drafter returns final content and dispositions for every material finding. Mark each as
   corrected with its actual change, rejected with evidence and reasoning, or unresolved with
   affected work and the next action. Use the existing findings mechanism or operation reply.

   The lead assesses disputes against governing sources and evidence. A reviewer preference is
   not a requirement. Do not force consensus or silently decide an open business choice. Preserve
   material disagreement and its dependent consequences in the result.

   If content changed substantively or material dispositions remain unchecked, the lead sends
   the actual final artifact, changes and dispositions for a focused correction check. The reviewer
   checks resolutions, rebuttals and affected interactions, including contradictions or lost obligations from consolidation.
   A drafter's response is not independent confirmation. Unchanged content needs no extra contact
   only when existing review also covers its material dispositions. Later substantive edits reopen
   the affected scope rather than inheriting stale coverage.

## Finish within the review's limits

Default to one source-framing contact, one challenge and a focused correction check when needed.
Further review must name a remaining defect, material correction, changed evidence or user-requested
continuation. Do not repeat full review to obtain agreement or erase unresolved findings by restarting.

Reuse a qualifying existing independent review when it covers current content, governing sources,
material findings and final corrections, and its reviewer did not author the material. Do not
reproduce these contacts retrospectively. Review only uncovered changes or consequences.

If an eligible fresh reviewer, configured model or host capability is unavailable, or the user
prohibits delegation, return useful work explicitly as unreviewed. Do not silently self-certify,
install helpers or add an approval request. Continue independent authorized work. A useful draft
is distinct from independently reviewed completion. Keep any existing required review gate closed.

In the existing operation result, identify the reviewer and actual model, inspected content and
source identity, coverage, limits and outcome. State whether there were no material findings,
corrections checked, open findings or partial coverage, or independent review was unavailable.
Do not add a ledger or readiness certificate. Independent review does not establish acceptance.
