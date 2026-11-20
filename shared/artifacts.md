# Artifacts and accepted baselines

Follow the repository's locations, identities and lifecycle. Do not rename a collection to
impose these defaults. Create only artifacts that the requested change needs. A concise
answer or one document may be sufficient. Link existing authority instead of copying it.

## Purpose and maintenance

An as-built document describes implementation at an identified revision and scope. A governing
document states approved requirements, meanings or decisions. A proposal contains changes
awaiting acceptance. State the purpose in ordinary prose or the repository's existing conventions.
Descriptions, indexes, evidence records and diagrams do not need front matter. A diagram embedded
in a governing document uses the containing document's lifecycle, without separate metadata.
The purpose distinction adds no status values. Reviewing an as-built description
for accuracy does not approve its contents as future constraints. Keep existing identities and
acceptance evidence. Do not relabel an accepted commitment as descriptive to bypass a change decision.

Reuse an existing as-built document when it covers the requested scope. Keep small observations
in explicitly non-governing sections. For a larger recovery, create a separate description when
its scope, authority or maintenance lifecycle differs from the governing document. Use an existing
supporting record for extensive recovery evidence where possible. Do not require an as-built
counterpart or implementation-notes document for every artifact.

Distinguish a maintained description from a historical snapshot. Review a maintained description
when relevant implementation or scope changes, and check its baseline before relying on it as
current. Update its inspected revision and affected observations under the existing edit authority.
A snapshot describes its recorded revision. Later implementation changes do not update it.
Check its applicability when reusing it, and preserve the original when recording a correction
or a later snapshot. Accuracy corrections follow the descriptive record's maintenance convention,
not acceptance of new governing obligations. Preserve accepted and historical baselines.

Use the shared [evidence guidance](principles.md#proof-proportional-to-the-claim) for inspection
coverage, provenance and limits. The acceptance lifecycle below applies to governing artifacts
and proposals. A descriptive record follows its existing review convention without acquiring
governing authority.

## Locations and identities

When there is no convention, use these locations:

| Content | Default location and identity |
| --- | --- |
| Durable requirements brief | `docs/requirements/requirements-NNN-<concern>.md`, `REQUIREMENTS-NNN` |
| Domain overview and shared glossary | `docs/domain/README.md`, `docs/domain/glossary.md` |
| Scoped domain meaning and rules | `docs/domain/models/<concern>.md` |
| Cross-model business workflow | `docs/domain/workflows/<business-process>.md` |
| Domain supporting record | `docs/domain/supporting/<record-type>-<scope>.md` |
| Architecture overview and component map | `docs/architecture/architecture-NNN[-<scope>].md`, `ARCH-NNN` |
| Architectural decision | `docs/decisions/adr-NNN-<decision-scope>.md`, `ADR-NNN` |
| Supporting decision assessment, if needed | `docs/decision-support/adr-NNN-<description>.<extension>` |
| Technical design | `docs/designs/design-NNN-<concern>.md`, `DESIGN-NNN` |
| API contract family | `docs/apis/api-NNN-<api-name>/`, `API-NNN` |
| Outcome roadmap | `docs/roadmaps/roadmap-NNN-<scope>.md`, `ROADMAP-NNN` |
| Execution plan or record | The execution lead's established location and convention |

An overview provides orientation and links. A scoped domain model owns its concepts,
relationships, business rules and examples. A glossary provides shared terms and points to
those owners, not a second rulebook. Requirement-local terms stay local unless shared usage
justifies promotion. Shared domain views use names such as `context-map.md` and
`ecosystem-map.md` at the domain root. A context map owns cross-context meaning boundaries,
relationships, translations and agreements, linking to local definitions rather than duplicating
their rules. An ecosystem map describes external participants and business responsibilities.
Use an existing owning section when sufficient; no separate file or document per context is required.
Add a scope suffix only when several shared views are needed.
Do not create empty overview, glossary or evidence files.

Name governing files with lowercase kebab-case concern slugs, except `README.md`. Keep dates,
status, revision numbers and selected solutions out of those slugs. Keep cited paths stable.
Temporary drafts are the explicit exception, not a new artifact identity.

Allocate the next unused identity after inspecting the relevant collection and retained records.
For ADRs, include numbered decision-support files. Assign one writer to allocate IDs within
each namespace. Recheck the ID and destination before creating a file. No collection-wide
registry is needed. Keep accepted IDs stable. Numbering does not express priority or acceptance order.
Preserve external requirement IDs rather than wrapping them in another ID scheme. Domain models need
no numeric IDs merely for sorting. An architecture scope slug does not create a hierarchy.

## Default front matter

Use repository front-matter conventions first. Without an established convention, start new
governing Markdown documents and formal design-amendment records with a YAML mapping between `---`
lines, using the fields below.
Apply these defaults during authorized substantive revisions where needed; do not migrate existing
collections or reformat descriptive material merely to add metadata. Preserve existing acceptance
and identities. Missing historical metadata remains an explicit evidence gap, not a reason to
invent approval or relabel an accepted document as proposed.

Descriptions, indexes, evidence and diagrams are exempt even when their filenames resemble a
governing document. Classify by purpose. A domain overview or glossary that only points to owning
models is an index; a document that owns accepted domain rules is a governing domain model.
Execution plans and records retain the execution lead's conventions.

### Document types and identities

Every covered document requires `type` and `status`. Use these exact `type` values:

| Document | `type` | Additional identity fields |
| --- | --- | --- |
| Requirements brief | `requirements` | `id: REQUIREMENTS-NNN` |
| Governing domain model | `domain-model` | No `id` required; its stable repository-relative path identifies it. |
| Governing business workflow | `domain-workflow` | No `id` required; its stable repository-relative path identifies it. |
| Architecture | `architecture` | `id: ARCH-NNN` |
| Architectural decision | `adr` | `id: ADR-NNN` |
| Technical design | `design` | `id: DESIGN-NNN` |
| API contract companion | `api-contract` | `id: API-NNN`; `contract_paths`, a nonempty list of repository-relative wire-contract paths. |
| Outcome roadmap | `roadmap` | `id: ROADMAP-NNN` |
| Retained design amendment | `design-amendment` | `id: DESIGN-NNN-AMENDMENT-NNN`; `design_id: DESIGN-NNN`; nonempty `affected_scopes` list naming the design sections or contracts changed. |

Identity fields are nonempty strings. Match existing allocated identities; `NNN` denotes the
number, not literal text to copy. A temporary revision draft keeps its governing document's type
and identity. Do not add numeric IDs to domain documents. Keep titles and detailed dependencies
in the body unless repository conventions require them in metadata.

### Fields by lifecycle state

All types except amendments use `proposed`, `accepted` or `superseded`. Amendments use `proposed`,
`rejected` or `incorporated`. These are the existing lifecycle states, not new acceptance steps.

| Situation | Required fields beyond type and identity | Fields to omit |
| --- | --- | --- |
| Initial proposal other than an amendment | `status: proposed` | `revision`, acceptance fields and revision-baseline fields. |
| Proposed substantive revision of a revisioned document | `status: proposed`, `based_on_revision`, `based_on_ref` | `revision`, `accepted_on`, `acceptance_ref`. |
| Accepted revisioned document | `status: accepted`, `revision`, `accepted_on`, `acceptance_ref` | Revision-baseline fields. |
| Accepted ADR | `status: accepted`, `accepted_on`, `acceptance_ref` | `revision` and revision-baseline fields. |
| Superseded document or ADR | `status: superseded`; retain its accepted fields; `superseded_by` or `supersession_reason` | Revision-baseline fields. ADRs still have no `revision`. |
| Proposed or rejected amendment | Its `status`, `based_on_revision`, `based_on_ref` | `revision`, acceptance fields and `incorporated_revision`. Explain rejection in the body. |
| Incorporated amendment | `status: incorporated`, retain its baseline fields, add `incorporated_revision`, `accepted_on`, `acceptance_ref` | `revision`. |

Revisioned documents are requirements, domain models, domain workflows, architecture, designs,
API companions and roadmaps. Their first accepted `revision` is `1`; subsequent accepted revisions
advance once under the lifecycle below. ADR replacement is a new proposal, not a revision draft.
A replacement ADR requires `supersedes` naming the old ADR; omit it for an unrelated new decision.
Other types may use `supersedes` when replacing another identity. A relationship field does not
accept the replacement or supersede the old document by itself.

Use these value formats and conditions:

- `revision`, `based_on_revision` and `incorporated_revision` are positive integers. An incorporated
  amendment's resulting revision must exceed its baseline revision.
- `accepted_on` is the quoted ISO calendar date `"YYYY-MM-DD"` of the applicable acceptance.
- `acceptance_ref` is a nonempty string locating approval or scoped delegation for the exact content.
  Preserve enough context in the body or referenced record to identify that content. Never invent it.
- `based_on_ref` is a resolvable immutable reference to the exact accepted baseline, such as its full
  Git commit ID. A moving branch or an unexplained revision number is insufficient.
- `supersedes` and `superseded_by` are an identity or repository-relative path string, or a nonempty
  list when several documents are involved. Use `supersession_reason`, a nonempty explanatory string,
  when no replacement exists. Keep a superseded document's acceptance date and evidence unchanged.

The tables define required and conditional fields. Omit inapplicable fields rather than use nulls,
empty strings or placeholder values. Additional fields are optional unless repository policy
requires them; add only fields with a concrete use. Unknown historical values must be disclosed,
not guessed to make a header appear complete. YAML validity does not establish acceptance.

### Examples

These headers illustrate the defaults. Replace angle-bracket placeholders with real, resolvable
evidence before use. They are not acceptance records or references to existing project documents.

An initial requirements proposal and an initial domain model need no acceptance fields:

```yaml
---
type: requirements
id: REQUIREMENTS-001
status: proposed
---
```

```yaml
---
type: domain-model
status: proposed
---
```

An accepted design uses the same acceptance fields as the other revisioned document types:

```yaml
---
type: design
id: DESIGN-004
status: accepted
revision: 2
accepted_on: "2026-11-10"
acceptance_ref: "<approval record identifying this exact content>"
---
```

A proposed substantive revision preserves that identity and points to the accepted baseline:

```yaml
---
type: design
id: DESIGN-004
status: proposed
based_on_revision: 2
based_on_ref: "<full commit ID resolving to the accepted baseline>"
---
```

A replacement ADR has a new identity and no revision number:

```yaml
---
type: adr
id: ADR-006
status: proposed
supersedes: ADR-003
---
```

An API companion owns lifecycle metadata; its referenced OpenAPI files keep their wire format:

```yaml
---
type: api-contract
id: API-001
status: proposed
contract_paths:
  - docs/apis/api-001-orders/openapi.yaml
---
```

An incorporated amendment retains its baseline and identifies the resulting accepted revision:

```yaml
---
type: design-amendment
id: DESIGN-004-AMENDMENT-002
design_id: DESIGN-004
status: incorporated
based_on_revision: 2
based_on_ref: "<full commit ID resolving to the accepted baseline>"
affected_scopes:
  - Retry recovery
incorporated_revision: 3
accepted_on: "2026-11-10"
acceptance_ref: "<approval record identifying the incorporated change>"
---
```

Before completing an affected Draft or Revise, check the header against both tables and the
acceptance evidence. Check identity, conditional fields and baseline/result consistency, not just
YAML syntax. Review stays read-only; validation does not approve the document or manufacture evidence.

## References and discovery

Record a dependency in the artifact that relies on it, identifying the relevant scope and
governing source. Do not require upstream documents to catalogue downstream designs, tests
or implementations. Creating, revising or completing downstream work does not by itself
require an upstream edit, revision or renewed acceptance. Reassess upstream content when
the work changes or challenges a commitment it owns.

Distinguish governing dependencies, historical evidence and navigation in ordinary wording
where their purpose could be confused. Keep enough local explanation to understand the
artifact and cite the owner of inherited meaning. Mutual links are valid when each commitment
has one owner. Neither document gains authority merely by citing the other. A later-created
document may supply a genuine governing constraint or evidence, not just navigation.

Use stable IDs and paths for discovery. Preserve the particular accepted inputs used for a
decision, review or result in its owning record through revisions or immutable references.
A link to the current file does not establish what governed an earlier result. Existing
overviews may aid navigation without duplicating acceptance, revision or progress state.
Use the [handoff guidance](execution-handoff.md#information-the-lead-needs) to find dependent work.
Do not add a registry, mandatory relationship metadata or reciprocal lists. Preserve explicit
repository traceability requirements, historical citations and the lifecycle links below.
Apply this guidance to relevant work, not a bulk cleanup of existing links.

## Lifecycle

Use the repository's statuses. Otherwise evolving requirements, domain definitions,
architecture overviews, roadmaps, designs and API contract families use `proposed`, `accepted`
and `superseded`. A proposal can be complete enough to review while dependent implementation
still lacks accepted authority. ADRs and amendment records have the exceptions below.

### Record acceptance and editorial corrections

Follow the shared [acceptance authority](principles.md#meaning-and-authority) rule. Initial
acceptance records `revision: 1`, `accepted_on` and `acceptance_ref`. Existing acceptance
evidence identifies the accepted content and the human approval or scoped delegation used.
Applying approval already supplied for that exact content does not require asking again.
Editorial corrections that do not change meaning need no renewed approval and preserve
lifecycle metadata unless local policy differs.

### Prepare a substantive revision

Preserve an identifiable accepted baseline until authorized acceptance:

1. Use the repository's review mechanism. Without one, prepare a non-governing adjacent
   `<stem>.draft.md` for requirements, domain definitions or designs. Do not create a proposal archive.
2. Keep the same identity. Reuse a working copy only for the same authorized revision.
   Do not overwrite another pending proposal.
3. Mark the draft `proposed` with `based_on_revision` and `based_on_ref`, not an accepted `revision`.
   The reference must resolve to the exact accepted body, such as a full Git commit ID.
   Do not use a branch name or an invented history reference.

If the baseline cannot be preserved, continue proposal work but do not overwrite accepted authority.

### Accept a revision

1. Confirm the baseline is current and the exact change is authorized. Rebase and recheck stale proposals.
2. Apply accepted content and acceptance metadata together. Replace the proposal baseline fields
   and advance the revision once.
3. After full incorporation, remove the matching temporary draft unless retention was requested.

For partial acceptance, retain unaccepted changes as a proposal based on the updated accepted baseline.
On retry, finish the same transition without another revision. Keep paused drafts. After rejection
or abandonment, remove only that task's temporary draft and only when authorized.

### Record supersession and check references

Supersession identifies the replacement with `superseded_by`, or explains why none remains.
Acceptance covers only the identified content, not linked documents. Do not assign governing
lifecycle metadata to a pure index or evidence record. Execution records follow the lead's
conventions. Artifact acceptance is not implementation progress.

Recheck affected references and summaries within the edit scope for changes to meaning or
applicability. A changed source revision calls for an impact assessment, not automatic revision
of every citing document. Navigation-only edits preserve lifecycle metadata unless local policy
differs. Updating a reference does not accept the document containing it.

## Artifact-specific exceptions

Accepted ADR decisions are immutable. Editorial corrections preserve the ID, date and status.
A substantive change requires a new proposed ADR with a new ID and `supersedes: ADR-NNN`.
Do not assign ADR revision numbers. The old ADR stays accepted until explicit acceptance of
the replacement. Then accept the replacement and supersede the old record together. Retain
the old record as history. Use `proposed`, `accepted` and `superseded`, not a fallback
`rejected` state. Close an abandoned proposal through the repository's review workflow.

Separate retained design amendments are an alternative used by some repositories. Their
focused proposal, incorporation and historical-evidence behavior is covered in the
design-solution lifecycle reference. Amendment states are `proposed`, `rejected` and
`incorporated`. Neither unincorporated proposals nor historical amendments govern as overlays
on the current accepted contract.

An API family's lifecycle belongs to its owning source or companion, not OpenAPI wire-version
fields. The technical-contracts reference defines the fallback companion and version handling.
