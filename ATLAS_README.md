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

Catalog v2.4 incorporates the accepted MMU, Aurelia TPA discovery, FlexiBUS, Z80 peripheral bridge and BPI transaction designs under `specification.implementation_design`. Validation targets remain distinct from measured capabilities. The display API now specifies VRAM reuse between text and bitmap modes, font reload/redraw on mode changes and optional memory-checked screen preservation. Each computer lists its alternative text and bitmap allocations in `video.memory_layout`. TPA boundaries reserve application workspace within the existing physical RAM map. Facility planning and pricing remain deferred. Catalog v2.6 defines physical RAM populations and manufacturing requirements; electrical qualification remains open.

The 33 point events have author-confirmed day-level dates and are organized chronologically within eight consecutive calendar phases from 1972-01-01 through 1981-11-18. The 2025-12-07 time-travel origin is a separate prologue. Eight processes retain their original date precision/context and are listed separately by phase; the standalone Microsoft BASIC development event is deleted. Offers, plans and future rights retain their original meanings. Product introductions and platform availability are synchronized with confirmed launch dates.

## Pages

The directory links to dedicated Aurelia, Aurelia+, Artemis, Artemis PRO, Abacus, BPI, Pulse, Business Tools, C development, CP/M, AIONix, TUI/graphics, FlexiBUS, peripherals, networking, Academy/services and BASIC pages. All four computer pages provide hardware, peripherals, software, memory and bundle diagram layers, each fixed to its own model.

Artemis and Artemis PRO share the visual explorer format through `artemis-explorer.js`. The technical catalog's `artemis_explorer` section owns their diagram definitions and explanatory content. RAM controls distinguish shipping configurations from expanded module populations. Artemis exposes the later networking configuration; PRO includes networking at launch. Bundle diagrams use the selected bundle's configuration independently of these exploratory controls and preserve planned availability labels. The memory view depicts virtual-to-physical translation and memory resources; numeric address ranges remain unspecified. The optional CP/M-80 module appears only on the model whose compatibility list includes it.

`timeline.html` fills the browser's available width. The left inspector has a bounded width; the right calendar expands with the viewport, and party lanes share spare space while retaining horizontal scrolling on smaller screens. Equal-height years cover 1972–1981; the 2025-12-07 origin is separately labeled above the calendar. Compact cards show confirmed dates. The calendar uses native HTML/CSS, with no duration-bar visualization library.

Selecting an event or phase updates the inspector. Each phase's Processes section lists ongoing activities with their existing date precision and details; a separate Processes by phase section provides the same context below the timeline. Unknown durations are not plotted. The explicit 1973–1975 international investment process is listed in both phases it spans. Economics studies and NYSE speculation are separate processes. Legacy links to converted event IDs resolve to their process or phase.

Event filters, all-event-details mode, product links and event/phase fragments remain available. Process lists remain separate from the event filters. Lane definitions and display labels are in `site_pages.json`; story facts, processes and product facts remain in their JSON catalogs.

All HTML files are thin shells. `atlas.js` loads the three catalogs and renders their content; `architecture-explorer.js` renders the two Aurelia diagrams and supplies the shared explorer shell. The Artemis pages also load `artemis-explorer.js`. Shared styling is in `atlas.css`. Product or story changes belong in JSON, not in HTML or copied JavaScript objects.

## Validation

```sh
python -m pip install jsonschema
python tests/validate_catalogs.py
python tests/validate_hardware_bom.py
npm install --no-save jsdom
node tests/atlas.test.cjs
```

The schema/reference check validates uniform structures, unique IDs, actor/product/event references, page membership and key narrative distinctions. The DOM tests render every page, verify internal links and fragment targets, exercise both architecture explorers, RAM expansion, timeline filters and direct event links, and confirm JSON updates and offline recovery. DOM tests do not replace visual checks in a browser.

Catalog v2.5 places the BPI suite and relational-engine premiere in the NCC 1978 initial Aurelia offering, with Academy courses shortly afterward. Microsoft BASIC premieres at NCC 1979. The timeline removes the nonexistent 1978 COMDEX phase; platform editions and accounting-package availability follow the revised dates. BPI remains separately sold.


## Confirmed dates and process classification

[PHASE_DATE_REVIEW.md](PHASE_DATE_REVIEW.md) records the applied author confirmations. Aurelia+/Pulse/Abacus 2.0 launches on 1979-12-03 in phase five, Academy services begin on 1978-03-25, and BPI training begins on 1978-06-12. The AIONix agreement is in phase three; compatibility-module development and software preparation are in phase four. Their commercial introduction remains 1980-05-19.

Legacy fragments for the three merged phases resolve to their replacement phases. The narrative includes the synchronized phase/event/process index and updated dates.

## RAM and manufacturing baseline (v2.6)

[RAM_BOM_DESIGN.md](RAM_BOM_DESIGN.md) documents corrected chip densities, paired 16-bit RAM modules and four 32-bit banks. The Artemis explorer distinguishes equal capacities with different module populations. Superseded RAM records remain available for historical references but are excluded from active manufacturing.

`hardware_bom.json` contains component requirements, nested assemblies, coverage for every hardware catalog record and packouts for all offered bundles. `hardware_bom.schema.json` validates its structure. This engineering file is separate from the three catalogs loaded by the site; catalog records link to it through manufacturing requirements and assembly IDs. Unknown quantities and costs are null, and cost rollups remain blocked. The hardware validator checks bank arithmetic, assembly references and cycles, bundle coverage, and single-count networking/OS configurations.
