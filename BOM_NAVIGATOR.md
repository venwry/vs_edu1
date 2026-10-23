Computer-page follow-up: [COMPUTER_LISTS.md](COMPUTER_LISTS.md) supersedes the Artemis-only layout and multiple-filter description below. BOM Navigator behaviour is unchanged.

# BOM Navigator and Artemis list view

The BOM Navigator is a read-only catalogue at `bom-navigator.html`, linked from
Standards & services. It joins technical records and manufacturing components,
without duplicating a manufacturing component that already points to a technical
record. It covers parts, peripherals, computers, expansions, software products and
platform editions, catalogue/proposed bundles and commercial offerings.

Class, category and exact recorded introduction date filters combine with AND.
Partial dates retain their precision; missing dates have an Unknown option.
Introduction is not interpreted as confirmed shipment. The source availability,
announcement and qualification fields remain visible in the details. A selected
record can be linked with `?element=<record-id>`. Empty results clear the inspector;
Reset restores all records.

`bom-details.js` shares structural BOM and recorded-cost presentation between the
navigator and Artemis. Nested quantities are per parent assembly, never summed
as independent items. Unknown quantities/prices stay unknown. Assembly variants
are separate disclosures. Saved June 15 cost rows retain their status, range,
assumptions and decomposition. Detailed snapshot contents load on expansion.
Software cost includes its recorded media/licensing/delivery scope; it is not
represented as a manufactured hardware component. No financial model is rerun.

Artemis retains its configuration, revision and evaluation selectors. Six nested
sections replace the combined diagram. The list identifies fitted components,
empty slots, compatible options and architecture references separately. Memory
and OS architecture nodes and C portability references come from the same
`artemis_explorer` settings as the retired secondary diagrams. Compatible devices
and software come from the selected host record. Upgrade kits never acquire an
included host. Selecting the configuration name displays the full specification,
June 15 history and package cost decomposition; selecting an element displays
its specification and relevant BOM. Full platform records remain reachable as
reference entries. The duplicate architecture accordion and supplementary blocks
are removed from this page. Other computer pages retain their existing explorer.

Both main views use equal-width columns across the available browser width and
stack below 640 px. Native buttons, selects, details/summary and table headers
support keyboard operation. Selecting an item does not move keyboard focus.

Source changes: `site/config/document.site_pages.json` adds only presentation
metadata. `tools/data_catalog.py` regenerates its compatibility view;
`tools/build_site.py` adds the navigation destination to pages and report templates.
There are no historical fact, date, numerical assumption, schema or version
changes. Existing engineering estimates and qualification gaps remain unchanged.

Validation: `tests/bom-navigator.test.cjs` covers record coverage, deduplication,
unknowns, deep linking, combined filters, empty results and reset. Artemis tests
exercise every configuration, component button and revision/evaluation. Shared
navigation and cost destinations are checked by the site organization test.
Only the Artemis and new navigator body snapshots are intentionally changed.

Validation result: canonical schema/view checks, catalogue/BOM validators and all
34 page snapshots pass. The full Node suite passes 13 of 14 files, including all
new tests and every current CI consumer. The pre-existing `atlas.test.cjs` still
fails at its retired `.site-nav` pricing-link selector; its assertions are retained.
Browser screenshot review is pending; verification here used executable DOM and
model tests, not a rendered-browser visual check.
