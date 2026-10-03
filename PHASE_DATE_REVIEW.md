# Phase assignments and date review

All 41 story events have year/month precision, a conference/range date, or an unspecified date. The table reviews all of them so that known ranges are distinguished from missing dates. Proposed months, dates and intervals are editorial suggestions, not sourced historical facts, and are **not applied** to the operative story or technical catalog.

Phase assignment uses the existing narrative date, then an exact matching launch date already in the technical catalog, then the original narrative context for undated events. Explicit intervals are assigned by their start. The 2025 causal prologue is the exception and stays associated with phase one. Same-year/month ambiguity is resolved by the narrative context; it does not assert a new day. Development events with no dates retain their pre-NCC-1980 context provisionally in phase five.

## Requested phases

| Phase | Inclusive dates | Title | Events |
|---|---|---|---:|
| 1 | 1972-01-01 – 1974-12-31 | Adam studying and investing on stock market | 6 |
| 2 | 1975-01-01 – 1978-06-04 | Preparing first products and their ecosystem | 10 |
| 3 | 1978-06-05 – 1979-06-03 | Aurelia premiere and first months of sales | 11 |
| 4 | 1979-06-04 – 1979-12-02 | Apple extensions and market expansion | 5 |
| 5 | 1979-12-03 – 1980-05-18 | Aurelia+ and Pulse premiere Abacus 2.0 | 6 |
| 6 | 1980-05-19 – 1980-11-18 | Artemis launch, compatibility card and recompiled products | 1 |
| 7 | 1980-11-19 – 1981-05-03 | Abacus and Pulse 3.0 for Artemis | 1 |
| 8 | 1981-05-04 – 1981-11-18 | Artemis Pro, Networking and new BPI | 1 |

## Date review

| Event | Assigned phase | Current story date | Proposed date or interval | Basis / caveat |
|---|---:|---|---|---|
| `event.power` — Vincent gains time-travel powers | 1 | 2025 | 2025 (retain year precision) | Origin outside the historical phases; selecting a day adds no useful information. |
| `event.identity` — Arrival and assumption of Adam’s identity | 1 | 1972-01 | 1972-01 (retain month precision) | The arrival month is known; no basis for choosing a particular day. |
| `event.lottery` — Lottery win and move to the US | 1 | After January 1972; exact date unspecified | 1972-02 to 1972-08 | Allows the German lottery win and US relocation after January and before the proposed autumn studies. |
| `event.harvard` — Economics studies and NYSE speculation | 1 | After relocation to the US | 1972-09 to 1974-12 | Suggested study/investment interval before the company-building phase; no graduation date is asserted. |
| `event.office` — Investment-data office established | 1 | 1973 | 1973-01 | Suggested start of the data office during the first study year. |
| `event.exchanges` — Investment activity expands internationally | 1 | 1973–1975 (display currently says 1973) | 1973 to 1975 (retain range) | Already an explicit multi-year activity; spans phases one and two and is assigned by start. Display currently misleadingly says only 1973. |
| `event.companies` — Three technology companies founded | 2 | Late 1975 | 1975-11 | Fits the explicit late-1975 qualifier; phase two starts earlier than the founding event. |
| `event.facility` — Secret future-equipped facility established | 2 | Before product development; exact date unspecified | 1975-12 | After company formation and before the proposed engineering setup. |
| `event.setup` — Build the engineering and manufacturing organizations | 2 | Before NCC 1978 | 1976-01 to 1978-06-04 | Allows organizational buildup and product preparation ahead of launch. |
| `event.letwin` — Gordon Letwin recruited | 2 | 1977-06 | 1977-06 (retain month precision) | Month already explicit; no need to invent a hiring day. |
| `event.paterson` — Tim Paterson recruited | 2 | 1977 | 1977-07 | Suggested recruitment shortly after Letwin; their relative order is not established. |
| `event.dri_cpm` — CP/M development cooperation | 2 | Before NCC 1978; exact signing date unspecified | 1976-09 | Allows substantial CP/M/TUI/FlexiBUS work before June 1978. |
| `event.mpi` — OEM printer-mechanism agreement | 2 | Before NCC 1978 | 1977-09 | Allows printer mechanism/controller integration before launch. |
| `event.retail` — ComputerLand retail agreement | 2 | Before NCC 1978 | 1978-02 | Allows distribution preparation ahead of the Academy and June launch. |
| `event.bpi_offer` — Offer to establish AION BPI Systems | 2 | Early 1977 | 1977-02 | Fits early 1977 and leaves time for the BPI port; remains an offer. |
| `event.academy` — Logix Computer Academy established | 2 | 1978-03 | 1978-03 (retain month precision) | Already recorded at month precision in story and catalog. |
| `event.aurelia_launch` — Aurelia platform launches | 3 | 1978-06 | 1978-06-05 | Exact launch date already in the computer catalog; used only as a placement anchor. |
| `event.bpi_launch` — BPI suite presented for Aurelia | 3 | NCC June 1978 | 1978-06-05 | Exact introduction date already in the BPI catalog; used only as a placement anchor. |
| `event.bpi_training` — BPI training and direct sales begin | 3 | A few days after NCC June 1978 | 1978-06-12 | Suggested service start a few days after the premiere. Catalog currently groups the training introduction under 5 June; distinguish presentation from actual service availability. |
| `event.dri_portable` — DRI commits to portable TUI extensions | 3 | Late 1978 | 1978-11 | Fits late 1978 and the May 1979 release. |
| `event.apple_search` — Apple seeks business-software partners | 3 | By 1979 | 1978-10 | Places the partner search before the proposed Peachtree agreement and by 1979. |
| `event.others_monitor` — Other companies monitor the market | 3 | Post-NCC 1978 response period | 1978-06-05 to 1979-06-03 | Ongoing observation across the post-launch response phase, not a one-day event. |
| `event.market_growth` — US personal-computer market expands | 3 | Post-NCC 1978 response period | 1979-05 | Suggested assessment date for the accumulated post-Aurelia market effect. |
| `event.basic_develop` — Microsoft BASIC developed with AION | 3 | Before NCC June 1979 | 1978-09 to 1979-05 | Development interval ending before the June 1979 presentation. |
| `event.dri_release` — Portable CP/M extensions released | 3 | 1979-05 | 1979-05 (retain month precision) | Release month already explicit. |
| `event.apple_peachtree` — Apple partners with Peachtree | 3 | Between November 1978 and June 1979 | 1979-01 | Within the stated November 1978–June 1979 interval and after the proposed partner search. |
| `event.apple_cooperation` — Logix and Apple agree limited technical cooperation | 3 | 1979-02 | 1979-02 (retain month precision) | Agreement month already explicit. |
| `event.apple_extensions` — Apple II expansion products demonstrated | 4 | 4–7 June 1979 | 1979-06-04 to 1979-06-07 (retain conference range) | This is a known conference interval, not a missing date. Catalog introduction is 4 June; actual demonstration day is unspecified. |
| `event.basic_launch` — Microsoft BASIC presented | 4 | NCC, 4–7 June 1979 | 1979-06-04 | Catalog introduction is 4 June; story currently gives the 4–7 June conference window. |
| `event.apple_policy` — Apple continues limited compatibility cooperation | 4 | After NCC 1979 | 1979-06-08 to 1979-12-02 | Ongoing post-NCC policy during phase four, not a single action date. |
| `event.ibm_investigate` — IBM investigates the personal-computer market | 4 | 1979 | 1979-07 to 1979-11 | Fits the post-NCC context and precedes the proposed IBM project start. |
| `event.plus_launch` — Aurelia+, Pulse and Abacus 2.0 arrive | 4 | 1979-11 | 1979-12-03 (requires changing November 1979 in story and catalog) | Resolves the conflict with phase five’s title/start. Until accepted, the recorded November launch remains in phase four. |
| `event.ibm_project` — IBM starts its personal-computer project | 5 | After the 1979 investigation, before May 1980 | 1979-12 | Fits after the proposed investigation and before May 1980; remains a project plan. |
| `event.apple_business` — Apple–Peachtree small-business package starts | 5 | 1980-03 | 1980-03 (retain month precision) | Month already explicit. |
| `event.artemis_engineering` — Artemis and ERA1 engineering | 5 | Before NCC May 1980; exact start unspecified | 1978-07 to 1980-05-18 | A longer engineering interval is more plausible than beginning in late 1979. If accepted, assign by start to phase three and show its span through phase five. |
| `event.aionix_agreement` — AIONix development and ownership agreement | 5 | Before NCC May 1980 | 1978-09 | Suggested early agreement to allow OS work alongside Artemis engineering; if accepted, move to phase three. |
| `event.cpm_bridge` — CP/M-80 compatibility module developed | 5 | Before NCC May 1980 | 1979-06 to 1980-05-18 | Suggested development interval before commercial availability on 19 May 1980; if accepted, assign by start to phase four. |
| `event.artemis_software` — Artemis software and development tools prepared | 5 | Before NCC May 1980 | 1979-06 to 1980-05-18 | Suggested preparation interval for native tools and ports; if accepted, assign by start to phase four. |
| `event.artemis_launch` — Artemis platform launches commercially | 6 | 1980-05 | 1980-05-19 | Exact launch date already in the computer catalog; used only as a placement anchor. |
| `event.software32` — AION shifts major software development to 32-bit Artemis | 7 | 1980-11 | 1980-11-19 | Exact Abacus 3.0/Pulse 3.0 introduction date already in the catalog; used only as a placement anchor. |
| `event.network_launch` — Networked business-computing platform presented | 8 | 1981-05 | 1981-05-04 | Exact Artemis PRO/networking introduction date already in the catalog; used only as a placement anchor. |

## Unresolved mismatch

The recorded Aurelia+/Pulse/Abacus 2.0 premiere is November 1979 in both story and technical catalog. It therefore belongs to phase four (ending 2 December), even though phase five is titled for that premiere. Moving it to 3 December would require a separate coordinated revision of catalog introductions, platform availability, and narrative dates. No such revision is applied here.

The compatibility-card development and software preparation events belong before the Artemis launch; the catalog already places commercial introduction of the corresponding new products at 19 May 1980. Product launch dates must not be reused as development-start dates.
