# Artemis configuration tiers

| Offering | System RAM | Included replaceable video card | Monitor alternatives |
|---|---|---|---|
| Artemis 128 | 64 × purchased 16 Kbit chips, 128 KiB | 16 KiB display DRAM + 1 KiB sprite SRAM; Aurelia controller | Logix Mono II / Logix Color II |
| Artemis 256 | 32 × AION 64 Kbit chips, 256 KiB | 32 KiB display DRAM + 1 KiB sprite SRAM; professional controller | Mono Pro / Logix Color II |
| Artemis PRO | Existing purchased high-density memory | Existing 32 KiB professional card | Existing console/headless offers |

Both cards contain the controller, display RAM, independent sprite SRAM and internal four-page pixel buffer. They use the dedicated replaceable-card connector. Host DMA, MMU and system refresh remain dedicated host components in the diagrams. Power off before replacement. The RAM selector changes the card shown throughout the Artemis explorer. Expansion of a low-density configuration does not automatically change its card.

The economy card connects the 32-bit host through byte staging to **8-bit local memory**. Eight 4116 chips provide 16 KiB; they cannot form a native 32-bit-wide 16 KiB memory array. The reused controller has four 40-byte pixel pages. It retains all Aurelia text/bitmap modes and five sprites in every mode. No 400-line modes are offered. The professional card retains four 160-byte pages and all 32 KiB modes. Only Mono Pro accepts its 26.88 kHz 640×400 raster; Color II continues to use legacy timings.

## Cost boundary and risk

The selected central AION 64 Kbit scenario assumes a 45 mm² die, 75 mm wafer and 0.85 maturity multiplier with the existing dated defect-density, wafer, packaging and test assumptions. It produces approximately $15.13 per chip in 1980 ($484.15 for 32) and $14.45 in 1981 ($462.49 for 32). The $462 selection is the 1981 estimate, not an undated launch price. Module PCBs, buffers, connectors, assembly and system testing are additional. AION supplies Artemis high-density configurations and, in the subsequent Aurelia+ sourcing revision, eight chips per Aurelia+; PRO sourcing remains unchanged.

This is an unproven manufacturing scenario. Retention, refresh, sense amplifiers, cell/process integration, speed bins, power rails, host bridge timing and board loading require qualification. The investment model adds 120 AION Labs person-months for DRAM development, 24 Logix person-months for hardware integration and 12 AION Software person-months for economy-card support. The model's existing prototype/mask allowance and fab-capacity calculations apply; recurring chip cost does not pay for development or factory capex.

## Pricing, demand and finance

Prices are rebuilt from the configured BOM using the existing balanced contribution/net-receipts and below-proxy rule. Current dated results are in [pricing](pricing.html) and [manufacturing costs](manufacturing-costs.html); no manually maintained duplicate totals are used here.

The sales mix is an assumption: 70% Artemis 128 and 30% Artemis 256, each with 80% monochrome and 20% Color II. Therefore 24% of Artemis units use Mono Pro. The prior display appeal uplift is scaled by 24/60 to 2.4% / 4.8% / 7.2% before the existing price-elasticity adjustment; it is not added again as a second marketing bonus. The $435,000 display campaign is retained. Monthly configuration allocations sum exactly to Artemis deliveries.

Sales feed manufacturing, fab loading, staffing, logistics and capacity with 10% good-output headroom. ROI incorporates revised prices, costs, demand, engineering and capital; the original tier comparison baseline was a19af421; the current ROI comparison tracks the subsequent Aurelia+ sourcing revision. These are scenario estimates, not historical accounts or demonstrated production yields.

Run the five normal builders (cost, pricing, sales, investment, ROI), followed by Python validators and JavaScript DOM tests. tools/apply_artemis_tiers.py is an idempotent migration; artemis_tiers.json records application of the policy.
