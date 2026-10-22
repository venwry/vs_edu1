# AIONix2 and ERA²: accepted 1983 design revision

This revision records the author's accepted design direction, not completed silicon,
implemented software, measured performance or a shipment announcement. It retains
all existing historical date precision, including the provisional NCC 1983 premiere.

## Authoritative records

- `data/software/operating-systems/software.aionix2.json`: phased OS specification,
  compatibility, ROM execution, process resilience, filesystem, users, POSIX-oriented
  subset, four UI layers, illustrative memory allocation and release gates.
- `data/standards/technology.era2_architecture.json`: pipeline/fault contracts,
  cache evaluation, TLB obligations, CPU–memory interface, coherence and conditional
  write-buffer evaluation.
- `data/hardware/components/part.aion_4164_2um.json`: unqualified speed targets;
  measured access time and refresh requirement remain unknown.
- Athena desktop/server computer records and the Athena programme's scope,
  functional BOM and open decisions: restore a 256 KiB executable system ROM bank.
  Related world principles, launch/integration narrative and site description agree.

The desktop remains 256 KiB DRAM / 5 MB HDD; the server remains 1 MiB DRAM / 20 MB
HDD. The OS's 20–100 MB filesystem qualification goal does not change bundled disks.
System ROM does not imply external application cartridge slots. Its mounting,
chip count, speed and cost are still open; the functional BOM explicitly records
an uncosted ROM bank rather than inventing selected production components.

## Accepted baseline and deferred work

Initial OS priorities are shared executable ROM with RAM patch/recovery support,
documented ERA AIONix binary compatibility, protected preemptive processes,
recoverable inode-based storage, coherent user/group permissions, a documented
POSIX-oriented subset and an event-driven TUI. Existing AIONix v1 records remain
historical; Z80 portability remains source-level, not binary compatibility.

The four logical UI layers are Application, Abstraction, Translation & Compatibility,
and OS Native API. They extend the portable C API; four processes or four IPC
crossings are not required. Full graphical windowing, broader networking, threads,
locales, metadata journaling and disk paging are staged follow-on work.

The 256 KiB DRAM budget is illustrative, not proof of fit. ROM saves resident code
space, not writable application memory. Prefer at least 512 KiB for heavier desktop
workloads; qualify server workloads against its existing configuration.

ERA² remains a 12 MHz target with a 512-byte baseline instruction cache. A 1 KiB
cache, two-entry write buffer and 16 MHz speed bin require separate decisions and
qualification. The 142,000-transistor envelope is not enlarged. Pipeline stages,
ASID width, electrical details and exact fault continuation remain implementation
gates. No general 2–3× speedup is promised without workload measurements.

DRAM 120 ns access and 3–2–2–2 CPU-clock refill timing are engineering targets,
not measurements. Qualify fallback timing, board margin, refresh, DMA, ROM timing
and populated-bank behavior separately.

## Standards and evidence

[The Open Group Base Specifications Issue 8 / POSIX.1-2024](https://pubs.opengroup.org/onlinepubs/9799919799/)
is an out-of-world future-informed API reference. It supports the interface design
direction, not fictional 1983 availability or AIONix conformance. An explicit
implemented/partial/absent interface matrix and semantic tests are release work.
The project claims no complete contemporary POSIX conformance.

## Schema, generated output and economics

Existing version-1 object fields hold these additive specifications; no schema
version, IDs or consumers' existing field meanings change. There are no new edition
identities or commercially qualified resource promises. Resource figures are product
architecture planning targets until actual editions are defined.

`python tools/data_catalog.py` rebuilds deterministic catalog projections. Financial
models, prices, forecasts, their recorded input hashes and immutable baselines are
not recalculated. Any earlier ROM cost estimate remains provisional and is not a
selected production BOM cost.

## Validation

The existing Athena validator now checks system ROM against the functional BOM,
the illustrative RAM budget total, four UI layers and preservation of unqualified
DRAM/cache status. Schema/reference/BOM checks and rendered-page tests are run with
this revision; intentional page text changes are reviewed before updating fixtures.

Validation results: 956 canonical records pass schema/view/baseline validation;
catalog references, hardware BOM arithmetic and the expanded Athena check pass.
Ten interaction/layout suites pass. The legacy `atlas.test.cjs` fails at its
`timeline missing pricing.html` expectation on both untouched parent commit
`ebe97ac62fa33b4f8b414e27a06c5426d4b78e14` and this revision; no assertion was removed.
The reviewed page fixture changes only Athena, operating systems and timeline,
including their newly rendered specifications and related record links.
