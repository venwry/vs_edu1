# Logix / AION Atlas

Open `index.html` through a static web server, for example from this directory:

```sh
python -m http.server 8000
```

Then visit `http://localhost:8000/`. No build step is required. When opening an HTML file directly, select the three JSON catalogs in the page's file picker. Serving over HTTP is recommended for navigation between pages.

## Data ownership

- `logix_aion_technical_catalog_v2.json`: product specifications, architectures, software, services and bundles. Launch and service availability dates are synchronized with author confirmations.
- `logix_aion_story.json`: narrative conversion with three root sections, `assumptions`, `phases` and `processes`. The narrative Markdown is synchronized when story events are amended.
- `site_pages.json`: page titles, descriptions, catalog record membership, aliases and navigation.
- `logix_aion_story.schema.json`: strict JSON Schema for the narrative. Events use the same keys for dates, participants, actions, outcomes, agreement terms, metrics and references. Empty collections remain arrays; unknown values remain null.

Technical catalog v2.3 adds canonical `platform_editions`. Each software edition declares its execution target, role, per-computer availability, dependencies, delivery and resource-budget status. Product `edition_refs` and computer compatibility lists are validated against these records. Software product pages show their editions directly. Abacus 1 and 2 both support Aurelia and Aurelia+; their later native ERA editions remain separate.

`software.aionix_server` replaces `software.aionix_networked` as a complete AIONix Server edition. It includes the base OS and network services and does not require a prior OS installation. Network bundles supply this edition, while BPI application licensing remains separate. Pulse integration means offline read/edit/write access to versioned Abacus files, not a live shared spreadsheet.

Catalog v2.4 incorporates the accepted MMU, Aurelia TPA discovery, FlexiBUS, Z80 peripheral bridge and BPI transaction designs under `specification.implementation_design`. Validation targets remain distinct from measured capabilities. The display API now specifies VRAM reuse between text and bitmap modes, font reload/redraw on mode changes and optional memory-checked screen preservation. Each computer lists its alternative text and bitmap allocations in `video.memory_layout`. TPA boundaries reserve application workspace within the existing physical RAM map. Facility qualification remains open; pricing and sales now have separate scenario assessments. Catalog v2.6 defines physical RAM populations and manufacturing requirements; electrical qualification remains open.

The original 34 point events have author-confirmed day-level dates; six additional milestones use year/month precision and one event covers the NCC recording/session interval and are organized chronologically within eight consecutive calendar phases from 1972-01-01 through 1981-11-18. The 2025-12-07 time-travel origin is a separate prologue. Three top-level processes and four nested academic-year subprocesses are rendered as recorded or explicitly approximate intervals; the standalone Microsoft BASIC development event is deleted. Offers, plans and future rights retain their original meanings. Product introductions and platform availability are synchronized with confirmed launch dates.

## Pages

The directory links to dedicated Aurelia, Aurelia+, Artemis, Artemis PRO, Abacus, BPI, Pulse, Business Tools, C development, CP/M, AIONix, TUI/graphics, FlexiBUS, peripherals, networking, Academy/services and BASIC pages. All four computer pages provide hardware, peripherals, software, memory and bundle diagram layers, each fixed to its own model.

Artemis and Artemis PRO share the visual explorer format through `artemis-explorer.js`. The technical catalog's `artemis_explorer` section owns their diagram definitions and explanatory content. RAM controls distinguish shipping configurations from expanded module populations. Artemis exposes the later networking configuration; PRO includes networking at launch. Bundle diagrams use the selected bundle's configuration independently of these exploratory controls and preserve planned availability labels. The memory view depicts virtual-to-physical translation and memory resources; numeric address ranges remain unspecified. The optional CP/M-80 module appears only on the model whose compatibility list includes it.

`timeline.html` (Timeline original) fills the browser's available width. Its left inspector shows selected events, phases or processes. The right calendar has equal-height years from 1972–1981 and vertical party lanes. Each phase and each process is one continuous rectangle on the shared calendar coordinate system, spanning year boundaries without splitting. Overlapping processes occupy separate tracks alongside event cards. The 2025-12-07 origin is separately labeled above the calendar.

The timeline has a prominent **Timeline / Assumptions** tab switch. Assumptions occupy their own view, not a section below the calendar. The selected timeline position and item survive tab switches; `#assumptions` opens the assumptions view directly. Keyboard arrows, Home and End switch tabs.

`timeline-model.js` derives continuous display intervals. Economics studies spans September 1972–June 1976 with four nested year rectangles; the first two fall starts remain explicitly provisional. See [HARVARD_ACADEMIC_DATES.md](HARVARD_ACADEMIC_DATES.md) for sources and the commencement-based end-date convention. Apple compatibility and Artemis engineering still use approximate phase-context envelopes. Filtering never clips a process range.

The workspace is 870px high on desktop and mobile. There is no footer or visible section below it. The three organization/market assumptions retain their former process details and metrics in the Assumptions view. Legacy process links open the corresponding assumption. NYSE speculation is now part of Adam’s March 1, 1972 arrival event, following February’s lottery win.

The original view supports event/process search, phase/actor/type filters, all-event-details mode, product links and event/phase/process fragments. Legacy fragments still resolve. Party assignments and labels live in `site_pages.json`; story and product facts remain in their JSON catalogs.

All HTML files are thin shells. `atlas.js` loads the three catalogs and renders their content; `architecture-explorer.js` renders the two Aurelia diagrams and supplies the shared explorer shell. The Artemis pages also load `artemis-explorer.js`. Shared styling is in `atlas.css`. Product or story changes belong in JSON, not in HTML or copied JavaScript objects.

## Validation

```sh
python -m pip install jsonschema
python tests/validate_catalogs.py
python tests/validate_hardware_bom.py
python tests/validate_video.py
python tests/validate_ecosystem.py
npm install --no-save jsdom
node tests/atlas.test.cjs
node tests/timeline.test.cjs
```

The schema/reference check validates uniform structures, unique IDs, actor/product/event references, page membership and key narrative distinctions. The DOM tests render every page, verify internal links and fragment targets, exercise both architecture explorers, RAM expansion, timeline filters and direct event links, and confirm JSON updates and offline recovery. The dedicated timeline tests verify continuous range geometry, collision tracks, approximate envelopes, filtering, tab switching and direct links, including nested study years and migrated assumption links. DOM tests do not replace visual checks in a browser.

Catalog v2.5 places the BPI suite and relational-engine premiere in the NCC 1978 initial Aurelia offering, with Academy courses shortly afterward. Microsoft BASIC premieres at NCC 1979. The timeline removes the nonexistent 1978 COMDEX phase; platform editions and accounting-package availability follow the revised dates. BPI remains separately sold.


## Confirmed dates and process classification

[PHASE_DATE_REVIEW.md](PHASE_DATE_REVIEW.md) records the applied author confirmations. Aurelia+/Pulse/Abacus 2.0 launches on 1979-12-03 in phase five, Academy services begin on 1978-03-25, and BPI training begins on 1978-06-12. The AIONix agreement is in phase three; compatibility-module development and software preparation are in phase four. Their commercial introduction remains 1980-05-19.

Legacy fragments for the three merged phases resolve to their replacement phases. The narrative includes the synchronized phase/event/process index and updated dates.



Party lanes have draggable right-edge resize handles and collapse/expand buttons in their sticky headers. Collapsing hides all lane objects and leaves a 32px strip; expanding restores the previous width. Widths and collapsed states survive filtering and tab switches during the page session. Resize handles also support Left/Right arrows (20px steps) and Home (default width). Minimum widths keep event and process tracks from overlapping.

Event dates contain only `start` and `end`; equal endpoints may be ISO year, month or day. Partial-date milestones do not assert an exact day. Event labels use the start date. The inspector shows Start date and End date without a Date precision section. International investment expansion has been removed as a timeline process.
## RAM and manufacturing baseline (v2.6)

[RAM_BOM_DESIGN.md](RAM_BOM_DESIGN.md) documents corrected chip densities, paired 16-bit RAM modules and four 32-bit banks. The Artemis explorer distinguishes equal capacities with different module populations. Superseded RAM records remain available for historical references but are excluded from active manufacturing.

`hardware_bom.json` contains component requirements, nested assemblies, coverage for every hardware catalog record and packouts for all offered bundles. `hardware_bom.schema.json` validates its structure. This engineering file is separate from the three catalogs loaded by the site; catalog records link to it through manufacturing requirements and assembly IDs. Unknown quantities and costs are null, and cost rollups remain blocked. The hardware validator checks bank arithmetic, assembly references and cycles, bundle coverage, and single-count networking/OS configurations.

All four architecture pages fill the browser width. Drag the divider between diagram and details (or use its Left/Right arrow keys; Home resets it). Narrow screens stack the sections. Smaller blocks and larger gutters make the diagrams easier to read; shared orthogonal routing avoids intervening blocks and recalculates after resizing or changing layers. Run `node tests/architecture-layout.test.cjs` for routing checks.


## Unified Aurelia video (v2.7)

See [VIDEO_DESIGN.md](VIDEO_DESIGN.md). Both Aurelia and Aurelia+ now use 16 KiB custom dual-port VRAM and the shared controller, with native 40/80-column text, explicit bitmap and sprite allocations, and monitor capability discovery. The retained `video.text_mode` and `memory_layout` summaries describe the preferred/default configuration; `text_modes` and `bitmap_modes` enumerate all hardware configurations. Monitor filtering remains mandatory. Manufacturing figures are planning estimates; electrical qualification and costing gates remain open.

Architecture detail panels preserve nested specifications as expandable sections, lists and record tables. Short scalar properties use a single two-column Property/Value table at every panel width. Expand all / Collapse all controls operate within each specification; long explanations and status notes remain separate paragraphs. The renderer preserves zeros, false values, unknown values, and component names. Run `node tests/specification.test.cjs` for content-preservation and interaction checks.

## Negotiated networking and three-port Aurelia (v2.8)

See [NETWORK_DESIGN.md](NETWORK_DESIGN.md). The 1981 LAN negotiates one shared 100/250/500/1000 kbit/s rate with host ceilings, receiver credits, discovery and fallback. Aurelia and Aurelia+ each have three FlexiBUS ports. The catalog, adapter/hub requirements and manufacturing BOM carry the same baseline; rates and packet-RAM targets still require qualification.

## Recurring manufacturing cost assessment

`manufacturing-costs.html` compares all modeled June 15 offerings from 1978 through 1981, with product rows, four year columns, central/range values and selectable cost/BOM breakdowns. `manufacturing_costs.json` contains results and explicit assumptions; `tools/build_cost_assessment.py` reproduces it. See `MANUFACTURING_COSTS.md` for scope, historical sources, units, exclusions and uncertainty. Costs are scenario estimates rather than supplier quotes; engineering BOM unknowns remain unchanged. Software media, service units and bundles are distinct, overlapping views and must not be summed into a fleet-wide total.

### Retail pricing assessment

`pricing.html` presents 79 commercial products and bundles grouped by type, with June 15 snapshots for 1978–1981. `pricing_results.json` stores proposed retail prices, associated recurring costs, competitor evidence, availability, fees and stress cases. ComputerLand fees and cost scenarios are adjustable in the page. See `PRICING_ASSESSMENT.md` for assumptions and `tools/build_pricing.py` to regenerate. Prices are proposals, not amendments to historical catalog price fields.



## 1974 DRI / 1979 expansion and SMC revision

- `event.dri_founding`: late 1974, year precision; joint Gary/Dorothy/Adam company before Logix.
- `event.dri_cpm`: September 1, 1976 remains an Aurelia implementation milestone, not first cooperation.
- `event.smc_agreement`: July 1978; independent manufacturing/sales license with process-compatible mask and know-how transfer.
- `event.smc_sales`: October 1979; initial qualified sales, separate VRAM qualification and subsequent volume ramp.
- June 4, 1979 adds S-100 FlexiBUS and Apple II/S-100 video cards using AION launch silicon. Apple software is native; CP/M-6502 remains deferred.
- AIONix’s existing separate ownership/equity/1982 terms are retained; no replacement allocation was selected.
- `manufacturing_programs.json` contains separate one-time transfer budget assumptions and SMC purchase-price sensitivity inputs. Rebuild costs before pricing.
- 70 events, 3 parent processes and 4 subprocesses. Year/month positions in the chart are indicative; labels preserve source precision.


## Aurelia 1978 marketing and Academy

[AURELIA_1978_CAMPAIGN.md](AURELIA_1978_CAMPAIGN.md) and `aurelia_1978_campaign.json` define the accepted campaign, premiere, five-city Academy announcement and free professional television material. Timeline events appear in the Logix lane; the Academy catalog records the 50% Fundamentals credit. Run `python tests/validate_campaign.py` after regenerating costs and pricing.


## Revised retail contribution and demand through November 1979

Every page now includes Retail pricing and Demand and sales in its shared top navigation. `pricing_baseline.json` preserves the pre-reduction snapshots; current retail prices retain 60% of prior dollar contribution at unchanged costs/fees. Rebuild pricing, then `python tools/build_sales.py`. `sales.html` shows monthly 1978 sell-through, separate launch-year projections and June–November 1979 demand, delivery limits and sales, with scenario selection, market assumptions and the Academy roadmap. See [SALES_FORECAST.md](SALES_FORECAST.md). Run `python tests/validate_sales.py` and `node tests/sales.test.cjs` in addition to existing checks.


## Tandy, Apple and IBM reaction revision

[COMPETITOR_REACTIONS.md](COMPETITOR_REACTIONS.md) and `market_reactions.json` distinguish historical release windows from scenario milestones. The timeline has 70 events. Tandy external platform/CP/M/FlexiBUS and Abacus edition records appear on the Abacus page without invented OEM prices or Logix manufacturing costs. IBM delay is a software critical-path scenario; AIONix preliminary work begins before Aurelia launch. Sales incorporate named incremental effects, not retroactive Tandy shipments or an early IBM windfall. Run `python tests/validate_reactions.py` after costs, pricing and sales regeneration.


BPI is an independent partner in the Partners lane. See BPI_PARTNER_STRATEGY.md; run tests/validate_bpi.py for presentation order, ownership, dealer baskets, separate receipts and capacity gates.


The accepted NCC 1979 50-minute campaign and migration disclosure boundary are in NCC_1979_CAMPAIGN.md and ncc_1979_campaign.json. The timeline has 70 events. Run tests/validate_ncc79.py. CONSISTENCY_REVIEW_1979.md separates corrected conflicts from open engineering/commercial decisions.

## COMDEX 1979 manufacturer compatibility programme

[AURELIA_COMPATIBILITY_KIT.md](AURELIA_COMPATIBILITY_KIT.md) records the December 3 kit launch, optional support/certification and shift toward Aurelia+ with independent Aurelia-class implementations. The C/developer offering page shows the kit; the Academy/support page shows optional services. All three appear under Developer programs in pricing, first at the June 1980 annual snapshot. The separate compatibility pricing baseline preserves the original baseline unchanged.
