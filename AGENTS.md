# Repository editing instructions

Read `JSON_DATA_STANDARD.md` before changing JSON, models, schemas or page loaders.
Author data under `data/` and UI configuration under `site/config/`. Do not edit
`generated/catalogs/` directly; run `python tools/data_catalog.py` and commit its
views with source changes. Preserve stable IDs, unknowns and historical date precision.
Do not recalculate financial models merely to reorganise data. Read
`BUILD_PIPELINE.md` before numerical rebuilds. Frozen baselines are immutable.
Run `tests/validate_data_structure.py` and the relevant domain/page tests. Existing
baseline failures are documented in `MIGRATION_VALIDATION.md`; do not remove checks.
