# Unified component catalogue

Base: `6ed73cf3a0e9aca68af1b8f5f3a52e61db06ac70`.

The 41 technical base parts and 279 sourcing components now form one authoritative
`data/components.json.components[]` list of 287 records. The 33 explicitly linked
pairs are merged, eight unmatched technical definitions are retained, and 246
sourcing-only components retain their combined physical scope. No combined supplied
item was split. `data/sourcing.json` now owns supplier programmes only.

## Identifiers and relationships

Existing technical `part.*` IDs are preserved. Linked `bompart.part.*` IDs resolve
to those identities. Sourcing-only IDs use the same `part.*` namespace, with host
context retained in the suffix. The registry holds 279 exact historical aliases;
new source data, assembly lines and component-keyed cost inputs use canonical IDs.
The Navigator uses the aliases before existing retired-record redirects.

Both technical and hardware in-memory views expose the same `components` list.
Consumers no longer join two representations through component `catalog_ref`.
Product/offer mapping and cost-product `catalog_ref` fields are unrelated joins and
remain. Assemblies, software editions, bundles and computers were not redesigned.

Explicit `bom_role` distinguishes 279 material leaves, four assembled components,
and four specification-only records. Cost input generation iterates materials only.
Assembly lines must reference a material or an explicit assembly; this prevents a
composed RAM module being accidentally counted as a new purchased leaf.

## Reconciled fields

- Keep the technical names for the shared Aurelia video controller, Artemis buffered
  controller and AION 4164 2 µm revision; retain the sourcing labels in `alternate_names`.
- Store identical manufacturing/sourcing requirements once under `requirements`.
- Artemis graphics: retain the newer 16×4116, 2×2114, FIFO/cache and qualification
  requirements. Replace the older unclear 16 KiB statement with a compatible external
  bus/arbitration, scan/font-path, output and package qualification requirement.
- Brimar CRT and Mono Pro controller: consolidate duplicate generic requirements into
  one statement preserving pending sourcing, drawing, production qualification and
  the distinction between planning allowance and confirmed cost.
- Keep source-only requirements, candidate manufacturers, all seven nonempty ordering
  codes, meaningful unknown manufacturers and unresolved qualification statuses.
- Vendor and manufacturer remain separate fields. Historical date precision and
  explicit `no release` states are preserved.

The four all-null quote placeholders (`unit_cost`, `currency`, `quote_date`,
`quantity_tier`) are removed. Empty manufacturer part numbers and empty requirements/
usage lists are omitted. The all-null nested timing/refresh/ordering-code fields are
removed; absent values mean unspecified. The component schema no longer has mandatory
null-only quote properties. Tests that previously indexed empty placeholders now
check unspecified semantics. No fictional quote or timing value was introduced.

## Saved economics

No financial model was rebuilt, and all saved model and baseline bytes are unchanged.
Python and JavaScript readers translate archived IDs, map keys and compound keys
in memory. Exact collisions fail rather than overwrite values. Translation is
idempotent and changes no numbers. Both readers retain original provenance metadata.
Archived HTML reports retain their embedded historical model snapshots.

The browser's misleading always-Unknown supplier-unit-cost fallback is replaced by
an explicit statement that quotations are not recorded. Saved engineering estimates
remain in Manufacturing costs. Cost input builders and investment aggregation now
use canonical IDs without constructing a second `bompart.*` identity.

## Validation

- `python tools/validate_data.py`: strict component schema, role boundaries,
  alias targets, canonical references and assembly integrity.
- `python tests/validate_component_migration.py` / `python tools/check_migration.py`:
  287 identities, unchanged physical assembly data, 23 other logical views unchanged
  after ID translation, saved model/baseline byte equality and numerical invariance.
- Browser tests cover component list membership, merged specification/sourcing
  details, archival cost assumptions, old links, configurations and reader parity.
- Python tests cover RAM arithmetic, offer mappings, release dates, cost archive
  integrity and rejection of invalid source writes.

Existing unrelated baseline failures are retained, not bypassed: the atlas test
expects a pricing link absent from the timeline navigation; older domain validators
also have stale financial provenance/domain expectations documented in
`SINGLE_DATA_MIGRATION.md`. No checks are removed to make those baseline failures pass.

Reviewed page snapshots change only on Aurelia, Artemis and BOM Navigator: canonical
part IDs/names replace sourcing labels, source-only material components can now be
selected as fitted Aurelia parts, and merged Details omit empty placeholders. Table
and link counts are unchanged. One Artemis part link now includes its exact anchor.
