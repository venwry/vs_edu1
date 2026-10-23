# Repository editing instructions

Read `JSON_DATA_STANDARD.md` before changing JSON, models, schemas or page loaders.
Edit the 24 authoritative collections under `data/` directly, including `data/site.json`
for UI configuration. There is no catalogue generation step or per-record manifest.
Preserve stable IDs, unknowns and historical date precision. Do not split combined
components just to identify suppliers. Run `python tools/validate_data.py` and
`python tests/validate_data_structure.py`, plus relevant domain/page tests.
Read `BUILD_PIPELINE.md` before numerical rebuilds. Do not recalculate financial
models for structural edits. Frozen baselines are immutable. Existing baseline
failures are documented in `SINGLE_DATA_MIGRATION.md`; do not remove checks.
