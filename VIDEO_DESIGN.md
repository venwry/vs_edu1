# Unified Aurelia video design

Catalog 2.15 replaces the former custom random-plus-serial memory design with one shared controller and eight AION-manufactured 4116-equivalent 16Kx1 NMOS DRAM chips, providing 16 KiB on both computers. Launch dates and system RAM remain unchanged. This is an accepted specification, not a claim that electrical qualification is complete.

Both hosts implement 40x25 and 80x25 text with 256 writable 8x8 glyphs and 4-bit foreground/background indices. Two text pages share one 2 KiB font. Five 16x16, 4-bit sprites require 640 bytes of patterns and 20 bytes of X/Y coordinates total; reserve 768 bytes. Index zero is transparent only for sprites. Both text modes support two pages plus all five sprites.

| Bitmap | Bytes per page | Supported configurations |
|---|---:|---|
| 640x200x1 | 16000 | One page, no sprites |
| 320x200x2 | 16000 | One page, no sprites |
| 320x200x1 | 8000 | One page; two pages without sprites; or one page with five sprites |
| 320x100x4 | 16000 | One page, no sprites |
| 320x100x2 | 8000 | One page; two pages without sprites; or one page with five sprites |
| 160x100x4 (retained compatibility mode) | 8000 | One page; two pages without sprites; or one page with five sprites |

The remaining 384 bytes in a 16000-byte allocation do not enable a reduced sprite mode. Sprite coordinates use logical mode pixels and scale with the picture. All five sprites may overlap one scanline; lower sprite number wins. Page and position changes latch at vertical blank. Shared-font and sprite-pattern edits require separate synchronization.

The custom controller contains two 160-byte character/attribute row caches (current and prefetched next row), 40 bytes of sprite shifters, 40 bytes of sprite staging and four 40-byte pixel FIFO banks: 560 bytes total. The FIFO holds completed 4-bit colour indices, including sprite composition; it is not additional addressable display RAM. The renderer and scanout sequencer are dedicated hardware engines on one master clock, not general-purpose CPUs. Glyph bytes expand to eight coloured pixels per block. Sprite rows are prefetched and composed with fixed priority.

The four FIFO banks follow circular raster order with FREE/FILLING/READY/READING ownership. Each bank holds 80 pixels. Only complete banks are published, each has an output latch, the producer stops when full, and scanout starts after prefill. At 14.31818 MHz, all four banks hold 22.35 microseconds of pixels; two ready banks provide 11.17 microseconds plus the current bank remainder. Underrun emits border colour and sets sticky diagnostic status while sync continues. Banks use addressed storage, not a physically shifting 160-byte register.

Eight external AION 4116-equivalent 16Kx1 DRAM chips form one 16KiB, 8-bit memory bank. They have one random read/write port and no serial-output register. All glyph, sprite, bitmap, host and refresh accesses share the DRAM bus with bounded CPU waits. Character codes/colours are cached across eight glyph scanlines, while the next row is prefetched into the second cache. An illustrative worst-overlap text budget averages 80 glyph + 20 next-row + 40 sprite reads = 140 reads, or 52.5 microseconds at a 375ns cycle. This is not a local deadline proof. Validate cache transitions, FIFO refill, startup, refresh and host writes together; a faster qualified grade or page-mode schedule may be required. Repeated bitmap lines may be fetched again; no extra full scanline store is assumed. In particular, validate 320x100x4 throughput including line repetition.

The main RAM remains external. The 4116-compatible target uses a 16-pin DIP and +12V/+5V/-5V rails; final ordering code, electrical compatibility and speed grade remain qualification gates. Purchased system RAM (`part.dram_16kbit`) is distinct from internally manufactured display RAM (`part.aion_4116`). Existing `vram_policy`, `reserved_vram_bytes` and `remaining_vram_bytes` keys retain their generic video-memory allocation meaning for API compatibility; they do not describe dual-port silicon.

The existing Control pair becomes bidirectional for monitor capability discovery. Fixed raster profiles target 320x200 at 7.15909 MHz and 640x200 at 14.31818 MHz, with equal line/frame rates. Monitor I models advertise the 320 profile; Monitor II models target both. These are design requirements pending OEM bandwidth, sync and readability qualification. Both text widths are native to both computers; firmware exposes only modes supported by the connected monitor. Pixels/lines repeat by integer factors; unsupported downscaling is rejected. Mono I requires host index-to-luminance mapping because its DAC has no programmable palette.

Packet encoding, control turnaround/timing, connector, voltage, termination, sync widths and porches remain electrical release gates. The launch baseline requires video RAM process development and worst-case fetch validation before June 1978; no new historical event date or completed fabrication milestone is asserted.

Manufacturing estimates assume process-matched laser-written masks and AION fabrication on 75mm wafers. The controller is estimated at 40,000–50,000 transistors (central 45,000), 40–60mm² at 3µm (central 48), or 55–80mm² at 3.5µm (central 65). The ordinary DRAM planning range is 16–20mm² per die, central 18 at 3µm. These are not measured layouts. A six-device-per-storage-bit accounting model informs the controller estimate but does not substitute for a qualified NMOS cell design.

The reproducible recurring-cost model uses $210 per processed wafer in 1978, `die_yield = 0.85 * exp(-2.8 * area_mm2 / 100)` for these parts, then 93% package/test yield. The 48mm² controller has 22.17% wafer-test yield, 20.62% final saleable yield and costs $18.743. The 18mm² DRAM has 51.35% wafer-test yield, 47.75% saleable yield and costs $3.4452 each; eight cost $27.5618. The complete chipset is **$46.30**, approximately **$47** as a rounded planning allowance, in nominal 1978 USD. Later-year values are regenerated by `tools/build_cost_assessment.py` using the existing annual defect-density and wafer-cost assumptions. Speed-bin losses beyond this model remain unquantified.

This replaces the former detailed-model $43.81 chipset and supersedes the older conversational $65 stabilized / $130 ramp allowances. It does not apply a new ramp allowance to every shipment. Development, extraordinary startup expenses, capital depreciation, secret-facility costs and board/monitor electronics are excluded. The scenario assessment is separate from unquoted BOM `unit_cost` fields, which remain null. Ordinary DRAM still requires capacitor, sensing, retention and refresh qualification; AION must still fabricate all eight RAM dies. The redesign does not eliminate RAM wafer demand or the memory-process programme.

The shared-controller Apple II and S-100 cards inherit this silicon change. Artemis has a distinct controller; its existing unresolved 16KiB storage cost proxy follows the replacement AION DRAM part, without asserting that its architecture is now the Aurelia controller.
Run `python tests/validate_video.py` alongside the catalog/BOM validators and existing DOM tests. Resource arithmetic does not establish silicon timing or production yield.



## NCC 1979 third-party-host video cards

Apple II and S-100 video cards reuse the Aurelia-family controller, eight AION-manufactured 4116-equivalent 16Kx1 DRAMs and the Logix digital video interface. Each carries 16 KiB onboard display memory; this is not host general-purpose RAM. Host bus adapters, window/addressed video RAM access, software and electrical qualification are card-specific. Mode availability requires a compatible monitor; 80 columns requires the 640-pixel raster. Native Apple applications must use the card library or an explicit adaptation; existing display writes are not transparently redirected. These cards add no CP/M execution capability.

AION supplies June 1979 silicon; SMC transfer starts July 1978 and qualified independent chips become available from October 1979, subject to individual release. Process-compatible masks, test structures, process know-how and engineering assistance are transferred; arbitrary AION masks are not assumed drop-in compatible with SMC equipment.
