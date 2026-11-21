# Models and diagrams

During Draft and substantive Revise, select and include the smallest set of models that makes
material technical structure or behavior explicit. Inspect responsibilities, dependencies,
execution paths, data relationships, state-dependent behavior, interacting conditions, runtime
placement and timing. Settled rules still select useful views; ambiguity and a diagram request
are not prerequisites. Include the selected models beside the design content they explain.
Architecture documents also require the embedded context diagram in
[architecture](architecture.md#system-context). Do not create an architecture document merely
to model a small change, or produce every view in the table below.

Explicit scope and format limits prevail. "Suggest where modelling would help" requests
recommendations only. Review and Validate assess adequacy within their read-only scope.
A simple interface can be complete with signatures, semantics and a revealing example.
Select views for material relationships, rather than adding a diagram for every type or step.
Establish each selected view's question, scope, meaning, representation, governing source and
checks in working reasoning or the existing operation record, not new mandatory metadata.

An explicitly requested model remains a deliverable. Distinguish a model from a diagram:
a requested diagram needs meaningful visual relationships, not a list of enums or a prose
substitute. Conversation context can establish that a diagram is expected. Reuse adequate
views and explain their source and any technical refinement. Linking can suffice except for
the required embedded architecture context. Complete each selected, requested or reused view
within its stated scope, or identify the particular output or check that remains unresolved.

## Choose the semantic view

Choose the question, useful level of detail and meaning of edges before the notation. Preserve
adequate existing or user-selected notation unless a concrete semantic, readability or supported
rendering limitation requires a change. Agent preference alone is not a reason to redraw.

Reuse requirements and domain models as the basis for technical realization. Show which
components implement domain actions, which records represent concepts and how technical states
refine business transitions. Preserve meanings, information constraints and decision ownership.
Do not infer one service per domain context or one table per entity. Canonical types or schemas
can supply an adequate data view without a duplicate record diagram or another owning definition.
Distinguish conceptual relationships, logical schema, physical storage and execution records when
those differences matter. Operational records can be domain concepts when operations are the subject.

| Technical content made explicit | Suitable view | Default representation |
| --- | --- | --- |
| System users and external interactions | C4 system context | Mermaid C4Context |
| Component responsibilities, dependencies and interactions | Component structure | Mermaid flowchart with explicit ownership, invocation and data connectors |
| Runtime hosts, processes and isolation | Deployment | Mermaid C4Deployment |
| Call, message or concurrency order between participants | Interaction | Mermaid sequenceDiagram |
| Execution paths, ordering, branches, loops and handoffs | Activity or flow | Mermaid flowchart, including material linear handoffs |
| Concept or data relationships | Class or entity-relationship model | Mermaid classDiagram or erDiagram, or adequate canonical types or schemas |
| State-dependent lifecycle behavior | State machine | Mermaid stateDiagram-v2 or a complete transition table when no diagram is selected |
| Interacting technical conditions and their outcomes | Decision model | Markdown decision table with explicit matching semantics |
| Event timing and temporal constraints | Timing view | Mermaid timeline plus precise constraints in companion text |

For component flowcharts, define roles, boundaries and connector meanings. Distinguish ownership,
invocation and data transfer. Draw invocation from caller to callee; include a response when its
information matters. Hosting nodes are runtime locations, not logical responsibility boundaries.
Use C4Deployment to place runtime instances in hosts or processes and show relevant isolation and
communication. Do not substitute UML deployment or Mermaid architecture-beta as the default.

In sequence views, preserve supported partial order. Use concurrency constructs or separate scoped
scenarios when participants can act independently; vertical position must not invent a total order.
For decision tables, state whether rows are mutually exclusive, first-match in a specified order,
or all-match with defined combination semantics. Expose overlaps, gaps and undecided outcomes.
For timing views, identify event anchors, units, deadlines and relevant inclusivity or clock rules.
A timeline communicates event placement, but its layout does not enforce precise temporal semantics.
Do not claim full UML compliance or UML timing semantics from Mermaid notation.

Keep editable source. These defaults preserve adequate reused views and explicit notation choices
unless a concrete conflict requires a change. Do not introduce a renderer or dependency merely to
follow a notation preference. State models use Mermaid without a formal-checking dependency.

Use a fallback from the required C4 context notation only for a concrete compatibility or
rendering limitation. Identify the limitation and use a supported renderable notation with explicit roles, boundaries and
purposeful, directed relationships. A C4 context fallback must preserve C4 context semantics.
Plain-text boxes and connectors are a last resort when no suitable renderable option is available;
a block labeled "C4 system context" alone does not establish compliance. Missing validation tools
do not prove viewer incompatibility. When support is unknown, retain the default editable source
and report unperformed checks. Other views remain conditional on material technical content;
do not require a diagram bundle.

## Align related views

Use the shared [comparison procedure](../../../shared/principles.md#compare-related-representations)
to select relevant relationships and report scope, evidence and limits. Apply the technical
alignment criteria below within the existing authoring or review work.

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

For C4 context and deployment views, inspect the rendered layout for connectors crossing unrelated
boxes or labels, coincident line segments, line crossings and ambiguous arrowheads. Prioritise
keeping connectors clear of unrelated boxes and labels, then reduce shared segments and crossings.
When defects remain, compare alternative element declaration orders and row arrangements while
preserving the actual boundaries. Use supported `UpdateLayoutConfig` controls and relationship-label
offsets through `UpdateRelStyle` where the renderer provides them. Do not assume C4 supports
PlantUML's `Lay_*` positioning commands or arbitrary node coordinates.

Choose the clearest rendered arrangement, rather than accepting the first generated layout.
Recheck the exact final embedded source after changes. Do not delete relationships, reverse arrows
or invent boundaries to improve routing. If crossings remain unavoidable or tooling prevents visual
inspection, report the specific limitation instead of claiming that overlap has been eliminated.

## Lifecycle completeness

Identify the object or process whose state changes, scope and starting conditions. Describe
states, legal transitions, triggers and applicable guards; terminal behavior when there are
terminals; and relevant interruption, retry, cancellation and recovery. Not every lifecycle
is persisted, ends, or retries. Trace required, missing, repeatable and terminal transitions to
sources and distinguish explicit prohibitions from unknown transitions. Omission is not a
prohibition unless a justified, explicitly closed transition contract
makes it one. Check reachability, dead ends and source-supported invariants where consequential.

Do not put every status-like value in one machine. Distinguish mutable lifecycle state from
immutable attempt outcomes, findings, dispositions, reason codes and derived summaries or
scoped coverage claims. Model separate lifecycles where they exist and define derivation
rules for calculated values. A finding need not become another mutable workflow state.

When state-dependent behavior is material, select a lifecycle view during Draft or substantive
Revise. Preserve governing rules, scenarios, technical assumptions, unknown choices and permission
limits. Use editable Mermaid stateDiagram-v2 source for a selected diagram. A complete transition
table can suffice when no diagram is required. Use composite states, concurrent regions or choice states when supported behavior needs them. Review events, guards, effects and terminal
behavior against governing sources. This public skill does not invoke pstack, TLA+ or another formal
checker. Keep source fidelity, diagram syntax, rendering and implementation correctness distinct.
Model independent settled behavior while keeping provisional alternatives and unknown rules explicit.

## Authority and proof

A diagram can explain an authoritative table/prose contract or be normative when explicitly
designated under the repository's conventions. It is not automatically normative. Determine
whether a change alters meaning; an explanatory diagram need not trigger substantive revision.
Changed normative meaning follows the accepted-baseline rules. A requested model does not
authorize inventing behavior to fill a missing governing decision.

Before completing Draft or affected Revise, account for each selected, requested and reused view.
Check both directions: it must not add unsupported behavior, and surrounding contract text must not
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
