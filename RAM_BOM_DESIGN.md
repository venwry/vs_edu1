# RAM and BOM baseline

This branch applies the accepted RAM correction and adds manufacturing requirements to the catalog. It provides a starting structure for costing, not a priced or electrically qualified production BOM. Capacity labels in the existing JSON use `kb`; RAM quantities below are binary KiB. Chip densities use Kbit.

## Shipping RAM populations

| Product | System RAM | DRAM organization | Chips | Modules | Populated banks |
|---|---:|---|---:|---:|---:|
| Aurelia | 48 KiB | 16K × 1 | 24 | Mainboard | 3 × 8-bit |
| Aurelia optional card | 16 KiB additional | 16K × 1 | 8 | One expansion card | 1 × 8-bit |
| Aurelia+ | 64 KiB | AION 64K × 1 | 8 | Mainboard | 1 × 8-bit |
| Artemis | 128 KiB | 16K × 1 | 64 | 4 × 32 KiB | 2 × 32-bit |
| Artemis | 256 KiB | AION 64K × 1 | 32 | 2 × 128 KiB | 1 × 32-bit |
| Artemis PRO | 512 KiB | 64K × 1 | 64 | 4 × 128 KiB | 2 × 32-bit |
| Artemis PRO | 1 MiB | 64K × 1 | 128 | 8 × 128 KiB | 4 × 32-bit |

The 1 MiB configuration occupies all eight sockets and all four banks. Each module has sixteen one-bit DRAM chips and supplies a 16-bit word. Two matched modules supply a full 32-bit bank. Baseline modules have no parity; byte parity would require eighteen chips per module and additional control/error handling.

The first design prohibits mixing module densities within a chassis. Populate complete pairs in consecutive banks. The 64 KiB low-density bank kit contains two 32 KiB modules; the 256 KiB high-density kit contains two 128 KiB modules. Artemis can reach 256 KiB using eight low-density modules or two high-density modules; these are separate explorer choices. Further high-density expansion reaches a 1 MiB design target, pending electrical qualification. Upgrading density replaces the existing population.

video RAM and the Z80 compatibility module's RAM are separate memory pools. Existing 24-bit physical addressing, 32-bit virtual addressing and 4 KiB pages remain unchanged. Address ranges, module connectors, refresh, byte enables, wait states, loading and timing require engineering definition. A full-width bank does not imply zero-wait operation.

The unqualified 128 Kbit DRAM record and old 8-bit 64 KiB RAM module are retained as superseded history and excluded from active BOMs. Exact 16K × 1 and 64K × 1 manufacturer parts, rail requirements, speeds and period supply must be qualified; density alone is not a sourcing specification.

## Manufacturing coverage

`hardware_bom.json` covers all active hardware and offered bundles; validators reconcile coverage and recursive assembly contents. Assemblies include catalog parts and unresolved implementation requirements. Counts describe engineering records, not unique purchasable SKUs.

Every hardware catalog record now includes manufacturing requirements. Active records link to assembly IDs. Nested assemblies separate purchased mechanisms from their host systems and prevent counting both a functional assembly and its implementation as independent purchased items. Unknown quantities remain null, rather than zero or an invented count. Superseded records retain their historical identity.

The additions cover:

- Computers: mainboards, DRAM population, video RAM/ROM definition, control/buffering, connectors, power, chassis, cooling, drive mechanisms, wiring and assembly requirements.
- RAM and expansion products: module/card PCB, chips, buffers/control, connectors, decoupling, mounting and validation requirements.
- Displays, printers and storage: OEM mechanism boundaries, control electronics, power, enclosures, cables, consumables and calibration/test requirements.
- Networking: removable NIC assemblies, occupied host slots, hub port variants, connectors, cabling and power.
- Base parts and custom silicon: implementation, package, fabrication, qualification and test requirements.
- Bundles: host configuration, peripherals, physical software media and packaging; upgrade kits do not implicitly include a computer.

Networking-era Artemis configurations add one removable NIC. PRO includes one NIC. The later server-OS cartridge replaces the base OS cartridge in applicable bundle variants; it is not counted as a second required OS cartridge.

## Decisions required before costing

The BOM's `open_decisions` and per-product requirements preserve the remaining work: exact DRAM suppliers and electrical qualification; the physical memory map; drive/display OEM selection; video RAM electrical qualification and ROM organization; the video-link electrical specification; custom-silicon implementation and yields; PRO console packout or validated headless operation; and the controller die count and electrical qualification for three FlexiBUS ports on both Aurelia models.

`costing_inputs` separates direct materials, conversion labor/test/rework, factory overhead, NRE/capital and commercial costs. Before calculating totals, define supplier quote dates and volume tiers, quantities, assembly routing and minutes, programming/calibration, scrap and yield, fixtures, utilization and overhead allocation. Prices and all unresolved inputs remain null. The later manufacturing-cost model supplies explicit planning estimates for unresolved quantities; these are not supplier quotations.

## Validation

Run the catalog validator, the hardware BOM validator and the existing DOM suite as documented in ATLAS_README.md. Checks cover schema and references, complete hardware/offer coverage, recursive assembly cycles, DRAM arithmetic, paired-bank population, shipping configurations, networking count and OS replacement. DOM checks exercise both low- and high-density 256 KiB configurations and PRO's four-bank 1 MiB configuration. They do not establish electrical feasibility or replace browser visual review.


## Unified Aurelia video (v2.7)

Both Aurelia models now populate one shared video controller, eight AION-manufactured 4116-equivalent DRAM chips (16 KiB), two AION 2114-equivalent SRAMs (1 KiB exclusive sprites) and one AION system controller for DMA/banking/refresh. See VIDEO_DESIGN.md for mode allocations, monitor discovery and manufacturing estimates. Run `python tests/validate_video.py` to verify every buffer/sprite allocation and the eleven-chip video population and single system-controller BOM. These quantities are defined; electrical qualification and unit-cost quotations remain open.


## Artemis replaceable video and Mono Pro

See [ARTEMIS_VIDEO_CARD.md](ARTEMIS_VIDEO_CARD.md) for the 16/32 KiB configuration-specific cards, dedicated 1 KiB sprite SRAM, four pixel-buffer pages, 640×400 Mono Pro, new complete offers and qualification limits. Costs, balanced pricing, demand, engineering, marketing, capacity and ROI are rebuilt together; [ROI](roi.html) includes the current before/after comparison.
