# Logix / AION alternative-history atlas

A linked technical, narrative and business specification for the Logix / AION world,
with static HTML explorers and financial reports.

- **Authoring contract:** [JSON_DATA_STANDARD.md](JSON_DATA_STANDARD.md)
- **Build ownership:** [BUILD_PIPELINE.md](BUILD_PIPELINE.md)
- **Migration audit and test results:** [SINGLE_DATA_MIGRATION.md](SINGLE_DATA_MIGRATION.md)
- **Unified component migration:** [COMPONENT_MIGRATION.md](COMPONENT_MIGRATION.md)
- **Source/projection registry:** [schemas/data-registry.json](schemas/data-registry.json)

Edit the 24 authoritative collections under `data/`, then run:

```sh
python tools/validate_data.py
python tests/validate_data_structure.py
python -m http.server 8000
```

Open `http://localhost:8000/`. Existing page URLs are unchanged. Pages read the
collections directly through `data-store.js`; there is no catalogue build step.
Saved numerical outputs remain under `generated/models/` and are unchanged by
source validation. Python validation needs `jsonschema`; browser tests need `jsdom`.

Use HTTP hosting, including for local offline work. The retired three-catalogue
file picker is replaced with local-server instructions. The source-view links on
pages show transient JSON and link to its authoritative collections.

See the standard before adding a record, changing a schema or recalculating models.
