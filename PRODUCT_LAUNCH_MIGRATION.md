# Product launches and shipment dates

Products reference `launch_campaign_ref`. Campaigns own `id`, `launch_date`,
`main_launch_event_ref`, and unique `event_refs`; event definitions remain in
`data/events.json`. Main-event start and launch date must agree. Ten campaign
records cover the product launches from 1978 through 1983. Existing NCC/COMDEX
1979 campaigns were normalized, not duplicated.

The first chronological product composition `valid_from` is its shipment date.
It can follow the launch: COMDEX 1979 is December 3, with snapshot-defined bundles
shipping December 15; NCC 1982 is June 7, with review-defined kits shipping June 15.
Composition intervals and physical inventories were not changed.

Removed product introduced, shipping_date (including commercial_terms),
catalogue_status, availability_status, availability, product_status, status,
earliest_offer_date, and the obsolete campaign filename reference. Quotation
purchase terms, option relationships, engineering acceptance conditions and
snapshot date provenance remain. Device/software introduction metadata is unchanged.
The Team Edition launch date moved from programmes to its campaign; its merged
legacy view continues to expose it once.

The shared projection provides an in-memory `introduced` compatibility label from
campaign identity and composition shipment date for old consumers; no duplicate
product date is stored. Generic Details hides that compatibility field. BOM release
sorting reads composition dates for products. Computer labels no longer claim
undated planned/announced states, and the status line displays shipment date.
Computer dropdown membership remains solely `computer_line`.
Legacy commercial groups are category-derived: software in commercial_offerings,
other products in offered_bundles, proposed_bundles empty. No permanent status is
used to determine inclusion. Legacy memory configurations represent product
shipping configurations; financial qualification is independent.

Run validate_data.py, validate_data_structure.py, validate_product_launches.py,
validate_product_catalog.py, validate_product_standardization.py, and the computer,
composition-version, single-data and page-content browser tests. Saved financial
models and immutable baselines must not be rebuilt for this structural migration.
