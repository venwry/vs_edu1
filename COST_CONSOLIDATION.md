# Cost review consolidation and Navigator

The structural migration `python tools/merge_cost_reviews.py` embeds the complete NCC and COMDEX reports under `manufacturing-costs.json.reviews["ncc-1982"]` and `["comdex-1982"]`, then removes the two standalone outputs. No facts, assumptions, dates, IDs, numeric values or nulls change. The additive review-envelope contract is version 1.0.0 (`schemas/models/manufacturing-reviews.schema.json`); the existing manufacturing model version remains unchanged. This schema validates the container and identity/date fields, not every legacy financial field.

Example access: `model.reviews["comdex-1982"].prices[0].manufacturing_cost_usd`. Reviews retain nominal USD, estimate status, ranges, mixed-supplier boundaries, Team launch/proxy cost dates and source hashes. Unknown costs stay null. The November `cost_assessment` is retained in its historical review envelope and in `dated_assessments` for existing computer configurator consumers; they represent the same assessment, never additive costs.

`tests/fixtures/cost-consolidation-hashes.json` records semantic SHA-256 digests of the three pre-migration outputs. The migration audit verifies complete preservation. These fixtures intentionally need review after any future numerical rebuild. Historical input hashes describe their original inputs; they are not rewritten to imply a recalculation after this packaging change. Future NCC builds hash canonical JSON (sorted keys, compact separators, UTF-8) excluding `reviews` and declare `source_hash_scopes` for the manufacturing input; this avoids a self-reference. Legacy hashes remain untouched.

The NCC/COMDEX builders now write the embedded reviews. The base cost builder preserves those independently generated sections until their own pipeline stages refresh them. Sales reassessment and site loaders read the unified file. Annual cost/pricing generation remains governed by BUILD_PIPELINE.md. No financial builders were run for this change.

Navigator has accessible Details, Bill of Materials, Manufacturing costs and Related events tabs. BOM records include source requirements, nested assemblies and component qualification; costs include annual evaluations and dated commercial reviews. Reviewed offerings without technical catalogue records are explicitly identified, and no technical specifications are invented. Event association uses exact product references and links to the timeline.

Nine domain pages now link covered products to Navigator instead of rendering duplicate specifications, BOMs and cost reviews. Standards, services and external-platform records outside Navigator remain on their domain pages; Academy has no covered records to remove. Product campaign recaps on the video/development pages are removed from display; complete campaign context remains on the timeline.

## Validation

Passed: canonical source/schema validation (956 records), catalogue references (145 events), hardware BOM validation (115 assemblies), lossless consolidation and idempotence, November pricing arithmetic, Navigator tabs/keyboard navigation/filtering/unknown costs, and domain-page deduplication with complete cost coverage. The reviewed 34-page text/table/link fixture was updated for the intentional removals and new links.

Known existing failures remain: `validate_ncc82.py` checks a stale manufacturing-input hash; `validate_ecosystem_forecast.py` checks a stale technical-catalogue hash; `atlas.test.cjs` expects the retired timeline `.site-nav` pricing link. The original manufacturing file already failed the NCC hash comparison before this migration. No assertions or historical hashes were removed to hide these failures. Financial rebuilding and correction of these existing model-provenance issues are outside this structural change.

The full JavaScript suite passes 14 of 15 files; the only failure is the pre-existing `atlas.test.cjs` navigation assertion described above. Computer-family checks cover every configuration, revision and component across Artemis, Aurelia and Athena.
