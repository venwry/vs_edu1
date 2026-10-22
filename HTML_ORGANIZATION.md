# Site organisation and content ownership

The primary navigation has 19 destinations in five sections. Its authoritative
source is `site/config/document.site_pages.json`; `tools/build_site.py` generates
one identical header for all primary pages, legacy redirects and financial report
templates. The compact header uses five bordered section cells, inline slash-separated
links, 12px type and shortened navigation labels; full page titles remain unchanged.
There is no separate brand/title row. The header spans the viewport without a
maximum-width cap or outer padding. Navigation uses automatic table layout so
cell widths follow their text content rather than equal columns. Below 540px,
the five-cell row scrolls horizontally to keep links readable. Run catalogue assembly before this builder. Financial pipelines run
the site builder before publishing their staged output.

| Previous pages | Current destination |
| --- | --- |
| index | Timeline, including assumptions, people and organisations |
| Aurelia, Aurelia+ | Aurelia, with model and documented-offering selectors |
| Artemis, Artemis PRO | Artemis, with model, offering, RAM and networking controls |
| Enhanced CP/M, AIONix | Operating Systems, including the recorded AIONix 2 plans |
| Abacus, Business Tools | AION Business Software |
| Pulse, C development | Software Development |
| TUI and graphics APIs | Video system |
| Microsoft BASIC | Third-party ecosystem; its original release event remains on Timeline |
| NCC 1982, COMDEX 1982 | Campaigns on Timeline; technical sections on Artemis/Video system; commercial sections on Retail pricing; Team Edition on Software Development |
| Manufacturing costs | Product pages, FlexiBUS, Retail pricing and Investment as described below |

BPI retains its own page and is also represented in the third-party catalogue.
Old URLs redirect while preserving incoming query strings and anchors. Model
anchors select the corresponding model; COMDEX's November-price anchor goes to
Retail pricing. Redirect pages retain navigation and a usable fallback link.

## Computer views

Model selection loads the selected architecture, memory layout and software.
Documented offerings switch the bundle diagram, included monitor/devices,
configuration details and Artemis RAM. Colour and monochrome offers remain
separate dated records. The existing RAM/networking controls explore upgrades;
the bundle view explicitly distinguishes a recorded offer from exploratory
upgrades. PRO's included networking is not presented as an optional launch feature.
Expansion targets retain their qualification warnings. Do not generate a Cartesian
product of every RAM, display and network option or imply all combinations shipped.

## Manufacturing and technical details

`site-shell.js` reads existing technical, BOM and manufacturing projections.
Product rows retain all dated snapshots, breakdowns, source assumptions, unknown
quantities and recursive assembly/component requirements. Expensive details render
when opened. No manufacturing figure was changed by this reorganisation.

Computer-specific components appear with their computer family. Shared generic
FlexiBUS devices appear on FlexiBUS with specifications and BOMs. Other peripherals
retain their dedicated page. Software delivery/manufacturing rows appear on their
software pages. Bundles and services appear under Retail pricing as combined or
delivery costs, rather than physical manufactured products. Investment owns global
process assumptions, fabrication programmes, supplier scenarios and exclusions.
June/November 1982 product reviews remain available alongside their product pages
and Retail pricing. Component and assembly costs overlap and must not be added twice.

## Timeline and hand-authored material

Every original event remains in canonical data. The two 1982 conference campaigns
show one calendar block each, with dated preparation/follow-up steps inside its
details. Each step retains its stable event ID and deep link. Independently
meaningful Autodesk agreement, incorporation, handover, beta and financial review
events remain individual milestones. Search includes nested campaign text.

`site/content/` holds the relocated HTML narrative sections from the two retired
conference pages. These preserve existing editorial descriptions and tables; new
product facts must be authored in canonical JSON, not added as conflicting HTML
facts. The builder inserts campaign fragments into templates in Timeline and
product/commercial fragments in their destination pages.

## Ecosystem model revision

The model now has an explicit legacy compatibility pool, because a list of named
examples cannot represent the available CP/M market. The assumed discoverable
family pool is 250, 450, 750, 1,200, 1,800 and 2,500 for 1978–1983. Conservative,
central and strong scenarios qualify 20%, 40% and 60%, with one quarter's lag.
These are alternative-history planning assumptions, not historical measured totals.
The qualified pool is a floor using `max`, not an addition to the existing
installed-base curve. Named candidates and anonymous families share this pool.

Open interfaces, qualification tooling, loan systems, training, cooperative support
and portable C/TUI development underpin the qualification scenarios. Native ports
still require source rights, adaptations, tests and elapsed engineering time.
Historical manufacturer/product examples do not establish fictional signed deals.

For 1983 Q4 this produces 500/1,000/1,500 qualified CP/M families and 195/510/998
native AIONix families. TUI titles remain a subset; cross-platform families are
counted once. Clone computer models were previously counted twice in one summary;
that duplication is corrected. Product growth does not itself create paid licences.
Existing licence purchase budgets and the existing Logix sales factors already
recognise software/compatibility benefits: this change does not apply another
blanket sales uplift or alter sales, prices, ROI or market share.

This is an ecosystem-only numerical rebuild, staged via `pipeline.run_pipeline`.
The full cost/financial pipeline still has the previously documented missing
AIONix 2 cost profile; no cost was invented to bypass that limitation.

## Maintenance and verification

Run:

```sh
python tools/data_catalog.py
python tools/build_site.py
python tests/validate_data_structure.py
python tests/validate_catalogs.py
python tests/validate_hardware_bom.py
python tests/validate_ecosystem_forecast.py
node tests/site-organization.test.cjs
node tests/page-content.test.cjs
```

The organisation test checks identical headers, all cost rows, redirects, both
family models/configuration selectors, campaign grouping and ecosystem accounting.
The page-content test normalises only the shared header to the frozen
`tests/fixtures/page-baseline-navigation.html` before comparing the existing body
snapshots. The organisation test checks the actual current header separately.
The original migration snapshot remains `tests/page-content-baseline.json`.
The intentional new UI uses `tests/page-content-reorganized.json`; updating it
requires reviewing the organisation/content coverage tests, not merely accepting
a changed hash. Existing domain tests continue to test diagrams, BOMs, financial
views, timeline behaviour and report exports.
