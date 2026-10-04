# Unified Aurelia video design

Catalog 2.7 replaces the separate 8 KiB Aurelia and incompletely defined Aurelia+ controller designs with one shared controller and eight custom 16Kx1 NMOS random-plus-serial VRAM chips, providing 16 KiB on both computers. Launch dates and system RAM remain unchanged. This is an accepted specification, not a claim that electrical qualification is complete.

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

The controller contains a 160-byte character/attribute row cache, 40 bytes of sprite shifters, a 40-byte sprite staging bank and a 16-byte bitmap FIFO. Arbitration covers serial row transfers, random glyph/sprite reads, full-array refresh and CPU accesses with wait states. Repeated lines may be re-fetched; no full scanline buffer is assumed. These buffers are included in die/transistor estimates.

The existing Control pair becomes bidirectional for monitor capability discovery. Fixed raster profiles target 320x200 at 7.15909 MHz and 640x200 at 14.31818 MHz, with equal line/frame rates. Monitor I models advertise the 320 profile; Monitor II models target both. These are design requirements pending OEM bandwidth, sync and readability qualification. Both text widths are native to both computers; firmware exposes only modes supported by the connected monitor. Pixels/lines repeat by integer factors; unsupported downscaling is rejected. Mono I requires host index-to-luminance mapping because its DAC has no programmable palette.

Packet encoding, control turnaround/timing, connector, voltage, termination, sync widths and porches remain electrical release gates. The launch baseline requires VRAM process development and worst-case fetch validation before June 1978; no new historical event date or completed fabrication milestone is asserted.

Manufacturing estimates assume laser-written masks and an average 1978 AION wafer facility: controller 25000–40000 transistors, 30–50 mm² at 3 µm or 40–65 mm² at 3.5 µm, and 20–45% stabilized saleable yield. Each custom VRAM is provisionally 20000–25000 transistors and 15–30 mm². These are planning estimates, not measured results.

The conversation's illustrative nine-chip cost allowance is $65 stabilized or $130 during ramp in nominal 1978 USD, excluding development, exceptional startup costs, secret-facility costs and board/monitor electronics. This is not a supplier quote or a released BOM unit cost. BOM prices remain null and full cost rollups remain blocked pending qualification and routing data.

Run `python tests/validate_video.py` alongside the catalog/BOM validators and existing DOM tests. Resource arithmetic does not establish silicon timing or production yield.
