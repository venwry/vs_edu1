# TimelineJS 3.9.13 assets

CSS, icon font and license are locally bundled from the published `@knight-lab/timelinejs@3.9.13` package:

- https://cdn.jsdelivr.net/npm/@knight-lab/timelinejs@3.9.13/dist/js/timeline.js
- https://cdn.jsdelivr.net/npm/@knight-lab/timelinejs@3.9.13/dist/js/timeline.js.LICENSE.txt
- https://cdn.jsdelivr.net/npm/@knight-lab/timelinejs@3.9.13/dist/css/timeline.css
- https://cdn.jsdelivr.net/npm/@knight-lab/timelinejs@3.9.13/dist/css/icons/tl-icons.woff2
- https://cdn.jsdelivr.net/npm/@knight-lab/timelinejs@3.9.13/LICENSE

Upstream source: https://github.com/NUKnightLab/TimelineJS3

TimelineJS is licensed under MPL-2.0; see `LICENSE`. Third-party notices from the JavaScript bundle are retained in `js/timeline.js.LICENSE.txt`. The WOFF2 icon font is unmodified. The JavaScript is loaded from the pinned CDN URL above, and is not copied into this repository. Tests use the same published npm version. The CSS's `tl-icons` font-face declaration is changed to reference only the locally bundled WOFF2 file at `icons/tl-icons.woff2`; unused legacy font formats are omitted. Site-specific styling lives in `atlas.css`.

The page requires jsDelivr for its JavaScript library, loads story/catalog data locally and supplies an in-memory TimelineJS configuration. No Google Sheets, media embeds, analytics ID, or remote font configuration is used.
