# Architectural decisions

Use repository ADR conventions. Before allocating ADR identities, establish the question the
approver must decide and the credible alternatives. Group commitments that jointly establish
one choice under that question. A component, technology role or individual obligation does not
automatically need its own ADR. Keep independently decidable choices separate when their
alternatives, scope or acceptance can vary independently. Follow existing repository granularity.

A direct Draft can record an already settled choice without reopening option analysis. When a choice is unsettled, frame the question, supported criteria,
credible alternatives, evidence and tradeoffs. Recommend without accepting. Persist detailed
assessment only when useful, linked to the ADR rather than copied into it.

Read [artifact conventions](../../../shared/artifacts.md) for ADR identity and immutable
decision history. Revise an unaccepted proposal under its existing ID. When replacing an
accepted ADR, preserve retained commitments in the replacement or cite another continuing
authority. A citation to the superseded record alone does not keep its rules governing.
Preserve the supporting assessment version used at acceptance through repository history.

An ADR may cite architecture to identify its affected scope and a design or prototype as
evidence considered for the decision. Distinguish that historical evidence from a governing
dependency. Later implementation does not rewrite the accepted rationale. Architecture may
cite the ADR's governing choice without reissuing it. Implementing designs own their references
to that choice. The ADR need not maintain an implementing-document list. Genuine changes to
the accepted decision still follow replacement and supersession above.

## Recover an earlier decision

Retrospective drafting separates evidence of adoption from evidence of why it happened.
Preserve attributable historical reasoning and label supported reconstruction. Leave undocumented
rationale and excluded alternatives unknown. An implementation feature is not proof of a historical
selection criterion. For example, a dependency's use establishes adoption, not that it was chosen
for performance. Do not reopen option analysis or invent verification obligations to fill those gaps.
A decision now to retain or replace it is a present decision, with its own rationale and acceptance.
Do not backdate that decision or treat adoption as approval. Existing accepted ADRs still follow
the replacement rules above.

## Choose which rules belong in a present proposal

Use this procedure when proposing a new or changed governing decision, including
a present decision to retain an existing approach. Historical recovery preserves the supported
record and its gaps under the guidance above. It need not satisfy a new proposal's admission criteria.

Write one independently assessable obligation per statement. Inspect its existing authority in
requirements, domain definitions, ADRs, designs, API contracts, plans and policy. Cite an
accepted owner rather than independently reissuing its rule. If explicitly replacing that
authority, identify the replacement and required approval instead of claiming it is new.

| What a statement decides | Normal owner |
| --- | --- |
| Required user-visible outcome | Requirements |
| Business meaning, identity, grain or lifecycle meaning | Domain definition |
| Authority for a named result | ADR, result authority |
| Component ownership, dependency direction or trust boundary | ADR, component boundary |
| System-wide operating model or architectural consistency guarantee | ADR, operating model |
| Foundational technology and its role | ADR, technology role |
| Algorithm, representation, persistence, transition or recovery mechanism | Technical design |
| HTTP operation, wire schema, status, error or compatibility detail | API contract |
| Delivery order, migration execution, readiness gate or completion proof | Plan or runbook |

Before including a rule in Decision, establish:

- Its ADR category, selected property and scope of the affected result or system.
- A concrete excluded alternative.
- Why it belongs to the same approval decision as the other rules.
- Whether it is new or inherited, with the owner of any inherited rule.

If these cannot be established, leave the rule unresolved or route it to its owner.
Do not put it in Decision by default.

For Draft and substantive Revise, record where each proposed obligation belongs in working
output or the operation result. Include the statement, existing authority, classification,
architectural choice, excluded alternative and destination. A short note suffices for one
obvious choice. This adds no ADR section or approval gate. Validate checks the reasoning
against actual rules and sources. It may reconstruct the evidence without requiring a retained table.

After classifying a rule, test its relationship to the architectural choice:

- If the rule could change while the complete choice, role, scope and outcome remain intact,
  route that independent concern to its owner.
- If omitting the rule could defeat the requested architectural outcome while other rules hold,
  retain the necessary commitment. Route its replaceable mechanism to the appropriate owner.

Clarify an apparent conflict rather than broadening the choice. Testing whether a technology
could be substituted helps this analysis, but does not prove a rule is non-architectural.

Keep the smallest sufficient set of rules, without prescribing a count. Do not combine
independent decisions into one long rule or split one coherent choice merely to give each
commitment its own record. Importance, security, reliability, cross-cutting
reach, change cost or verifiability alone do not admit an obligation into an ADR.

## The whole ADR

Requirements are supported solution-independent selection criteria, not nearby workflow
policy. Decision establishes the admitted choice. Justification connects evidence to criteria.
Consequences explain benefits, costs and follow-up. They do not issue unrelated authority.
Verification states what observation would prove each admitted Decision commitment and when
checking is needed. This may be once, on a relevant change, before release, during the governed
operation, or at a stated review event or interval. Use governing policy where one exists.
Otherwise justify the proposed timing from the commitment and how it could be violated.
A shared check can cover several commitments when its coverage is clear. No new ID scheme or
table is required. One successful check does not discharge a continuing verification obligation.

Verification must not invent Decision commitments. Implementation guidance cannot smuggle a
removed rule back in. Test paths, commands and verification owners belong in execution records.
Architectural ownership and governed applicability paths may be part of the decision itself.

For technology decisions, verify that the selected technology actually performs its stated
role, not only that a manifest names it. Additional behavioral checks must prove an admitted
architectural constraint. Completeness accounts for inherited constraints through their
continuing owners. Do not copy surrounding requirements into Decision or Verification.

## Boundary examples

- Selecting a PDF parser for local conversion can preserve the local-execution commitment.
  It does not decide admission policy, parser-result fields, plugin settings or provider ownership.
- Selecting complete-old-or-complete-new atomic publication can be an operating-model decision.
  Staging names, compare-and-swap, checkpoint fields and retry commands remain design or execution.
- Selecting an authentication authority or API versioning strategy can be architectural.
  Individual routes, schemas and error bodies belong in the API contract.
- Selecting a provider's evidence as authority for a scoped result can be architectural.
  Exact predicates, unknown handling and timestamps remain domain/design concerns. The ADR
  cannot grant contractual rights or silently claim authority for another business result.
