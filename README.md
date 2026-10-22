# Logix / AION alternative-history atlas

A linked technical, narrative and business specification for the Logix / AION world,
with static HTML explorers and financial reports.

- **Authoring contract:** [JSON_DATA_STANDARD.md](JSON_DATA_STANDARD.md)
- **Build ownership:** [BUILD_PIPELINE.md](BUILD_PIPELINE.md)
- **Migration audit and test results:** [MIGRATION_VALIDATION.md](MIGRATION_VALIDATION.md)
- **Source/projection registry:** [data/manifest.json](data/manifest.json)

Edit authoritative records under `data/` or `site/config/`, then run:

```sh
python tools/data_catalog.py
python tests/validate_data_structure.py
python -m http.server 8000
```

Open `http://localhost:8000/`. Existing HTML page URLs are unchanged. Generated
catalogue views are committed so hosting requires no backend. Financial output
snapshots are preserved under `generated/models/`; rebuilding catalogue views does
not alter prices, sales, forecasts or ROI. Python validation needs `jsonschema`.

For offline file selection, choose the three files in `generated/catalogs/`:
`logix-aion-technical-catalog-v2.json`, `logix-aion-story.json` and `site-pages.json`.

See the standard before adding a record, changing a schema or recalculating models.
