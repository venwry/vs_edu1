# Authoritative JSON data standard (v3)

## One source layer

The 24 JSON files immediately under `data/` are the authoritative collections.
Edit their records directly. Each root declares `schema_version: "3.0.0"` and a
relative `$schema` pointing to its contract in `schemas/collections/`.
There are no persisted generated catalogues and no per-record files or manifest.
`data/site.json` owns navigation and page configuration.

Collections group records by domain; file boundaries do not define identity.
Keep existing stable IDs and reference fields. Names are labels, never join keys.
Keep nulls, unknown quantities, units, date precision, supplier attribution and
record order. Do not invent values or split combined supplied components.
Offers, assemblies and product BOM mappings retain their existing meanings.

`schemas/data-registry.json` lists collection files and field ownership for
compatibility views. It contains no record payloads or per-record registrations.
Adding a record to an existing collection requires no registry change. Adding a
collection or moving ownership requires updating the registry and schema together.

## References and contracts

Events are stored once in `data/events.json`. Timeline phases use `event_refs`;
events with contractual terms use `agreement_ref` into `data/contracts.json`.
Other domain records retain existing reference relationships. The validator checks
schemas, technical IDs/references, edition parents, BOM references and positive or
unknown quantities, assembly cycles, agreement references and phase membership.
Domain-specific tests supplement those checks; validation does not prove historical
accuracy, financial consistency or compatibility of every hardware combination.

Use `python tools/validate_data.py` after edits. `tests/validate_data_structure.py`
also validates legacy consumer contracts and frozen baseline integrity.

## Consumers

Browser code uses `DataStore.fetch('catalog:<name>')` (load `data-store.js` first).
The reader fetches authoritative collections and assembles existing consumer shapes
in memory. Existing `generated/catalogs/<name>.json` arguments are virtual aliases,
not network requests or stored files. Reload the page after editing data: collection
responses are cached for the lifetime of the page. Host the repository over HTTP.

Python uses `tools/data_store.py`: `read_document`, `document_text` and
`document_bytes`. Existing file names are accepted as logical aliases. Legacy
serialisation is retained for snapshot provenance checks. To edit through a legacy
view, use `store_document`; it distributes fields to their owners and validates
all proposed collections before writing. New code should edit the grouped source
collections directly, then validate. JSON edits require no build step.

`data/view.html?view=<name>` shows a transient compatibility view and links to its
source collections. Downloads are optional exports, never another source of truth.

## Derived numerical outputs

`generated/models/` contains calculated results, not duplicate source catalogues.
Those results and immutable `baselines/` remain separate because recomputing them
is an intentional numerical operation. Follow `BUILD_PIPELINE.md`; never refresh
saved hashes or models solely to make a structural migration pass.

`python tools/check_migration.py` is the one-time losslessness audit for this
migration. Its fixture hashes deliberately describe the migration base, so it is
not a permanent gate against future intentional data changes.
