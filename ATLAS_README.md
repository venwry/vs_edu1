# Logix / AION Atlas

Open `index.html` through a static web server, for example from this directory:

```sh
python -m http.server 8000
```

Then visit `http://localhost:8000/`. No build step is required. When opening an HTML file directly, select the three JSON catalogs in the page's file picker. Serving over HTTP is recommended for navigation between pages.

## Data ownership

- `logix_aion_technical_catalog_v2.json`: product specifications, architectures, software, services and bundles. This change preserves the existing technical catalog.
- `logix_aion_story.json`: narrative conversion with exactly two root sections, `assumptions` and `phases`. The original Markdown remains unchanged.
- `site_pages.json`: page titles, descriptions, catalog record membership, aliases and navigation.
- `logix_aion_story.schema.json`: strict JSON Schema for the narrative. Events use the same keys for dates, participants, actions, outcomes, agreement terms, metrics and references. Empty collections remain arrays; unknown values remain null.

Technical catalog v2.3 adds canonical `platform_editions`. Each software edition declares its execution target, role, per-computer availability, dependencies, delivery and resource-budget status. Product `edition_refs` and computer compatibility lists are validated against these records. Software product pages show their editions directly. Abacus 1 and 2 both support Aurelia and Aurelia+; their later native ERA editions remain separate.

`software.aionix_server` replaces `software.aionix_networked` as a complete AIONix Server edition. It includes the base OS and network services and does not require a prior OS installation. Network bundles supply this edition, while BPI application licensing remains separate. Pulse integration means offline read/edit/write access to versioned Abacus files, not a live shared spreadsheet.

Catalog v2.4 incorporates the accepted MMU, Aurelia TPA discovery, FlexiBUS, Z80 peripheral bridge and BPI transaction designs under `specification.implementation_design`. Validation targets remain distinct from measured capabilities. The display API now specifies VRAM reuse between text and bitmap modes, font reload/redraw on mode changes and optional memory-checked screen preservation. Each computer lists its alternative text and bitmap allocations in `video.memory_layout`. TPA boundaries reserve application workspace within the existing physical RAM map. Facility planning, pricing, manufacturing and memory-bus organization remain deferred.

The 41 events retain narrative order within 13 phases. The time-travel origin in 2025 intentionally precedes the intervention in 1972 in causal order. Approximate dates, offers, future rights and plans are not converted into completed transactions or invented exact dates. Product introductions can be more precise in the technical catalog than in the narrative; each retains its own date precision.

## Pages

The directory links to dedicated Aurelia, Aurelia+, Artemis, Artemis PRO, Abacus, BPI, Pulse, Business Tools, C development, CP/M, AIONix, TUI/graphics, FlexiBUS, peripherals, networking, Academy/services and BASIC pages. All four computer pages provide hardware, peripherals, software, memory and bundle diagram layers, each fixed to its own model.

Artemis and Artemis PRO share the visual explorer format through `artemis-explorer.js`. The technical catalog's `artemis_explorer` section owns their diagram definitions and explanatory content. RAM controls distinguish shipping configurations from expanded module populations. Artemis exposes the later networking configuration; PRO includes networking at launch. Bundle diagrams use the selected bundle's configuration independently of these exploratory controls and preserve planned availability labels. The memory view depicts virtual-to-physical translation and memory resources; numeric address ranges remain unspecified. The optional CP/M-80 module appears only on the model whose compatibility list includes it.

`timeline.html` shows six colored swimlanes for Adam, Logix, AION/BPI, partners, Apple/Peachtree and IBM/the market. Conference and inter-conference phases run downward, with sticky lane headings and phase labels. Each event appears once in its principal lane, with all participants identified on the card. Dense event groups can be expanded. Lane assignments and display labels are defined in `site_pages.json`; event facts remain in the story JSON.

The timeline retains phase, participant, event-type and text filters. Select a card to open its full details below the board, or enable all event details. Stable event links select the corresponding event, clearing incompatible filters when needed. The layout follows narrative phase order rather than proportional calendar spacing, including the 2025 time-travel origin before the 1972 arrival. Offering pages link to related events, and product references and subject mentions link to relevant offering pages.

All HTML files are thin shells. `atlas.js` loads the three catalogs and renders their content; `architecture-explorer.js` renders the two Aurelia diagrams and supplies the shared explorer shell. The Artemis pages also load `artemis-explorer.js`. Shared styling is in `atlas.css`. Product or story changes belong in JSON, not in HTML or copied JavaScript objects.

## Validation

```sh
python -m pip install jsonschema
python tests/validate_catalogs.py
npm install --no-save jsdom
node tests/atlas.test.cjs
```

The schema/reference check validates uniform structures, unique IDs, actor/product/event references, page membership and key narrative distinctions. The DOM tests render every page, verify internal links and fragment targets, exercise both architecture explorers, RAM expansion, timeline filters and direct event links, and confirm JSON updates and offline recovery. DOM tests do not replace visual checks in a browser.
