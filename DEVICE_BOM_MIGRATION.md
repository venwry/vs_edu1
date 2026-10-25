# Device-owned BOM definitions

`data/devices.json` replaces `data/peripherals.json`. Its 28 device records include
27 `bom_assembly_definition` arrays. Each array contains the original assembly
lines, preserving component IDs, quantities (including null), units, roles,
conditions and quantity status. `bom_assembly_metadata` preserves the former
assembly name, manufacturing requirements, routing and cost-rollup status.
The superseded 64 KB Artemis RAM device still has no BOM definition.

The former shared network hub is now three independent records:

- `device.network_hub.4_port`
- `device.network_hub.8_port`
- `device.network_hub.16_port`

Each owns its port-specific BOM and integer `specification.port_count`. Shared
component identities remain unchanged. Compatibility, site membership and product
BOM references now identify the three variants. A legacy hub-family navigator link
shows the three choices instead of silently selecting one SKU.

The 27 migrated standalone assemblies have been removed, leaving 87 records in
`data/assemblies.json`. The two separately referenced COMDEX 1982 device assembly
revisions remain. References to migrated assemblies now use the owning device ID.

Python and JavaScript readers construct a 114-record assembly index in memory from
standalone assemblies plus device definitions. They never persist a duplicate
catalogue. BOM traversal uses index membership, since an assembly reference may
now be a device ID. Python writes through the hardware-BOM view route changes back
to the owning device; missing owners, duplicate IDs and cycles fail validation.

Registry `device_assembly_aliases` translate historical assembly IDs at read time.
`device_family_aliases` records the three-way hub split; archived hub cost rows
are disambiguated using their existing variant IDs. Archived numerical models and
frozen baselines remain byte-for-byte unchanged, with no financial recalculation.

Run source validation, `tests/validate_device_migration.py`,
`tests/validate_component_migration.py`, and `tests/device-boms.test.cjs`.
The migration audit compares all 25 logical views against an independently
transformed pre-migration snapshot, verifies financial-file hashes and tests
write-through routing and rejection of cyclic device BOMs.

The subsequent structural migration is documented in COMPOSITION_MIGRATION.md.
It supersedes source field names and platform ownership above while preserving
the existing production BOM calculation pending the separate simulation review.
