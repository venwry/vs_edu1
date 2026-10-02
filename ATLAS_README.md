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

The 41 events retain narrative order within 13 phases. The time-travel origin in 2025 intentionally precedes the intervention in 1972 in causal order. Approximate dates, offers, future rights and plans are not converted into completed transactions or invented exact dates. Product introductions can be more precise in the technical catalog than in the narrative; each retains its own date precision.

## Pages

The directory links to dedicated Aurelia, Aurelia+, Artemis, Artemis PRO, Abacus, BPI, Pulse, Business Tools, C development, CP/M, AIONix, TUI/graphics, FlexiBUS, peripherals, networking, Academy/services and BASIC pages. Aurelia and Aurelia+ retain their interactive architecture layers, RAM and networking controls, and bundle diagrams, each fixed to its own computer model.

`timeline.html` shows six colored swimlanes for Adam, Logix, AION/BPI, partners, Apple/Peachtree and IBM/the market. Conference and inter-conference phases run downward, with sticky lane headings and phase labels. Each event appears once in its principal lane, with all participants identified on the card. Dense event groups can be expanded. Lane assignments and display labels are defined in `site_pages.json`; event facts remain in the story JSON.

The timeline retains phase, participant, event-type and text filters. Select a card to open its full details below the board, or enable all event details. Stable event links select the corresponding event, clearing incompatible filters when needed. The layout follows narrative phase order rather than proportional calendar spacing, including the 2025 time-travel origin before the 1972 arrival. Offering pages link to related events, and product references and subject mentions link to relevant offering pages.

All HTML files are thin shells. `atlas.js` loads the three catalogs and renders their content; `architecture-explorer.js` renders the two Aurelia diagrams from the technical catalog. Shared styling is in `atlas.css`. Product or story changes belong in JSON, not in HTML or copied JavaScript objects.

## Validation

```sh
python -m pip install jsonschema
python tests/validate_catalogs.py
npm install --no-save jsdom
node tests/atlas.test.cjs
```

The schema/reference check validates uniform structures, unique IDs, actor/product/event references, page membership and key narrative distinctions. The DOM tests render every page, verify internal links and fragment targets, exercise both architecture explorers, RAM expansion, timeline filters and direct event links, and confirm JSON updates and offline recovery. DOM tests do not replace visual checks in a browser.
