# Commercial catalogue and technical ownership

Base: `5c433f35be93aae19060ce6a0ebe621249c0541b`.

`data/product-catalog.json` replaces `computers.json`, `offers.json`,
`product-boms.json`, and `retail-catalog.json`. There are 21 authoritative source
collections. The 48 product/platform records include historical identities,
purchase options and explicitly incomplete quotations; they are not 48 currently
available computer configurations. Existing commercial identifiers remain stable.

## Computer selection

`computer_line` is the sole membership predicate for the three computer selectors:
Aurelia has four products, Artemis eight, Athena two. No cost row, RAM recipe,
category, status, or chassis enumeration adds a choice. Status labels preserve
announced/planned/acceptance-pending distinctions. Null excludes a record from these
selectors without asserting it is unavailable in other commercial contexts.

Retired promotional choices and purchase options have null computer_line. Software
solutions and unresolved multi-machine quotations remain separate commercial entries.
The six platform identities remain valid software/event references. Four are
non-sale platform records; the two Athena identities also describe planned products.

The console variants are purchase options on their respective server products.
AutoCAD is an option on the professional hardware upgrade. Historical IDs and
prices are preserved rather than aliased to products with different contents.
Retail display labels are reconciled onto their owning product. Catalogue editions
hold section/order/policy data and product references, not copied product payloads.

## Physical and commercial ownership

A commercial configuration has `main_product`, `connected_devices`, and
`attached_products`. Connections specify device_ref, quantity, used_socket and,
for a device-provided output, connected_to. Chassis expansion_socket_groups are the
authority for the chassis's allowed devices, quantities, installation multiples and
per-device limits. Installed graphics cards provide monitor outputs. Validation
checks that each such provider is supplied, and enforces its socket contract.

Source hardware assemblies for commercial packages retain manufacturing metadata
and physical packout lines. The runtime BOM inserts the main product and connected
devices from the commercial record; it does not persist another copy of those
populations. Device internals remain in devices.json. Dated product revisions retain
their original assembly IDs and connection populations. Nine unoffered RAM design
BOMs are removed and listed in retired_configuration_ids; their socket/module
capabilities remain technical facts, not sale configurations.

Cartridge software is derived through software_refs. A matching attached software
entry is rejected. Service duration and quantity remain explicit. Existing budget
HDD packout retains its historical functional HDD component and external-storage
qualification; no new connector, rail budget or enclosure specification is invented.

The three missing Artemis retail package definitions are explicit quotation-only
references with no release and unresolved composition. They are not reconstructed
as released hardware from saved pricing estimates. Unknown services, acceptance
conditions and incomplete quotation scope remain visible.

## Computer specification migration

Platform records contain identity/lifecycle/default links and technical_profile
references, not copied video/memory/storage specifications. Address maps and shared
population policies belong to memory technologies; physical RAM organization belongs
to fixed-memory devices; quantities and installed capacities are projected from BOMs.
Drive specifications live on drive devices. Internal ROM specifications live on ROM
devices. Chassis own interfaces, firmware contents and integration qualification.

Existing video cards own their board specifications. The integrated Aurelia devices
share an Aurelia video technology profile. Shared sprite behavior has a technology
with distinct authored profiles; ASIC pixel buffers and row caches reference their
controller component. NIC host_qualification owns host rate profiles; technology and
adapter views resolve references to those facts. Software compatibility is derived
from edition platform_support, and physical compatibility from device sockets.

## Readers and writes

The commercial projection in `data-store.js` is the shared in-memory commercial projection used by browsers
and Python. Python invokes it through Node with JSON on stdin: Node is now required
for affected Python catalogue tools. There is one projection implementation, no
persisted generated catalogue and no network/subprocess shell evaluation.

The 25 existing logical views remain available for historical consumers. Retired
file-shaped documents exist only transiently inside the reader. New code should use
the source product catalogue. Legacy metadata/BOM views are read-only where ownership
is derived; unchanged roundtrips are no-ops. Direct component/software/service edits
and device-owned BOM write-through remain validated. All other edits use the source
owner and validate before writing.

No financial models or frozen baselines are recalculated. Existing routing/RAM
reassessment guards remain. Historical CAD review dates remain inspectable even when
current hardware costs require reassessment; archived evaluations do not establish
current manufacturing costs.

## Verification

Run tools/validate_data.py, tests/validate_data_structure.py,
tests/validate_product_catalog.py, the existing component/device/chassis migration
audits and the browser suite. The new independent audit compares every retained
physical assembly with the base revision and hashes all saved models/baselines.
Negative tests reject illegal slots, incompatible devices, excessive quantities,
unmatched RAM, invalid computer lines and duplicate cartridge software. The browser
tests cover all 14 products, their components, saved evaluations, tabs and source
membership. Earlier snapshot counts and RAM-list indexes are updated for the explicit
catalogue reduction, not used to suppress unrelated failures.

Publication checks: 21/22 browser tests pass (the existing timeline pricing-link
assertion remains). Python validators: 19/38 pass, including the added commercial
migration audit, with the same 19 pre-existing failures. All 21 collections pass
source/schema/reference validation, all 25 logical views agree between Python and
JavaScript, and the data viewer works with the new shared resolver. Fourteen page
snapshots were reviewed and updated for the intentional product/specification changes.

The subsequent structural migration is documented in COMPOSITION_MIGRATION.md.
It supersedes source field names and platform ownership above while preserving
the existing production BOM calculation pending the separate simulation review.
