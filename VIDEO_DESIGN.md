# Aurelia video and dedicated sprite memory

Both Aurelia and Aurelia+ use the same video controller, eight AION 4116-equivalent 16Kx1 DRAMs (16 KiB display RAM), and two AION 2114-equivalent 1Kx4 SRAMs (1 KiB exclusive sprite RAM). The SRAM has its own 8-bit bus to the video controller. These are accepted design requirements; electrical timing, layout and production qualification remain open.

All modes below support five overlapping 16x16, 4-bit sprites. Sprite storage does not reduce display RAM. Text uses 256 writable 8x8 glyphs and 4-bit foreground/background indices. RAM per text page includes the padded character and colour maps; one 2048-byte font is additional and shared by both pages.

| Text mode | Pixels | RAM per page (bytes) | Shared font (bytes) |
|---|---|---:|---:|
| 40x25 | 320x200 | 2048 | 2048 |
| 80x25 | 640x200 | 4096 | 2048 |

Both text modes support two pages. Total display allocation is `page_count * ram_bytes_per_page + font_bytes`: 4096/6144 bytes for one/two 40-column pages, or 6144/10240 bytes for one/two 80-column pages.

| Bitmap mode | Stride (bytes) | RAM per page (bytes) | Double buffering |
|---|---:|---:|---|
| 640x200x1 | 80 | 16000 | No |
| 320x200x2 | 80 | 16000 | No |
| 320x200x1 | 40 | 8000 | Yes |
| 320x100x4 | 160 | 16000 | No |
| 320x100x2 | 80 | 8000 | Yes |
| 160x100x4 (compatibility) | 80 | 8000 | Yes |

A full 16000-byte background or two 8000-byte backgrounds leave 384 bytes of display DRAM. Text/font and bitmap allocations are alternative uses of display RAM; mode switches reload fonts/redraw. Sprite SRAM remains available throughout.

## Exclusive sprite SRAM

640 bytes hold five 128-byte patterns. Two banks of five 8-byte descriptors occupy 80 bytes; 304 bytes remain reserved. Descriptors include signed 16-bit X/Y, enable and reserved controls. Switch the active descriptor bank at vertical blank for atomic position/enable updates. The 1 KiB bank does not contain two complete pattern sets: pattern changes require scheduled writes or disabling affected sprites. Lower sprite number wins; index zero is transparent for sprites. Coordinates use logical pixels and scale with the background.

CPU and DMA use auto-incrementing video upload ports with target-ready backpressure. Sprite SRAM reads and writes are arbitrated on the separate bus. Two 18-pin, +5 V SRAM packages target 250 ns cycles, subject to process and electrical qualification; no refresh is required.

## Rendering and timing

The controller retains two 160-byte character/attribute row caches, 40-byte sprite shifters, 40-byte sprite staging and four 40-byte completed-pixel FIFO banks: 560 bytes of internal storage. Renderer and scanout are dedicated hardware engines sharing one master clock. FIFO banks hold completed 4-bit colour indices and follow circular FREE/FILLING/READY/READING ownership with complete-bank publication, output latches, prefill and backpressure. Underrun continues sync, emits border colour and sets diagnostic status.

At 14.31818 MHz the FIFO holds 22.35 microseconds of pixels; two ready banks hold 11.17 microseconds. Glyph expansion creates eight pixels per fetched byte. In 80-column text, 80 glyph reads plus an average 20 next-row prefetch reads consume 37.5 microseconds at a 375 ns DRAM cycle. Separately, 40 sprite pattern bytes take 10 microseconds at 250 ns per SRAM cycle. Descriptor reads, cache transitions, startup, refresh, uploads and local FIFO deadlines still require a complete schedule. Average throughput is not a timing proof. Repeated bitmap lines may be fetched again; validate 320x100x4 explicitly.

The video controller refreshes every row of its eight ordinary single-port DRAMs, including hidden pages. The system controller independently refreshes system DRAM; see [AURELIA_SYSTEM_CONTROLLER.md](AURELIA_SYSTEM_CONTROLLER.md). The 4116-compatible target uses +12V/+5V/-5V rails and a 16-pin DIP. Qualified ordering codes, retention, speed, power and package pinouts remain release gates.

## Monitor and interface contract

The bidirectional Control pair discovers monitor capabilities. Fixed raster profiles target 320x200 at 7.15909 MHz and 640x200 at 14.31818 MHz with equal line/frame rates. Monitor I supports the 320 profile; Monitor II targets both. Both computers have native 40/80-column text, but firmware exposes only modes supported by the connected monitor. Integer repetition is supported; unsupported downscaling is rejected. Mono I uses host index-to-luminance mapping. Connector, voltage, sync widths/porches, turnaround and OEM readability remain qualification gates.

## Manufacturing and integration

The recurring model assumes 75 mm wafers and 3 micron NMOS: 52 mm2 central video-controller die, 18 mm2 per 4116 DRAM and 20 mm2 per 2114 SRAM. Video-controller transistor planning is 44,000–56,000, central 49,000; these estimates are not measured layouts. The 3.5 micron sensitivity requires a larger die and a separate cost/capacity run.

At 1978 assumptions ($210 processed wafer, die yield `0.85 * exp(-2.8 * area_mm2 / 100)`, 93% final package/test yield), the video chip costs $22.5629, eight DRAMs $27.5618, and two SRAMs $7.7784: about $57.90 for the eleven-chip video population. Incremental package/interface/PCB/test allowance is $7.40 at assembly level. Speed-bin losses, initial design/masks and capital are excluded from recurring chip costs. The industrial model separately budgets extension engineering and computes wafer loading from the revised BOM.

Apple II and S-100 video cards inherit the same sprite SRAM and modes because they reuse this controller. Host adapters and drivers remain specific; these cards do not contain the Aurelia system controller and do not add CP/M execution capability. Existing SMC agreements do not automatically qualify newly added SRAM or system-controller parts.

Run catalog/BOM, video, costs, investment and DOM validators. Passing arithmetic and rendering checks does not establish production timing or yield.


## Artemis replaceable video and Mono Pro

See [ARTEMIS_VIDEO_CARD.md](ARTEMIS_VIDEO_CARD.md) for the 16/32 KiB configuration-specific cards, dedicated 1 KiB sprite SRAM, four pixel-buffer pages, 640×400 Mono Pro, new complete offers and qualification limits. Costs, balanced pricing, demand, engineering, marketing, capacity and ROI are rebuilt together; [ROI](roi.html) includes the current before/after comparison.
