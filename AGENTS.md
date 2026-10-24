# Repository editing instructions

Read `JSON_DATA_STANDARD.md` before changing JSON, models, schemas or page loaders.
Edit the 21 authoritative collections under `data/` directly, including `data/site.json`
for UI configuration. There is no catalogue generation step or per-record manifest.
Preserve stable IDs, unknowns and historical date precision. Do not split combined
components just to identify suppliers. Run `python tools/validate_data.py` and
`python tests/validate_data_structure.py`, plus relevant domain/page tests.
Read `BUILD_PIPELINE.md` before numerical rebuilds. Do not recalculate financial
models for structural edits. Frozen baselines are immutable. Existing baseline
failures are documented in `SINGLE_DATA_MIGRATION.md`; do not remove checks.

Components live only in `data/components.json.components[]`. Preserve unified IDs,
BOM roles and the archival alias adapter. Read `COMPONENT_MIGRATION.md` before
changing component contracts. Run `tests/validate_component_migration.py` for this
migration, in addition to source validation and relevant browser/domain tests.

Device BOM definitions live in `data/devices.json`. Read
`DEVICE_BOM_MIGRATION.md` before changing BOM ownership or assembly references.
Run `tests/validate_device_migration.py` and relevant browser tests.

For chassis, slots, processor bins, RAM devices and physical media ownership, read
[CHASSIS_DEVICE_MIGRATION.md](CHASSIS_DEVICE_MIGRATION.md). Run
`python tests/validate_chassis_migration.py` after structural hardware changes.

For commercial products and computer projections read PRODUCT_CATALOG_MIGRATION.md.
Run tests/validate_product_catalog.py. Node is required by the shared Python/JS
projection. Do not recreate retired source collections or infer products from cost rows.
