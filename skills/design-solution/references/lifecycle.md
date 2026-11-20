# Design revisions and amendments

Use [artifact conventions](../../../shared/artifacts.md) and the repository's established
workflow. The accepted current design governs its technical scope; implementation still needs
the applicable accepted requirements, domain and architectural authority. Proposal completeness,
review success and acceptance are distinct. A requested outcome does not implicitly authorize
new requirements, architecture or domain rules.

Determine whether the edit changes meaning. Correcting a typo or adding a faithful explanatory
diagram need not change status or revision. A substantive proposal preserves the accepted
baseline through the repository's review mechanism or an adjacent temporary `.draft.md`.
Do not manufacture acceptance evidence or an immutable reference that cannot be resolved.

## When separate amendment records are retained

Do not require retained amendments. When the repository uses them, preserve its convention.
With no established naming convention, keep related files in the same design directory:

```text
design-004-refresh-recovery.md
design-004-z001-amendment-retry-limit.md
design-004-z002-amendment-operator-recovery.md
```

The design is `DESIGN-004`; the second amendment is `DESIGN-004-AMENDMENT-002`. The `z`
only groups filenames alphabetically. Amendment numbers are permanent identities, not
acceptance order. Keep filenames stable; represent proposed, rejected and incorporated
through metadata. Do not rename existing documents or migrate conventions without authority.
Use the shared [amendment front-matter fields](../../../shared/artifacts.md#default-front-matter)
when the repository has no metadata convention.

A proposed amendment identifies the target design, accepted baseline revision and full
immutable reference, affected scopes and proposed change. Its review examines the combined
result: responsibilities, interfaces, invariants, models, failure/recovery behavior and proof
must form a coherent solution after incorporation. Identify overlapping amendments or upstream
decisions; do not leave readers to assemble contradictory overlays.

## Incorporation

Before accepting an amendment, resolve its baseline and confirm it is still current. A stale
baseline needs rebasing and renewed review. Under explicit authority, incorporate only the
accepted normative change into the current design, advance the revision once and record
affected scopes in revision history. In the same change, mark the amendment incorporated
with acceptance evidence and the resulting revision, which must follow its baseline revision.
Update the existing index if one is used.

Validate both records and inspect the design body for actual semantic incorporation. Metadata
alone cannot prove it. Retain the incorporated record as historical evidence, not a governing
overlay or a second current contract. Retries do nothing if both records already reflect the
transition; if interrupted, complete the same transition without another revision increment.
Do not clean up other proposals opportunistically.

## Effect on work already underway

Pass changed obligations and affected evidence to the active implementation lead using
[execution handoff](../../../shared/execution-handoff.md). Preserve valid completed work and
one authoritative execution record. Design prose does not become a competing progress log,
and updating delivery status cannot accept a changed design.
