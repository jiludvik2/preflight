# Models and diagrams

Architecture documents require the embedded context diagram in [architecture](architecture.md#system-context).
Other models are discretionary when they explain an important relationship better than prose.
An explicitly requested model is a deliverable even when the agent would not have added it.
Establish its question, scope, semantic model, representation, authority and verification
approach in working reasoning or the existing operation record, not new mandatory metadata.

Distinguish model from diagram. A requested state diagram needs a diagram with meaningful
transitions. A state model can be a precise transition table or formal text if it satisfies
the stated intent and repository conventions. A list of enums is not transition semantics.
Conversation context can establish that a diagram is expected; do not silently substitute a
table. Choose routine notation without asking. Reuse a sufficient authoritative model, explaining
how it serves the request and what local refinement is needed. Linking can suffice for other models.

## Choose the semantic view

Choose the question, useful level of detail and meaning of edges before the notation. Preserve
adequate existing or user-selected notation unless a concrete semantic, readability or supported
rendering limitation requires a change. Agent preference alone is not a reason to redraw.

Conceptual data models describe the subject of the design. Identify the relevant concepts,
relationships and distinctions from the governing problem and requirements. Distinguish this
view from a logical schema, physical storage model or execution-record catalogue. Choose concepts
by their meaning, not their names. Operational records can be domain concepts when operations
are the subject being modelled. Keep implementation details separate when they would obscure
the requested model.

| Question | Suitable view | Default representation |
| --- | --- | --- |
| Who uses the system and which external systems interact with it? | C4 system context | Mermaid C4Context |
| Which internal components own responsibilities and how do they connect? | Component structure | Mermaid flowchart or C4 |
| What types or entities relate? | Class or entity-relationship model | Mermaid classDiagram or erDiagram |
| Who interacts in what order? | Sequence model | Mermaid sequenceDiagram |
| What steps and branches make up a workflow? | Activity/flow model | Mermaid flowchart |
| What transitions are legal? | State machine | Mermaid stateDiagram-v2, or a complete transition table when no diagram is required |

A Mermaid flowchart is a normal option for component structure as well as behavior. For a
structural view, define the roles, boundaries and connector semantics. Keep ownership, invocation,
data transfer and deployment relationships distinguishable. Draw invocation from caller to callee;
include a response only when the return conveys information needed to answer the model's question.
Default to Mermaid C4Context for C4 context views and prefer repository-supported Mermaid for
other diagrams. Keep editable source. Do not introduce
PlantUML, install a renderer or add a dependency merely to use this skill.

Use a fallback from the required C4 context notation only for a concrete compatibility or
rendering limitation. Identify the limitation and use a supported renderable notation with explicit roles, boundaries and
purposeful, directed relationships. A C4 context fallback must preserve C4 context semantics.
Plain-text boxes and connectors are a last resort when no suitable renderable option is available;
a block labeled "C4 system context" alone does not establish compliance. Missing validation tools
do not prove viewer incompatibility. When support is unknown, retain the default editable source
and report unperformed checks. Other views remain conditional; do not require a diagram bundle.

## Align related views

When several views describe the same design, make each view's question, scope and level of
detail clear through its title, labels or nearby prose. Keep shared identities and meanings
consistent. Distinguish a decomposition from views that answer different questions. A component
diagram, sequence diagram and data model need not contain the same nodes or relationships.

In component views, distinguish components, their internal parts, provided operations, stored
data and external systems where confusion would affect understanding. Do not present an internal
adapter as a peer of its owning component without explaining that relationship. An operation
does not need to become a component.

When a view expands a component from another view:

- Identify the expanded component and its boundary.
- Show relevant callers and dependencies outside that boundary, even when they belong to the
  same application or host.
- Connect boundary interactions to the responsible internal parts or operations. Explain how
  detailed names and endpoints map to the parent elements where that mapping is unclear.
  Names may become more specific at the detailed level.
- Check both directions within the views' shared scope. Material parent interactions must
  remain traceable in the detail. Detailed interactions crossing the expanded boundary must
  agree with the parent view's direction and purpose.
- Allow internal interactions to disappear when their endpoints collapse into one parent component.

A focused view may omit unrelated behavior. Explain its scope without excluding interactions
needed to answer its stated question or satisfy the requested deliverable. Resolve unexplained
differences by correcting the views or explaining their actual scope difference. Do not invent
behavior to complete a diagram.

Invocation arrows, data relationships and state transitions express different relationships.
Related views need consistent facts, not identical arrows. Use a short mapping table when names
or aggregation make the relationship difficult to follow. Do not require a mapping register,
a fixed diagram hierarchy, or a detailed diagram for every component.

## Keep connectors traceable

In architecture context and component interaction diagrams, arrange nodes and route connectors
so each relationship is easy to follow from its source to its destination. Avoid overlapping
connector segments and unnecessary crossings. Keep lines clear of unrelated nodes and labels,
and keep relationship labels and arrowheads distinct. Sequence diagrams may need crossings to
show message order; preserve that order.

Use the supported notation's layout controls: adjust direction, node order, spacing, grouping
or label placement. Inspect the rendered result and revise the layout when paths are ambiguous.
If a complex view remains crowded, use focused views with consistent component identities and
explicit scope, retaining the required system context view. Preserve material relationships,
directions and boundaries; do not remove or merge distinct interactions just to simplify routing.
Where crossings cannot reasonably be avoided, minimize them and keep each path traceable.
Report remaining ambiguities and unperformed visual checks.

## Lifecycle completeness

Identify the object or process whose state changes, scope and starting conditions. Describe
states, legal transitions, triggers and applicable guards; terminal behavior when there are
terminals; and relevant interruption, retry, cancellation and recovery. Not every lifecycle
is persisted, ends, or retries. State the important invariants and make forbidden transitions
unambiguous, for example by prohibiting unlisted transitions. Check reachability, dead ends
and consistency where they affect behavior.

Do not put every status-like value in one machine. Distinguish mutable lifecycle state from
immutable attempt outcomes, findings, dispositions, reason codes and derived summaries or
scoped coverage claims. Model separate lifecycles where they exist and define derivation
rules for calculated values. A finding need not become another mutable workflow state.

## Authority and proof

A diagram can explain an authoritative table/prose contract or be normative when explicitly
designated under the repository's conventions. It is not automatically normative. Determine
whether a change alters meaning; an explanatory diagram need not trigger substantive revision.
Changed normative meaning follows the accepted-baseline rules. A requested model does not
authorize inventing behavior to fill a missing governing decision.

Before completing Draft or affected Revise, account for each requested model. Check both
directions: it must not add unsupported behavior, and surrounding contract text must not
contain material lifecycle behavior omitted from it. Name discrepancies precisely. Check
important transitions, guards, failures, recovery and invariants proportionately, not every
possible forbidden pair. Leave only the affected gap unresolved if authority is missing.

Report these checks separately; none proves the others:

- Review semantics against governing sources, including boundaries, roles and purposeful,
  directed relationships. Check [alignment between related views](#align-related-views).
- Validate the syntax of the exact source embedded in the final document, not an earlier draft
  or a separately corrected copy.
- Render that source with an available applicable renderer and visually inspect the output
  for clipping, overlap, readable labels and traceable connectors as described above.
- Check target-viewer compatibility in the intended publication environment. Success in a
  different renderer does not establish compatibility there.

An installed `render-mermaid` skill can supply optional rendering support. Check its supported
notation and capabilities before use; do not assume it handles the selected view. Keep its helper
and dependency management in that package rather than copying them into this skill.

After changing a diagram, repeat the affected checks. If tools or environment access are
unavailable, perform the checks you can and report the rest as unverified. Do not call settled
semantics incomplete solely because rendering is unavailable. Explicitly requested rendered
output remains an unmet deliverable if unavailable. Review remains read-only and Validate
remains bounded. Neither operation accepts artifacts or silently repairs them.
