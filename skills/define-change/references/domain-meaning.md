# Domain meaning

Describe the real activity before inventing a model. Ask what objects, events, relationships
and decisions practitioners need, and why. An implemented route, job or status name does not
prove a distinct business operation exists. Would the activity still matter without this
implementation or deployment topology?

Tables, endpoints and services can reveal how concepts are represented; they do not define
the business concepts. Explain the mapping to practitioner activities and rules, distinguishing
observed representations from proposed meanings when governing definitions are absent.

Establish the business rules, identity and grain needed by the current concern. Explain
central concepts through their purpose, participants and a representative scenario before
formal structure. Distinguish adjacent concepts where confusion affects a decision. Use
specialist vocabulary correctly rather than replacing it with vague everyday language.

Inspect project definitions and governing sources. Reuse established terminology where it
fits; lack of a project glossary is not lack of domain knowledge. Local usage is not proof
of industry-standard meaning. Surface a conflict with practitioner usage without silently
overriding accepted project meaning. Investigate consequential contested usage through the
available research workflow; familiar terms do not all need external citations.

Before introducing or renaming a material concept, identify its closest established meaning
and the substantive distinction that requires a separate term. “More precise,” “cross-cutting”
or “existing terms are insufficient” is not evidence of that distinction. Use plain prose
while unresolved, and mark justified project-specific terminology as local or proposed.

Check phrases as well as capitalized names. A model can be internally consistent and readable
yet invent unnecessary categories. For example, explain that a calculation uses prices before
index entry for lookback and after exit for an existing position's returns before deciding
whether this needs a new named concept. In a clinic, “appointment cancellation” need not
become “consumer schedule cessation demand.” These examples do not prescribe universal terms.

Different specialisms may legitimately mean different things by the same word. Establish the
applicable scope, not a universal vocabulary. Keep product users, document readers and business
decision authorities distinct. No preset specialist profile or audience configuration is required.

## Contexts and relationships

A bounded context is a scope within which a particular domain model, its terms and rules apply
consistently. Analyse relevant contexts when material differences in meanings, policies, ownership,
permitted information or translations affect the requested outcome. Always examine restrictions on
information another context may receive. Keep the analysis within the selected concern.

Reuse accepted contexts and explain their business purposes and relevant local meanings. A
terminology or ownership difference prompts analysis, not an automatic split. Distinguish bounded
contexts from aggregates, capabilities, departments, components and services. Do not infer one
from another merely because their current names or boundaries coincide.

For each consequential relationship, establish:

- Which context supplies meaning, which consumes it, and who owns the relevant decisions.
- The direction of dependency and whether the consumer translates, adopts or shares the meaning.
- What information may cross the boundary and which distinctions change or disappear.
- How consumers influence supplied or shared meanings and who participates when those meanings change.

Supplying a fact does not confer ownership of a consumer's derived classification or action.
Test translations with a revealing scenario. If permitted information cannot distinguish states
needed for a decision, identify the missing distinction, affected conclusion and decision needed.
Do not introduce prohibited information or transfer decision ownership to complete the model.
Keep unsupported boundaries and agreements proposed or unresolved, under the existing decision rules.

Record relevant conclusions in the requested result without automatically adding a map or diagram.
For a requested context map, use [modelling guidance](models.md#context-maps). Keep local rules in
their owning models and cross-context relationships in the appropriate shared view. Hand semantic
constraints and unresolved dependencies to design-solution without choosing technical mechanisms.

<a id="model-boundaries"></a>
## Consistency boundaries

Use aggregates and their invariants as candidate consistency boundaries when helpful. Record
what must change together and what can be reconciled later, with uncertainty visible. A domain
boundary does not automatically select a service, database or deployment unit. Hand meaningful
constraints to design-solution rather than designing infrastructure here.

For a domain-facing command, transition or authoritative result, establish purpose and decision
authority independently of current code. Distinguish enduring capabilities from UI actions,
compatibility seams and accidental service boundaries. If unsettled meaning materially changes
the requested outcome or obligation, report the specific missing domain decision before
designing a mechanism that depends on it; continue independent work.

An overview or glossary helps navigation. Scoped domain models own detailed meanings,
relationships, rules and scenarios. Cross-cutting shared terms link to those owners. Keep
consequential domain questions visible in the model; keep detailed review ledgers, dispatch
instructions and execution status in the operation result or existing supporting record.

Use [artifact conventions](../../../shared/artifacts.md) for placement and revisions.
Acceptance of a brief does not amend a linked model or glossary unless that change is also
explicitly accepted. Identify affected rules, scenarios and downstream conclusions. Recheck within scope and return
needed technical or delivery changes to their owner rather than editing them implicitly.

## Review

For material rules introduced, changed or relied on, compare their meaning with the governing
sources. Preserve who may or must do what, the applicable objects and population, conditions,
exceptions, prohibitions, quantities and timing. A necessary condition is not sufficient
permission, and missing applicability evidence does not establish either permission or a
prohibition. When governing wording permits plausible interpretations, distinguish their
source support and test a boundary case allowed by the other governing rules. If those rules
already settle the affected outcomes and obligations, state that scoped conclusion without
selecting a definition or adding a rule. If the interpretations differ materially, or whether
the case is permitted remains uncertain, report the specific uncertainty through the existing
findings mechanism. Failure to find a distinguishing case does not prove none exists. Do not
invent a rule to complete the model or require a separate obligation ledger.

For contextual relationships, check meaning, decision ownership, permitted information and
translation fidelity against the sources and revealing scenarios. Check affected consumers and
shared-change responsibilities when a relationship changes. Preserve the requested review scope.

Check semantics, terminology and comprehension separately. For material new or renamed
concepts, distinguish suitable existing terms, justified local terms, unresolved conflicts
and unnecessary inventions. Record material defects using the existing finding mechanism;
awkward wording alone is not an implementation blocker. A cold reader should be able to
explain the problem, follow a representative scenario and understand the consequences.
