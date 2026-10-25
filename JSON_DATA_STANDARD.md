# Authoritative JSON data standard (v3 / unified components)

## One source layer

The 22 JSON files immediately under `data/` are the authoritative collections.
Edit their records directly. Roots declare `schema_version: "3.0.0"` (components, devices and software editions use `"3.3.0"`) and a
relative `$schema` pointing to its contract in `schemas/collections/`.
There are no persisted generated catalogues and no per-record files or manifest.
`data/site.json` owns navigation and page configuration.

Collections group records by domain; file boundaries do not define identity.
Keep existing stable IDs and reference fields. Names are labels, never join keys.
Keep meaningful unknowns, unknown quantities, units, date precision, supplier attribution and
record order. Do not invent values or split combined supplied components.
Offers and product BOM mappings retain their existing meanings. Product BOM targets may be material component IDs as well as assembly/device IDs. Computer assemblies contain devices and parts directly; single-material assembly.part wrappers are retired.

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

`python tools/check_migration.py` is the one-time component-identity migration audit.
Its fixture checks unchanged physical assemblies, other views after identifier
translation, and exact archived model/baseline bytes. It is not a permanent gate
against future intentional data changes. Earlier migration audit fixtures describe
the historical revisions documented in `SINGLE_DATA_MIGRATION.md`.

## Unified component identity

`data/components.json.components[]` is the sole component list. Do not recreate
`base_parts[]` or `data/sourcing.json.components[]`. The technical and hardware
in-memory views both expose this same list as `components`; edits through either
view write to the same source. `data/sourcing.json` retains supplier programmes only.

Each record has one `part.*` ID, name, canonical category, introduction and `bom_role`:
`material` for physical BOM leaves with component-cost inputs, `assembly` for
components represented by constituent assemblies, or `specification` for records
without a released constituent BOM. These roles are not sales availability flags.
Assembly lines point to material IDs or explicit `assembly.*` IDs, never an assembled
component ID that would be ambiguously counted as a leaf.

There is no component `catalog_ref`. Product/offer BOM mappings and cost-product
`catalog_ref` fields retain their separate purpose and remain valid. Keep vendor
and manufacturer distinct. Use `requirements` for reconciled requirements and
`alternate_names` only for meaningful previous names. Empty quote fields and empty
specification placeholders are omitted; absence means unspecified, never zero or
qualified. In particular, no supplier quote should be inferred from saved model costs.

`schemas/data-registry.json.component_id_aliases` maps retired BOM identifiers to
canonical IDs. It is compatibility metadata, not a second component catalogue.
The browser and Python readers translate IDs and component-keyed maps in saved
models in memory, including compound `assembly|component` keys. They reject key
collisions. Raw files, numerical values and original provenance remain unchanged.
Do not manually refresh archival hashes. Old Navigator links resolve through the
same alias map. New data and builder outputs must use canonical IDs.

## Device BOM ownership

Device schema 3.2 stores BOM lines in `bom_assembly_definition` and the remaining
assembly attributes in `bom_assembly_metadata`. Standalone assemblies and device
IDs share the runtime BOM index; resolve references by index membership.
See [DEVICE_BOM_MIGRATION.md](DEVICE_BOM_MIGRATION.md).

For chassis, slots, processor bins, RAM devices and physical media ownership, read
[CHASSIS_DEVICE_MIGRATION.md](CHASSIS_DEVICE_MIGRATION.md). Run
`python tests/validate_chassis_migration.py` after structural hardware changes.

## Commercial source ownership

`data/product-catalog.json` schema 4.0 owns commercial product definitions and
platform identity. Computer specification payloads belong to devices/components/
technologies. See [PRODUCT_CATALOG_MIGRATION.md](PRODUCT_CATALOG_MIGRATION.md).
The former computers/offers/product-boms/retail-catalog files are retired. Their
logical view shapes are read-time projections only. Python catalogue readers now
require Node to execute the same projection used by browser readers.

## Versioned composition ownership

The current source contract uses composition_history on devices and products.
Base-computer platform information lives in devices; external platforms live in
ecosystem-inputs. Retired assemblies have a separate archive. See
COMPOSITION_MIGRATION.md for the shared line contract and compatibility boundary.
Assembly consolidation and temporal calculation are simulation-only in this revision.

The approved follow-up in PRODUCT_COMPLETION.md fills snapshot-derived product
dates/contents and changes device delivery scope. It supersedes the prior missing
product/date counts and unchanged-BOM statement; financial files remain unchanged.

The approved COMPOSITION_RESOLUTION.md follow-up stores bom_assembly_metadata on
composition versions. Transitional assemblies reference metadata_owner_ref and
metadata_version_number; the reader hydrates their former metadata shape. BOM line
units allow each and set: one supplied functional set does not assert one internal IC.

Software delivery migration: SOFTWARE_DELIVERY_MIGRATION.md supersedes the earlier
22-file count and stored software-line ownership. software-editions.json schema 4.0.0
owns software_editions; 14 line groups are derived from consistent edition metadata.
There are 21 authoritative collections. Device/software composition edges share cycle
validation; only physical media/documents enter their BOM leaves, not licence fees.

COMPOSITION_CUTOVER.md supersedes the simulation-only BOM boundary. Current BOM
consumers resolve products/devices/software histories directly. assemblies.json is
empty; retired assemblies are historical only. Version-specific aliases preserve
old identity without supplying a second composition. Historical hardware-BOM exports
remain compatibility views, not current traversal inputs.
