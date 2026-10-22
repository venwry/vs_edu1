# Build ownership and stage order

## Catalogue assembly (safe for structural edits)

`python tools/data_catalog.py` reads `data/manifest.json`, resolves canonical records
under `data/` and `site/config/`, and exclusively produces `generated/catalogs/`.
It is deterministic, preserves source order and does not calculate business metrics.
`--check` compares views to sources without writing. Static pages consume these
views plus archived outputs under `generated/models/`. Existing page URLs stay fixed.

## Financial recalculation (intentional numerical changes)

`python tools/rebuild_outlook.py` is the existing full-chain orchestrator. It first
checks that catalogue views are current, then runs in an isolated staging checkout. This migration retains its calculation order because
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
of catalogue assembly. `apply_memory_manufacturing.py` is an explicit source
transformation, not a routine build step.

The retained financial scripts share intermediate filenames only inside the staging
checkout managed by `tools/pipeline.py`. The orchestrator is the single publisher:
it copies results into the working repository only after every selected stage and
source/view validation succeeds. A failed calculation leaves current outputs intact.
The individual legacy scripts are internal stages, not independent publish targets.
Do not bypass the orchestrator when producing current financial results. The
calculation formulas and ordering remain unchanged by this migration.

## Provenance and rebuild safety

Frozen baseline files are inputs, not stale outputs to delete. Existing snapshot
provenance may contain the original root filenames; resolve through the manifest's
`paths` map. Do not refresh hashes without actually running the corresponding model.
Current model scripts emit the new paths. A numerical rebuild can differ from the
committed snapshots because the original repository already contains stale model
hashes and older validator expectations; see `MIGRATION_VALIDATION.md`.

The source mutation bridge validates all proposed records before writing, distributes
owned fields to canonical files, and rejects unregistered IDs/fields. When adding a
new entity, register it in the manifest before invoking a legacy transformer. New
code should edit domain records directly and use the assembler for projections.

## Shared HTML assembly

After data assembly or report regeneration, run `python tools/build_site.py`.
It installs common navigation and relocated content on all pages and report
templates and rebuilds redirects. The financial orchestrator invokes it inside
its staging checkout before publishing, so later report builds retain navigation.
An ecosystem-only revision can run `run_pipeline([['build_ecosystem_forecast.py']])`
using current committed sales inputs; it does not publish a new sales/ROI result.
