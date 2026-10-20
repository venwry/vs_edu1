# Artemis replaceable video card and Mono Pro

Every Artemis and Artemis PRO includes one replaceable video card on one dedicated keyed connector, in addition to four general-purpose expansion slots. Replacement requires power off. The networking NIC still occupies one general-purpose slot. Existing system DMA, MMU and bank/refresh circuitry remain host components; they are not duplicated on the video card. The hardware and memory diagrams expose these boundaries.

## Economy card (Artemis 128)

The 16 KiB card reuses the Aurelia controller, eight AION 4116 chips, two AION 2114 sprite SRAMs, four 40-byte pixel pages and two 160-byte row caches. A buffered bridge connects the 32-bit host to 8-bit local display memory; a CPU word write needs up to four local transfers. This is not native 32-bit display memory. Its modes match Aurelia: 40×25 and 80×25 text with 8×8 cells, plus six legacy bitmap modes. Each 8000-byte bitmap supports two pages; each 16000-byte bitmap supports one. It cannot drive Mono Pro. Canonical per-mode allocations are shown in the selected-card explorer tables.

See [ARTEMIS_TIERS.md](ARTEMIS_TIERS.md) for the configuration and sourcing policy.

## Professional card and monitor (Artemis 256 / PRO)

| Component | Accepted design |
|---|---|
| Display memory | 16 AION 4116-equivalent DRAMs, 16K × 16-bit organization, 32 KiB |
| Exclusive sprite memory | Two AION 2114-equivalent SRAMs, separate 8-bit bus, 1 KiB |
| Custom AION display controller | Parallel pixel renderer, memory/refresh arbitration, four 160-byte SRAM pages, serializer and sync |
| Pixel FIFO | 640 bytes; each page is 40 × 32-bit words. Eight 4-bit pixels load into a serializer latch every eight dot clocks; the SRAM is not read at the 21.504 MHz dot rate |
| Character-row caches | Two × 160 bytes on the controller, additional to the pixel FIFO |
| Sprites | Five 16×16, 4-bit, all five per scanline in every mode; transparent index zero |
| Sprite allocation | 640-byte patterns + 128-byte descriptor area (80 used, 48 padding) + 256-byte scratch; descriptors switch at vertical blank, patterns are not double buffered |
| Mono Pro CRT | Thorn–Brimar M36-141W, 14-inch monochrome bare tube; period candidate, qualification pending |
| Mono Pro raster | 640×400 progressive, 21.504 MHz dot clock, 800 dots/line, 448 lines/frame, 26.88 kHz horizontal, 60 Hz frame |
| Grayscale path | Four-bit index → AION 16-entry × 8-bit palette/receiver chip → external precision DAC ladder → external 25–30 MHz target amplifier → CRT |
| Analog assembly | Separate matched yoke, deflection, high voltage and mains supply; none is assumed included in the bare tube |

The [1978 Brimar industrial CRT catalog](https://www.worldradiohistory.com/Archive-Catalogs/Suppliers/Brimar-Industrial-Cathode-Ray-Tubes-1978-Volume-2.pdf) supports the period tube candidate. It does not establish our monitor's resolution, production yield or price. Focus, spot size, yoke matching, thermal performance, sync porches/polarity and safety require qualification.

Mono Pro is fixed-frequency. The card scales legacy modes to its 400-line raster. Older monitors receive only their advertised original 200-line timings; never the new 26.88 kHz raster. They are not generally described as incapable of progressive scanning: the distinction is the new frequency and raster. Identification failure blanks the output unless an explicit compatible profile is configured. New 200-line bitmap formats can also use capable older monitors; new 400-line text and bitmaps require Mono Pro.

## Professional card text modes

RAM per page includes padded character and attribute maps. Each character has 4-bit foreground and 4-bit background indices. All modes support two pages and one shared 256-glyph font; glyph editing affects both pages.

| Columns × rows | Cell | Logical pixels | RAM/page (B) | Shared font allocation (B) | Two pages + font (B) |
|---|---|---|---:|---:|---:|
| 40×25 | 8×8 | 320×200 | 2,048 | 2,048 | 6,144 |
| 80×25 | 8×8 | 640×200 | 4,096 | 2,048 | 10,240 |
| 80×25 | 8×16 | 640×400 | 4,096 | 4,096 | 12,288 |
| 80×40 | 8×10 | 640×400 | 8,192 | 4,096 | 20,480 |

The 80×40 maps contain 6,400 useful bytes in an 8,192-byte page allocation. Its font contains 2,560 useful bytes in 4,096 bytes using a 16-byte glyph stride.

## Professional card bitmap modes

| Logical pixels | Bits/pixel | Indexed colors | RAM/page (B) | Double buffer | Compatible raster |
|---|---:|---:|---:|---|---|
| 640×200 | 1 | 2 | 16,000 | Yes | Compatible legacy monitor or Mono Pro |
| 320×200 | 2 | 4 | 16,000 | Yes | Compatible legacy monitor or Mono Pro |
| 320×200 | 1 | 2 | 8,000 | Yes | Compatible legacy monitor or Mono Pro |
| 320×100 | 4 | 16 | 16,000 | Yes | Compatible legacy monitor or Mono Pro |
| 320×100 | 2 | 4 | 8,000 | Yes | Compatible legacy monitor or Mono Pro |
| 160×100 | 4 | 16 | 8,000 | Yes | Compatible legacy monitor or Mono Pro |
| 640×400 | 1 | 2 | 32,000 | No | Mono Pro only |
| 640×200 | 2 | 4 | 32,000 | No | Compatible legacy monitor or Mono Pro |
| 320×400 | 2 | 4 | 32,000 | No | Mono Pro only |
| 320×200 | 4 | 16 | 32,000 | No | Compatible legacy monitor or Mono Pro |

The 32,000-byte modes leave 768 bytes free. Background/font allocations never consume sprite SRAM. Compatibility means display modes and the documented API, not automatic native execution of Z80 applications.

## Production and financial assumptions

The enlarged controller is modeled at 80 mm², with a 60–110 mm² planning range and approximately 65,000–95,000 transistors, including 960 bytes of internal SRAM. This is not a measured layout. At the repository's existing 75 mm wafer/defect assumptions, the central 1980 die yield is only 12.36%, giving about $67.79 recurring cost per packaged controller before final OEM fulfillment. It is a significant yield/cost risk, not a claim of effortless fabrication. The 21.504 MHz serializer and full-load memory scheduling need corner testing and a respin allowance. Keeping analog circuitry external reduces mixed-process risk; the digital die remains large.

Display fetches and refresh have reserved deadlines. Host DMA/upload requests wait; neither CPU HALT nor a long DMA transfer may stop display refresh. Completed-page ownership prevents the renderer overwriting the page being displayed. An underflow blanks affected pixels and records a fault while maintaining sync. PCB power distribution, 4116 multi-rail sequencing, connector loading and maximum sprite/text traffic remain qualification gates.

The recurring-cost model separately counts card PCB, dedicated connector pair, host buffers, clocks/transceivers, DRAM, SRAM, controller and assembly/test. The monitor separately counts its bare tube, yoke, HV/deflection/PSU, receiver, ladder, amplifier, PCB, case, harnesses, calibration and packout. No original video-chip or eight-chip memory-set charge remains in the motherboard. Each bundle contains one card through its host assembly.

Artemis 128 includes the 16 KiB economy card and Mono II or Color II. Artemis 256 includes the 32 KiB professional card and Mono Pro or Color II. PRO console offers retain the professional card and Mono Pro; server-only PRO offers remain available. PRO shipments remain unconfirmed; the industrial model conditionally starts them in July 1981, with no PRO revenue before the end-1980 ROI cutoff.

Prices balance contribution/net receipts against discount below the proxy using P = sqrt(C × B / (1 − fee)). Mono Pro's $450/$425 comparator envelope is an unverified assumption, not a historical matching quote. New workstation proxies replace the old display allowance; server-console proxies add keyboard and display. Standalone replacement-card pricing has no matched proxy and uses the disclosed 25% contribution fallback. Corporate development, marketing and capex are assessed in ROI, not called unit manufacturing profit.

The sales scenario assumes 24% Mono Pro uptake among Artemis packages and 30% among conditional 1981 PRO offers. Combined product appeal and incremental campaign uplift is 2.4%/4.8%/7.2% on Artemis buyer intentions, applied once before price elasticity. This is assumed, not measured. Higher prices can offset greater interest. The $435,000 incremental campaign covers new creative, regional commercials, press, dealer demonstrations and incremental NCC/COMDEX staging; original Artemis event budgets are not charged twice.

Display engineering is 150 person-months: AION Labs 90 (72 card, 18 receiver), Logix 36 (card/monitor integration and qualification), AION Software 24 (drivers, fonts, mode discovery and compatibility). The tier revision adds 156 person-months: AION Labs 120 for the 64 Kbit DRAM, Logix 24 for modules/economy-card integration, and AION Software 12 for the economy driver. Total incremental engineering is 306 person-months. Existing chip/process and OS programmes remain separately funded. Prototype/mask/validation expenditure follows the investment model's existing engineering-cost allowance. Recurring assembly staffing, chip loading and capacity are recomputed from the BOM.

Capacity retains 10% good-output headroom. Added card assembly and monitor calibration affect stations; larger monitor packout affects warehouse/linehaul allowances; extra PCB area and explicit chip counts affect supplier and fab requirements. These physical allowances are planning estimates. No separate replacement-card sales volume is invented.

See [pricing](pricing.html), [sales](sales.html), [manufacturing costs](manufacturing-costs.html), [industrial investment](industrial_investment_1974_1981.html) and [ROI](roi.html). The ROI page includes a before/after comparison of this entire revision; accounting ROI is distinct from cash payback. The historical delivery ramp in the sales page and the full-demand capacity scenario in ROI are explicitly separate.

## Regeneration and checks

Run the five existing builders in order: cost assessment, pricing, sales, investment, ROI. Policy inputs are in `artemis_display_revision.json`; the prior-model comparison is frozen in `artemis_display_baseline.json`; `artemis_display_impact.json` is rebuilt with ROI. Validate with `tests/validate_artemis_video.py`, the existing Python validators and JavaScript DOM tests. No simulated check establishes physical electrical qualification.
