# Canonical category and vendor migration

This accepted catalogue cleanup applies the 406-element BOM review to authoritative
JSON, rather than adding display labels. It changes classification and brand
attribution, not historical launch dates, technical specifications or cost inputs.

## Ownership and conversion

- Source records under `data/hardware/`, `data/software/`,
  `data/commercial/offers/` and `data/manufacturing/sourcing/` own the new categories.
- Components, BOM components, peripherals, computers, software products and offers
  now use schema version 2.0.0. The existing external Tandy computer shares the
  computer schema and now uses `computer`; its ownership and specifications remain.
- The 80 allowed functional codes live in `schemas/category.schema.json`. Existing
  proposed names were converted mechanically to lowercase snake_case (`I/O` to
  `io`); no second editable display vocabulary or legacy-code aliases are retained.
- Software editions keep their version-1 envelope and derive category from their
  existing `product_ref`. Their execution targets, dates, dependencies and memory
  requirements remain separate from parent product identity.
- Generic `catalog_component` and `unresolved_component` classifications are
  replaced by the reviewed functional categories. Qualification remains separate.
- `display` becomes `monitor`; display-controller ICs, graphics-controller ICs,
  CRT tubes/assemblies, DACs and video expansion cards remain distinct categories.
- Bundle function is `system_bundle` or `upgrade_bundle`. Proposed/reviewed status
  remains in the original source collection and status fields, not the category.
- Six review-only identities (`offer.ncc82_colour_upgrade`,
  `offer.ncc82_professional_graphics`, `offer.ncc82_mouse_learning`,
  `offer.comdex82_reference_hardware`, `offer.comdex82_professional_hardware`,
  `offer.comdex82_upgrade_autocad`) are registered as canonical commercial offers.
  Their review dates are explicitly not confirmed shipment dates. Archived review
  costs remain in manufacturing-costs.json. Navigator inventory stays at 406.

## Vendors and uncertainty

56 existing records and the six extracted offers receive the accepted Logix/AION
Software selling-brand attribution. Existing independent vendor values are retained.
The Mono Pro 17 OEM core records Ball Brothers as an unqualified candidate, with a
basis note; its manufacturer remains null. 245 navigator entries still have no
assigned vendor. Generic components have not been attributed to their host brand.

## Consumers and costs

`catalog-categories.js` centralizes explicit memory, monitor, video-card, disk and
expansion predicates. BOM Navigator and the computer/architecture views consume
these codes directly. Category labels are ordinary underscore-to-space formatting.
Compatible Aurelia RAM expansion is now listed under Memory and its external
floppy options under Disk drives, following their functional categories. These
are placement corrections; selected configuration membership is unchanged.
Services and their categories are unchanged; the cost builder now rejects an
unsupported service category instead of falling through to training costing.

Component costs, assembly routing and quantities use stable IDs/references, not the
renamed hardware categories. No prices, quantities, royalties, labor assumptions or
saved manufacturing-cost results were changed. Frozen financial baselines remain
immutable. The ecosystem-only pipeline is regenerated for current catalogue source
hashes; this does not publish a new sales, pricing, manufacturing-cost or ROI model.

## Verification

Compared with main tree `64209f9afef9a00c5425c3f5915935a5a788ad97`:

- 83 configuration/revision/date states across Aurelia, Artemis and Athena retain
  the same selected components, display/card choices, BOMs and saved estimates.
- Executing the existing cost setup, component calculations, assembly roll-ups and
  hardware estimate functions produces identical results for 278 components,
  115 assemblies and 57 hardware/OEM rows over five annual evaluations. The
  serialized comparison SHA-256 is
  `e16010d377b8473e7c20298222aeda9cd1298e16f3faac830c856e8a7292fa9e`.
- This was a bounded calculation comparison, not a full financial rebuild. The
  full cost builder has a documented pre-existing missing AIONix2 profile
  (`MIGRATION_VALIDATION.md`); no profile or price was invented to bypass it.
- New regression checks validate all 406 categories, edition inheritance, linked
  BOM categories, hardware classification, vendor uncertainty and failure on
  unsupported service categories. The existing CI page/domain suites also run.

The repetition inventory is in `BOM_NAVIGATOR_REPETITIONS.md`. No repeated record
has been merged or deleted.
