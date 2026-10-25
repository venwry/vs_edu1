# Chassis, devices and configured products

Base: `386ea4166eb94a1a06d4f10cac14c3128969f36d`.

The four processor records are `part.erav1_6mhz`, `part.erav1_8mhz`,
`part.era2_12mhz` and `part.era2_16mhz_rev2`. Their display names are ERAv1 6MHz
(initial), ERAv1 8MHz (upgraded), ERA^2 12MHz and ERA^2 16MHz rev2. The last remains
an uncommitted target with no release. Generic historical processor estimates
remain explicitly family-level; they are not assigned to a speed bin as new costs.

Physical RAM modules now belong to `data/devices.json` with category
`memory_expansion`. The redundant superseded 64 KB part/device pair is consolidated;
prototype/excluded status remains. Individual memory ICs remain components. Four
module BOMs moved to their owning devices without changing chip counts or unknowns.

Six `rom_cartridge` devices own the former software-media BOMs and reference their
software editions through `software_refs`. Editions reference these via
`physical_media_refs`; software functionality, platform support, delivery choices,
licensing and prices remain with software. CP/M mainboard ROM and cartridge delivery
remain distinct. Athena's internal AIONix2 system ROM is not an external cartridge.

Six `device.chassis.*` records describe fixed hardware only. Chassis BOMs exclude
removable memory, cartridges, disks, video/network cards and external peripherals.
Aurelia and Aurelia+ fixed RAM and integrated video use nonselectable virtual
subsystems. Virtual grouping does not split combined supplied items or imply a
separately sold module. Storage mechanisms have device wrappers around their
existing component identity. Athena's existing functional BOM is now in the common
index, including its unsplit mainboard/controllers/PSU/chassis/wiring set. Its
component sourcing and incomplete engineering status are preserved.

Existing `assembly.computer.*.base` records retain their meaning as supplied base
configurations. They reference a bare chassis plus the original installed storage
and cards. Existing bundles continue to reference configured computers and their
additional devices. The BOM is the single authoritative inclusion list; there is
no second stored list of slot populations. Programme BOM descriptions now reference
the same device/assembly owners.

## Socket ownership and validation

`expansion_socket_groups[].sockets[]` describes physical connection pools with
stable IDs, a connection type, integer/null capacity, and compatible device IDs.
Aurelia's 16 KB card shares its two general expansion slots with other expansion
cards; at most one such RAM card is allowed. RAM socket pools enforce matched pairs,
capacity limits and no mixing module types. Fixed subsystems are not selectable
socket occupants. Display outputs belong to fitted graphics cards (or integrated
Aurelia video). Known card/monitor raster and electrical qualification still applies.
NICs and hubs expose network connection definitions. These are compatibility
relationships, not BOM edges, and therefore need not form an acyclic network.

Unknown Athena maximum RAM and socket capacities stay null. It has no application
cartridge sockets. Slot counts are owned by chassis definitions; the legacy reader
projects them into computer `io_and_expansion` and `memory` fields in memory. CPU
clock and label come from the selected processor record. Computer records retain
product defaults, configurations and positioning. The source writer rejects edits
to projected hardware fields; edit the chassis or processor owner directly.

`tools/device_configuration.py` derives fitted devices and slot assignments from
BOM traversal. Validation rejects duplicate sockets, incompatible/fixed selections,
overpopulation, unmatched RAM and mixed module types. Missing connection facts or
unknown capacities are reported as qualification pending, never silently treated
as confirmed compatibility. Chassis BOM validation rejects removable devices.

## UI and costs

The three family pages show only Processor and System RAM below the selector.
Existing complete computer options are labelled configured computers; each family
also offers two bare-chassis selections with fixed-hardware BOMs and socket details.
ROM cartridge buttons open physical devices; software remains separately inspectable.
The BOM Navigator distinguishes Chassis and Internal subsystem records.

No financial models, embedded reports or baselines were recalculated. New standalone
hardware has no fabricated price or unit cost. Archived family-level processor cost
rows remain inspectable on both family members with an explicit scope warning. Old
processor-family URLs open a variant chooser. Exact memory/media aliases preserve
old links and archived assembly references.

Future cost rebuilds are blocked until routing ownership is qualified for the new
chassis/configuration split; simply costing each new wrapper would double-count
production overhead. The old one-time memory manufacturing migration is guarded
against recreating superseded source structures.

## Verification

`tests/validate_chassis_migration.py` compares every pre-migration assembly's
flattened physical inventory (including unknown quantities) against its new graph,
normalizing only the intentional CPU split. It checks immutable model/baseline
hashes, module capacities, Athena functional sets, invalid socket populations and
write-through roundtrips. Older migration audits retain their lasting identity,
archive and ownership checks; their original whole-view fingerprints are historical.
Run source/schema checks, this audit, and the browser tests, including
`tests/chassis-devices.test.cjs` and `tests/computer-families.test.cjs`.

Verification at publication: 21/22 browser tests pass; the existing atlas timeline
pricing-link assertion still fails. Python validators: 18/37 pass, with the same
19 failing validators as the base revision. Source schemas, logical-view parity,
physical-equivalence migration audit and archive invariance all pass.

## Component roots and flat computer configurations

The follow-up removes all 33 single-material `assembly.part.*` wrappers. Components
own the merged meaningful names (`alternate_names` where different), reconciled
requirements, and `cost_rollup_status`; wrapper lines and routing are discarded.
The old unbuffered graphics requirement is already covered by the newer buffered
controller requirements and is not reintroduced. Product BOM mappings now reference
`part.*` directly. Redundant component-to-self BOM references are removed.

`record_id_aliases` redirects retired wrapper IDs for links and archived models.
Archived financial files and frozen fixtures remain unchanged; their references
are translated only when read. A material component is a terminal BOM target, not
an assembly with a synthetic self-edge. Browser rendering and the guarded future
cost builder accept material roots directly. There are now 47 stored assemblies
and 58 device-owned definitions (105 runtime assemblies).

All 21 `assembly.computer.*` configurations contain device/part lines directly;
no configuration includes another computer assembly. Device internals still retain
their own BOMs. Flattening multiplies quantities, preserves unknowns and combines
parent/child conditions and roles. The independent original-inventory audit still
passes. Numerical rebuilds remain blocked pending routing qualification; flattening
must not silently remove historical configuration installation costs.

All chassis storage socket pools are called `internal_drive`. Aurelia compatibility
remains FDD-only. Artemis/Artemis Pro and Athena/Athena Server have shared FDD/HDD
pools with total capacities of 2/3 and 2/2 respectively, preserving previously
recorded bay totals. These are documented population counts, not evidence of spare
bays. Existing device compatibility and unresolved qualification remain explicit.

The computer family right-hand column now has accessible Details and Bill of
materials tabs. The latter contains selected-element BOMs/costs, or configuration
physical BOMs, recorded cost history and dated decomposition. Keyboard arrows,
Home and End switch tabs; selection updates the content within the active tab.

The subsequent commercial migration supersedes the configuration-selection and
computer-field ownership described above. See PRODUCT_CATALOG_MIGRATION.md for
the current 14-product selector, shared projections and retired target assemblies.
