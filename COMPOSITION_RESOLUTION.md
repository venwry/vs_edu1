# Composition quantities and ownership resolution

Base commit: e957eec802785a3823a27cb51aa1014ad0fef53b.

The approved design baseline defines one DMA, MMU, storage controller and FlexiBUS
controller per applicable owning device. Combined functional circuitry, firmware
sets, RAM-module support electronics, cartridge board/shell sets and passive/harness
kits have quantity one set. These are complete supplied sets, not invented internal
IC counts or qualified manufacturing designs. Existing custom AION ROM/chip supplier
attribution is retained; combined Logix integration sets remain Logix. The keyboard
has 104 switches, keycaps and matrix diodes. OEM-excluded circuitry retains a supply
condition; its quantity is one set when that condition applies. OEM sourcing and
cost completeness remain unqualified.

Each base computer owns one shared FDD controller harness. FDD devices do not each
repeat that shared cable; this supports the recorded one- and two-drive populations.
Fixed base-computer power wiring remains separate. The approved single-FDD correction
applies to Artemis Budget HDD, Athena and Athena Server commercial configurations.
Artemis Budget HDD has one FDD and one internal ST506 in its two recorded drive bays.
Athena Server retains its separate 20 MB drive model, not an ST506 substitution.

part.hdd_5mb is the canonical Seagate ST506 component. The duplicate part.athena.hdd
is removed with an archival ID alias; Athena's physical device references the same
canonical component. Its adopted availability date is 1980-07-15, an author-selected
modelling date, not a verified day of historical release. Artemis Budget HDD and its
internal HDD device start at the existing COMDEX milestone, 1980-11-19; its networking
revision still starts 1981-05-04. Each ST506 device owns one control/data cable set
and one mounting set. PSU/controller qualification stays with its base computer.

Network upgrade products reuse their existing NIC and system cartridge. Each NIC
now owns one network cable and one combined installation documentation, diagnostics
media and packaging set. Internally powered NIC delivery has no mains-cable allowance.
Existing card and bundle delivery allowances are excluded to prevent double counting.
System OS software remains owned by the cartridge. The cable's first-use date follows
the networking launch, 1981-05-04. RAM upgrade kits own their single instructions and
packout set at product level, independent of module quantity.

The undefined supplemental distribution-media allowance is removed from both active
product compositions and active assembly lines. The historical component remains
excluded. Real additional distribution media must be defined explicitly if supplied.
Three multi-computer products are removed: offer.retail.connected_office,
offer.retail.development_team and bundle.proposed_artemis_pro_small_office. Historical
snapshots and financial output bytes are preserved. Active products total 41; the
14 computer selector choices remain governed only by computer_line.

## Versioned manufacturing metadata

Device bom_assembly_metadata is owned by its composition version. Product assembly
requirements, routing and cost_rollup_status move to the corresponding product
version. Active transitional assemblies reference metadata_owner_ref plus
metadata_version_number; they no longer store duplicate metadata. The compatibility
reader hydrates the existing runtime shape and validates the pointer. The legacy
single-version device writer also writes metadata back into the version.

Original manufacturing requirements remain available, accompanied by an ownership
clarification: device construction/test belong to the device, final system integration
and shipment checks to the product. Historical requirements that call for exact parts,
test processes, firmware capacities or supply qualification are still open requirements,
not assertions that the quantity proposal completed engineering. No routing time,
yield, labour rate or cost is fabricated.

## Calculation boundary and verification

The production reader remains the transitional, non-temporal reader. Only the approved
RAM-kit physical attachments are now included through its attached physical-material
projection. Device revision assemblies remain separate; no general assembly merge or
date-based costing is enabled. Unknown quotation scope is preserved. No legacy product
BOM means no asserted equivalent financial baseline, not a zero cost.

The read-only simulation matches all 27 comparable product versions without assembly
line consolidation. Manufacturing ownership, duplicate lines, assembly-only lines,
component-date conflicts and multi-computer placement findings are resolved. One
component quantity remains unknown (site-survey network cables), alongside the two
unqualified quotations. There are 22 versions without a legacy product-level BOM.
The hypothetical full device-revision cutover still matches 26/27: the November
AutoCAD configuration would gain two AION 2114 chips. That change is not applied.

Run tests/validate_composition_resolution.py plus existing source, migration and page
tests. The new independent audit checks quantities, metadata pointer rejection,
unique HDD identity, dates, single-drive populations, remaining findings and immutable
financial files. The explicit delta fixture verifies 67 changed runtime owners before
restoring their historical view for older one-time migration audits; original historical
fixtures remain unchanged. Current counts are 350 components, 60 devices and 41 products.

Verification: all 22 source collections, legacy schemas and migration audits pass.
Python validators: 22/41 pass, with the same 19 pre-existing failures. Browser
checks: 21/22 pass after refreshing reviewed content snapshots; the existing atlas
timeline pricing-link failure remains. Financial files and frozen baselines are unchanged.
