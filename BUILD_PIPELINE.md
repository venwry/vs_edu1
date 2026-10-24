# Build ownership and stage order

## Direct collection reads (structural edits)

Edit the 24 authoritative `data/*.json` collections and run
`python tools/validate_data.py`. Browser and Python readers assemble legacy shapes
in memory using `schemas/data-registry.json`. There is no catalogue generator,
committed catalogue copy, or build needed for data edits. Static hosting serves the
collections directly alongside saved outputs in `generated/models/`.

## Financial recalculation (intentional numerical changes)

`python tools/rebuild_outlook.py` is the existing full-chain orchestrator. It first
validates the authoritative collections, then runs in an isolated staging checkout. This migration retains its calculation order because
changing financial models would change displayed information:

| Stage | Script | Outputs / ownership |
| --- | --- | --- |
| Recurring costs | `build_cost_assessment.py` | `manufacturing-costs.json` |
| Base price assessment | `build_pricing.py` | Base `pricing-results.json` |
| November overlay | `build_comdex82_costs.py` | November cost review; pricing overlay |
| Retail catalogue | `build_retail_catalog.py` | Dated retail catalogue results |
| Base demand | `build_sales.py` | Base sales forecast |
| Industrial resources | `build_investment_model.py` | Industrial investment model and HTML |
| Base financials | `build_roi.py` | Base ROI, marketing budget, display impact and ROI HTML |
| Timeline feedback | `build_market_outlook.py --timeline` | Updates owned timeline records via the source bridge |
| Second base pass | Sales → investment → ROI | Existing feedback reconciliation |
| Supporting reviews | Market outlook → memory report → NCC review | Corresponding model outputs |
| Final reassessment | `build_sales_reassessment.py` | Final sales, ROI, quarterly market share and ROI HTML |
| Ecosystem | `build_ecosystem_forecast.py` | Ecosystem forecast and HTML |

Paths in the output column are relative to `generated/models/`. The final
reassessment, not the base sales/ROI stage, owns the published reassessed results.
Do not run a base stage afterwards and call its output the current scenario.
`rebuild_ncc82.py` intentionally rebuilds the cost/pricing/review subset only.
`build_artemis_budget.py` is an explicit optional overlay that updates manufacturing
costs, pricing and the Artemis budget review together; it is not an automatic part
of collection validation. `apply_memory_manufacturing.py` is an explicit source
transformation, not a routine build step.

The retained financial scripts share intermediate filenames only inside the staging
checkout managed by `tools/pipeline.py`. The orchestrator is the single publisher:
it copies results into the working repository only after every selected stage and
collection validation succeeds. A failed calculation leaves current outputs intact.
The individual legacy scripts are internal stages, not independent publish targets.
Do not bypass the orchestrator when producing current financial results. The
calculation formulas and ordering remain unchanged by this migration.

## Provenance and rebuild safety

Frozen baseline files are inputs, not stale outputs to delete. Existing snapshot
provenance may contain the original root filenames; resolve through the registry's
`legacy_paths` map. Do not refresh hashes without actually running the corresponding model.
Current model scripts emit the new paths. A numerical rebuild can differ from the
committed snapshots because the original repository already contains stale model
hashes and older validator expectations; see `MIGRATION_VALIDATION.md`.

The source mutation bridge validates staged collections before writing and distributes
fields to their owners. New records belong in the existing collection arrays; no
per-record registration is needed. New programme fields require explicit ownership
in the collection contract. See `JSON_DATA_STANDARD.md`.

## Shared HTML assembly

After UI configuration edits or report regeneration, run `python tools/build_site.py`.
It installs common navigation and relocated content on all pages and report
templates and rebuilds redirects. The financial orchestrator invokes it inside
its staging checkout before publishing, so later report builds retain navigation.
An ecosystem-only revision can run `run_pipeline([['build_ecosystem_forecast.py']])`
using current committed sales inputs; it does not publish a new sales/ROI result.

## Component identity migration

Cost builders consume canonical `part.*` IDs. Only components with `bom_role:
"material"` enter component costing; composed parts reference explicit assemblies.
Saved models from before the migration retain their bytes and old IDs. The shared
readers translate those identifiers and component-keyed/composite maps in memory.
This is an identity adapter, not a recalculation. `document_bytes` still returns
stored bytes for archived model provenance checks. See `COMPONENT_MIGRATION.md`.

Device-owned BOM definitions are composed into the hardware-BOM view at read time.
Writers route these definitions back to `data/devices.json`; do not copy them into
`data/assemblies.json`. Recurse by assembly-index membership, not an ID prefix.
See [DEVICE_BOM_MIGRATION.md](DEVICE_BOM_MIGRATION.md).
