# AION Aurelia system controller

Aurelia and Aurelia+ each contain one custom AION chip combining DMA, bank selection and CPU-independent system-DRAM refresh. The hardware and memory diagrams show memory control and DMA as separate functional blocks explicitly labeled as the same physical die. The chip is separate from the video controller.

## Memory organization

The Z80 logical space remains 64 KiB: 0000–6FFF fixed lower RAM, 7000–EFFF switchable in 4 KiB pages, F000–FFFF common system RAM. Normal Aurelia mapping provides 44 KiB lower RAM plus 4 KiB common RAM; expanded Aurelia and Aurelia+ provide 60 KiB lower plus 4 KiB common. Existing application-workspace/BDOS boundaries remain specified and must be revalidated against the completed drivers. Sprite SRAM is a separate 1 KiB video resource, accessed through upload ports rather than a new application-memory window.

The controller supports three banks of eight 16Kx1 system DRAMs in base Aurelia, a fourth bank with the 16 KiB expansion, and eight 64Kx1 system DRAMs in Aurelia+. Every installed bank receives refresh, including hidden banks. Derive row coverage and retention deadlines from each qualified DRAM ordering code. Refresh runs during CPU execution, HALT and DMA. Initialize refresh before RAM use; reset disables DMA and establishes boot ROM at address zero.

## DMA contract

One 8-bit transfer engine has two saved contexts, 16-bit source/destination/length registers, fixed/increment/decrement addressing, memory-to-memory and memory/I/O operations. Physical bank selections are latched when starting a transfer. Software resolves logical mappings and splits buffers at 4 KiB boundaries; reject invalid banks, ROM writes and out-of-range transfers. CPU remapping cannot redirect an active physical transfer.

Use bounded bursts with guaranteed CPU and refresh service. Video upload ports provide automatic address increment and target-ready backpressure; display reads retain deadline priority. Peripherals need qualified request/ready or FIFO interfaces before drivers enable DMA. Completion/error interrupts and remaining-count status support controlled abort; warm boot drains or aborts DMA before restoring maps or reusing buffers. Programmed I/O remains available. Qualify both 4 and 6 MHz host interfaces without overclocking a slower part.

## Manufacturing assessment

Central 3 micron die area is 30 mm2, range 26–34 mm2; pin count and layout are not released. The cost model uses a $3 package allowance and $1.30 test labor, producing $10.4753 per good packaged chip under 1978 assumptions (approximately 34.1% final saleable yield). An $11.50 incremental interface/PCB/assembly-test functional allowance is added. The old $18 clock/reset/interrupt/mapper/buffer set becomes a $13 remaining set: a $5 replacement credit, not a second mapper charge. Nominal later-year costs follow model learning factors.

The combined sprite/system-controller change has an approximately $36 central recurring increment before final-product scrap/rounding effects, with a $27–53 planning envelope. This is not a supplier quotation. Engineering BOM unit_cost fields remain null pending released definitions; manufacturing_costs.json holds scenario estimates. The credit and interface allowances need schematic-level reconciliation.

Incremental effort is explicitly budgeted in the industrial model: 48 AION Labs person-months for SRAM/video, 60 for the system controller, 24 Logix for board/integration, 18 DRI for DMA/BIOS, and 12 AION Software for API/SDK. These are planning work packages additional to existing programmes. Their payroll/prototypes and revised fab capacity flow into quarterly investments and ROI; they are not hidden inside recurring chip prices.

## Acceptance gates

Prove CPU/DMA bus handover, every installed-bank refresh deadline, simultaneous peripheral requests, maximum display/sprite load, upload backpressure, page boundaries, abort/reset and warm boot across temperature/process corners. Verify a stalled peripheral cannot hold ownership indefinitely and that refresh deadlines remain protected during waits. Freeze numeric burst/time-out limits from those timing proofs. Memory corruption, missing display deadlines and bus contention are release blockers; specification tests alone cannot certify silicon.
