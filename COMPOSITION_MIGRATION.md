# Versioned composition migration

Base: a70df3d (merged PR #25). This migration changes storage and identity, but does
not consolidate assembly lines into compositions or enable temporal BOM costing.

## Source ownership

Six device.chassis IDs become device.base_computer IDs, category base_computer.
Names and socket consumers follow the new category. Fixed hardware contents remain
unchanged. The six former computer platform records now live on those devices;
platform_assembly_refs preserves historical configured-BOM links without confusing
them with the base device's own hardware_assembly_refs. Technical references,
lifecycle, availability and qualification remain at their owners.

computer.* remains a compatibility platform identity for software, technology,
event and archived financial references. schemas/data-registry.json declares
platform_device_aliases to the sole stored device owners. Legacy computer records
are transient projections, not a second persisted collection. Chassis IDs redirect
through record_id_aliases. Athena commercial identities are product.athena and
product.athena_server; their technical platform identities remain computer.athena
and computer.athena_server in legacy views. Their product contents stay separate
from the fixed base computers.

The Tandy external platform moves to ecosystem-inputs.json.external_platforms.
There are 44 commercial product records and 60 devices. Computer selectors retain
4 Aurelia, 8 Artemis and 2 Athena choices, qualified solely by computer_line.

## Shared composition contract

Both products and devices use composition_history. Each version has valid_from,
valid_to, version_number and composition_definition. Lines have ref, quantity,
unit, role, condition and quantity_status. Product lines additionally have
main_product/connected_device/attached_product element_type; connection socket,
provider and service-duration data remain explicit. Line IDs and typed device_ref,
software_ref, product_ref and service_ref are removed from stored composition lines.

Five month-only device dates are now 1982-06-07 (the approved correction of 1092).
Athena premiere is 1983-05-16; qualification status is not upgraded by a date edit.
Device histories start at their introduction dates. Ten undated proposals retain
null valid_from and explicit date_status unknown; dates are not fabricated.
Initial valid_to defaults to 1990-01-01, a modelling boundary rather than withdrawal.
Actual product revisions close the preceding interval. Two excluded RAM designs
have empty histories, not invented BOMs.

Products never contain another product as a composition line. The old base-bundle
and attached-product references are expanded. Three unknown underlying package
identities remain in unresolved_items as provenance, not inclusion edges. Their
compositions are explicitly incomplete. Cartridge software is not included twice.

Refs are unique within each composition version. The five-computer development-team
package needs three placements lists: identical video cards, NICs and cartridges
are supplied to two different host types. Each placement carries connected_to,
used_socket and quantity. This preserves original placements under one unique ref,
without inventing line IDs or virtual commercial devices. Aggregate capacity checks
are not proof of per-machine electrical qualification.

## Assemblies and production calculation remain transitional

28 assembly records remain active; 19 are in retired_assemblies.json (10 moved and
9 restored from pre-catalogue history). Retirement follows commercial dependencies,
including device revision dependencies. Cost references do not prevent retirement.
Assembly lines have NOT been merged into product/device histories. Both November
device revision assemblies remain separate. Their future consolidation is simulated.

The reader reconstructs the former device BOM fields and commercial connection
fields in memory, then executes the existing assembly projection and traversal.
It includes the 10 moved assemblies for compatibility; the nine previously removed
configurations stay excluded from the production index. All 97 production assembly
line arrays are identical to the base revision after the chassis-ID translation.
Financial models and frozen baselines are byte-identical. No financial recalculation
or date-based composition selection has been enabled.

Editing a single-version device through the legacy BOM writer updates that version;
ambiguous multi-version writes are rejected. New code should edit explicit source
versions. Source validation rejects duplicate refs, bad dates/intervals, cycles,
product nesting, invalid socket populations and duplicate cartridge software.

## Simulation and unresolved decisions

Run python tools/simulate_compositions.py --markdown to reproduce
COMPOSITION_SIMULATION.md. The simulator never writes source or financial files.
For each nested device it selects child.valid_from <= parent.valid_from <
child.valid_to, then recurses at the selected child's own start date. It separately
compares unchanged legacy BOMs, product-packout consolidation, and full consolidation
including the dated device revisions. No missing child is silently replaced with
an arbitrary version.

The full dry run matches 26 of 27 comparable product versions. The COMDEX AutoCAD
package gains two AION 2114 chips when its November professional video revision is
actually selected. This is a reported discrepancy, not an applied correction.
24 of 27 product versions need retained assembly packout to reproduce their legacy
inventory. 26 assembly-only line occurrences must be assigned to composition owners.
Ten proposals lack start dates; three referenced packages have undefined contents.
The original budget-HDD product predates its HDD component. 141 distinct components
have unknown physical quantities across the traversed inventories. Routing,
requirements and cost-rollup ownership, nonhardware costs and per-host placement
qualification must be resolved before calculation cutover. Exact records and
inventory deltas are listed in the simulation report.

## Verification

Run tools/validate_data.py, tests/validate_data_structure.py,
tests/validate_composition_migration.py, tests/validate_product_catalog.py,
tests/validate_device_migration.py and tests/validate_chassis_migration.py, plus the
browser suite. The composition fixture independently fingerprints all 97 legacy
assembly line arrays and immutable financial files. Negative tests cover overlapping
versions, duplicated refs, product nesting, inconsistent quantities and cycles.
Earlier one-time audit fixtures remain historical and are not regenerated.

Verification result: all 22 source collections and migration audits pass. Browser
suite: 21/22, with the pre-existing timeline pricing-link failure. Python validators:
20/39, with the same 19 pre-existing failures. All 25 JS/Python logical views agree.
Fourteen UI snapshots were updated for the explicit identity, composition and date
changes; derived compatibility composition fields are hidden beside their source
histories to avoid duplicate details.

The approved follow-up in PRODUCT_COMPLETION.md fills snapshot-derived product
dates/contents and changes device delivery scope. It supersedes the prior missing
product/date counts and unchanged-BOM statement; financial files remain unchanged.

COMPOSITION_RESOLUTION.md records the later approved quantity, manufacturing ownership,
commercial removal and single-FDD changes. Current active product count is 41.
