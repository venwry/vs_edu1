# Data reorganisation validation

Source: `venwry/vs_edu1` commit `d7720e909ba28060538dfc5f9c7d50ff832f0eb6`.
This is a structural migration, not a change to story facts or economic assumptions.

## Passed

- All **48 original JSON documents** reconstruct with identical parsed values and
  array order, including the two relocated legacy schemas.
- **956 canonical records/sections** are registered, schema-valid and reconstructed
  into 25 compatibility views. Overlapping ownership and cycles are rejected.
- Existing catalogue/reference and hardware-BOM validators pass.
- All **29 HTML pages** retain rendered text, table counts and link targets; only
  moved JSON paths are normalised in the comparison. Page URLs remain unchanged.
- Nine interactive/layout Node suites pass: architecture layout, costs, ecosystem,
  market share, pricing, ROI, sales, specification and timeline.
- Frozen baseline semantic hashes are unchanged; Python files compile.
- The pricing test mock URL matcher was updated for hyphenated paths. Its content
  assertions were retained.

## Pre-existing failures reproduced before and after

The original repository does not have a clean full validation suite:

| Validator | Existing failure |
| --- | --- |
| `validate_artemis_video.py` | Display raster capability assumption |
| `validate_costs.py` | Athena missing from cost coverage/exclusions |
| `validate_ecosystem.py` | Stale recorded input hashes |
| `validate_ecosystem_forecast.py` | Stale quarterly market-share input hash |
| `validate_investment.py` | Stale sales forecast input hash |
| `validate_market_outlook.py` | Older forecast period-count assumption |
| `validate_market_share.py` | Older quarterly-count assumption |
| `validate_memory_manufacturing.py` | Stale impact input hashes |
| `validate_ncc79.py` | Older event-count assumption |
| `validate_ncc82.py` | Stale manufacturing-cost input hash |
| `validate_pricing.py` | Older product-count assumption |
| `validate_reactions.py` | Stale source-story hash |
| `validate_roi.py` | Stale input hashes |
| `validate_sales.py` | Stale input hashes |
| `validate_team_1982.py` | Older programme status-string expectation |
| `validate_video.py` | Repository-wide text restriction conflicts with existing data |
| `atlas.test.cjs` | Expects four fetches on pricing page; current page makes five |

No assertions were removed to conceal these failures. The new CI gate runs source,
schema, reference, BOM, content-parity and currently passing interaction checks.
Repairing older checks or recalculating their models is separate work; do not update
hashes merely to make a stale model appear fresh.

## Financial pipeline smoke check

The original first numerical stage fails with `KeyError: 'aionix2'` in
`build_cost_assessment.py`: that software product has no cost profile. The same
failure occurs after migration. The new staging orchestrator leaves current outputs
untouched on failure. No fabricated cost profile was introduced, and no current
prices, forecasts or ROI values were recalculated.

## Reproduce

```sh
python tools/data_catalog.py --check
python tools/check_migration.py
python tests/validate_data_structure.py
python tests/validate_catalogs.py
python tests/validate_hardware_bom.py
node tests/page-content.test.cjs
```

The one-time semantic migration fixture is not an ongoing ban on intentional edits.
Update the page fixture only with reviewed intentional UI/content changes. See
`JSON_DATA_STANDARD.md` for normal authoring and validation procedures.
