# Single authoritative data layer

This migration replaces 951 per-record source files and 25 generated catalogue
JSON files with 24 grouped authoritative collections. It preserves the offer,
assembly and computer model; the later base-chassis/composition redesign is deferred.

Browser and Python readers now consume the same collections. Compatibility shapes
are assembled in memory, never regenerated into a second stored catalogue layer.
Existing stable IDs, supplier/date values, record order and unknowns are preserved.
Financial results and frozen baseline bytes are unchanged. Schemas remain separate
contracts, and calculated models remain separate results.

## Ownership

| Collection | Owned root fields |
| --- | --- |
| `data/assemblies.json` | `assemblies` |
| `data/campaigns.json` | `aurelia_1978_campaign`, `ncc_1979_campaign`, `ncc_1980_campaign`, `comdex_1979_campaign`, `comdex_1982_campaign`, `ncc_1982_campaign`, `team_development_program` |
| `data/components.json` | `base_parts` |
| `data/computers.json` | `computers`, `external_platforms` |
| `data/contracts.json` | `event.dri_founding`, `event.dri_cpm`, `event.bpi_offer`, `event.retail`, `event.smc_agreement`, `event.aionix_agreement`, `event.tandy_agreement`, `event.apple_cooperation`, `event.apple_extensions`, `event.ibm_project`, `event.clone_agreement_northstar`, `event.clone_agreement_vector`, `event.clone_agreement_sks`, `event.clone_agreement_goupil`, `event.clone_agreement_eina`, `event.sgs_transfer_agreement` |
| `data/cost-inputs.json` | `artemis_budget_inputs`, `ncc_1982_inputs`, `comdex_1982_cost_inputs`, `memory_manufacturing` |
| `data/demand-inputs.json` | `market_reactions`, `sales_reassessment_inputs`, `sales_model_inputs`, `aurelia_plus_aion_memory`, `artemis_tiers` |
| `data/ecosystem-inputs.json` | `ecosystem_forecast_policy` |
| `data/events.json` | `events` |
| `data/investment-inputs.json` | `artemis_display_revision`, `memory_manufacturing`, `manufacturing_programs` |
| `data/manufacturing-processes.json` | `memory_manufacturing` |
| `data/offers.json` | `offered_bundles`, `proposed_bundles`, `commercial_offerings` |
| `data/peripherals.json` | `devices` |
| `data/product-boms.json` | `metadata`, `products`, `offers`, `open_decisions`, `costing_inputs`, `proposed_offer_refs` |
| `data/programmes.json` | `product_strategy`, `review_scope`, `market_reactions`, `memory_manufacturing`, `athena_1983_program`, `manufacturing_programs`, `aurelia_plus_aion_memory`, `team_development_program`, `artemis_tiers` |
| `data/retail-catalog.json` | `retail_catalog_1982` |
| `data/services.json` | `services`, `team_development_program` |
| `data/site.json` | `aurelia_explorer`, `artemis_explorer`, `site_pages` |
| `data/software-editions.json` | `platform_editions` |
| `data/software-products.json` | `software_products`, `external_partner_products` |
| `data/sourcing.json` | `components`, `supplier_programs` |
| `data/standards.json` | `technologies` |
| `data/timeline-structure.json` | `phases`, `processes` |
| `data/world.json` | `metadata`, `scenario`, `entities`, `principles`, `conventions` |

## Consumer changes

`data-store.js` and `tools/data_store.py` share `schemas/data-registry.json`.
The registry contains file/field ownership, not hundreds of record registrations.
The former generated paths are accepted only as logical aliases in these readers.
HTML download links now open `data/view.html`, which shows an in-memory view and
links to actual source files. No former generated catalogue URL is fetched.
Serve the repository over HTTP; direct file selection of three generated files
has been retired. Local use works with `python -m http.server 8000` without internet.

The financial pipeline validates sources first and retains its existing staged
calculation order. Legacy transformers write through the source reader back to
owning collections. Normal data edits require validation, not a build.

## Validation

- `tools/check_migration.py`: all 25 previous catalogue payloads are semantically
  identical; saved model and baseline bytes are identical to the migration base.
- `tests/validate_single_data.py`: valid edits update only sources; invalid IDs,
  unresolved references, cycles and empty documents are rejected before writing.
- `tests/single-data.test.cjs`: all 25 JavaScript/Python views agree, edits appear
  without generation, and concurrent browser reads share collection requests.
- Collection schemas, legacy consumer contracts, BOM Navigator, domain navigators,
  specification rendering, timeline and page-content checks are exercised.

The baseline revision is `bb813e3`. Its Python domain suite has 14 passing and
19 failing validators. The failures reproduced before this migration are:

- `validate_artemis_tiers.py`
- `validate_artemis_video.py`
- `validate_bpi.py`
- `validate_costs.py`
- `validate_ecosystem.py`
- `validate_ecosystem_forecast.py`
- `validate_investment.py`
- `validate_market_outlook.py`
- `validate_market_share.py`
- `validate_memory_manufacturing.py`
- `validate_ncc79.py`
- `validate_ncc82.py`
- `validate_pricing.py`
- `validate_reactions.py`
- `validate_retail_catalog.py`
- `validate_roi.py`
- `validate_sales.py`
- `validate_team_1982.py`
- `validate_video.py`

The Node baseline has one existing failure: `atlas.test.cjs` expects a pricing
link in the timeline that the current navigation does not contain. These existing
checks remain enabled. Financial results were not rebuilt to hide stale provenance
hashes or older domain expectations. The one-time hash fixture is an audit of this
migration, not a prohibition on future intentional data edits.
