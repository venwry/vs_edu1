# Composition cutover simulation

Read-only simulation. Assembly consolidation and date-based BOM calculation are NOT enabled.

Dates use inclusive starts and exclusive ends. Each nested child is selected at its immediate parent version start. Unknown quantities are not converted to zero.

## Results

```json
{
  "devices": 60,
  "products": 44,
  "active_assemblies": 28,
  "retired_assemblies": 19,
  "compared_versions": 27,
  "unmerged_equal": 27,
  "merged_static_equal": 27,
  "merged_temporal_equal": 27,
  "full_cutover_equal": 26,
  "unknown_components": 1,
  "findings_by_kind": {
    "no_legacy_product_bom": 25,
    "quotation_scope_unresolved": 2,
    "unknown_quantity": 1,
    "multi_computer_package": 3,
    "multiple_placements": 7,
    "separate_device_revision": 2,
    "full_cutover_inventory_change": 1,
    "nonhardware_cost_boundary": 82
  }
}
```

Static comparisons ignore version dates to isolate ownership/packout differences. Temporal comparisons additionally enforce the requested parent-start rule. Financial values are not recalculated.

## Every finding

### no_legacy_product_bom

- `bundle.proposed_aurelia_office` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `bundle.proposed_aurelia_accounts` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `bundle.proposed_aurelia_developer` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `bundle.proposed_aurelia_plus_office` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `bundle.proposed_aurelia_plus_accounts` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `bundle.proposed_aurelia_plus_developer` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `bundle.proposed_aurelia_plus_analysis` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `offer.ncc82_colour_upgrade` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `offer.comdex82_reference_hardware` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `offer.ncc82_professional_graphics` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `offer.ncc82_mouse_learning` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `offer.comdex82_professional_hardware` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `offer.comdex82_upgrade_autocad` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `offer.retail.office_professional` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `offer.retail.business_accounts` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `offer.retail.developer_workstation` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `offer.retail.connect_office` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `offer.retail.cpm_migration` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `bundle.proposed_artemis_accounts` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `bundle.proposed_artemis_accounts` version 2: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `bundle.proposed_artemis_developer` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `bundle.proposed_artemis_developer` version 2: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `product.retail.connected_office` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `product.retail.development_team` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `product.proposed_artemis_pro_small_office` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.

### quotation_scope_unresolved

- `offer.retail.connect_office` version 1: Site survey/application qualification must determine remaining equipment, quantities and services; this is not a complete fixed-price package.
- `offer.retail.cpm_migration` version 1: Site survey/application qualification must determine remaining equipment, quantities and services; this is not a complete fixed-price package.

### unknown_quantity

Unknown quantities remain null. Every affected component and owner/version is listed below.

- `part.logix_network_cable`: `offer.retail.connect_office@1`

### multi_computer_package

- `product.retail.connected_office` version 1: Multiple supplied computers: connection placements must be allocated per host; aggregate capacity does not prove each machine is valid.
- `product.retail.development_team` version 1: Multiple supplied computers: connection placements must be allocated per host; aggregate capacity does not prove each machine is valid.
- `product.proposed_artemis_pro_small_office` version 1: Multiple supplied computers: connection placements must be allocated per host; aggregate capacity does not prove each machine is valid.

### multiple_placements

- `product.retail.connected_office` version 1 → `device.network_card_artemis`: Unique ref has distinct connection placements: [{"connected_to": "device.base_computer.artemis_pro", "quantity": 1, "used_socket": "expansion"}, {"connected_to": "device.base_computer.artemis", "quantity": 2, "used_socket": "expansion"}]
- `product.retail.connected_office` version 1 → `device.rom_cartridge.aionix_server`: Unique ref has distinct connection placements: [{"connected_to": "device.base_computer.artemis_pro", "quantity": 1, "used_socket": "system_cartridge"}, {"connected_to": "device.base_computer.artemis", "quantity": 2, "used_socket": "system_cartridge"}]
- `product.retail.development_team` version 1 → `device.artemis_video_card`: Unique ref has distinct connection placements: [{"connected_to": "device.base_computer.artemis_pro", "quantity": 1, "used_socket": "video_card"}, {"connected_to": "device.base_computer.artemis", "quantity": 4, "used_socket": "video_card"}]
- `product.retail.development_team` version 1 → `device.network_card_artemis`: Unique ref has distinct connection placements: [{"connected_to": "device.base_computer.artemis_pro", "quantity": 1, "used_socket": "expansion"}, {"connected_to": "device.base_computer.artemis", "quantity": 4, "used_socket": "expansion"}]
- `product.retail.development_team` version 1 → `device.rom_cartridge.aionix_server`: Unique ref has distinct connection placements: [{"connected_to": "device.base_computer.artemis_pro", "quantity": 1, "used_socket": "system_cartridge"}, {"connected_to": "device.base_computer.artemis", "quantity": 4, "used_socket": "system_cartridge"}]
- `product.proposed_artemis_pro_small_office` version 1 → `device.network_card_artemis`: Unique ref has distinct connection placements: [{"connected_to": "device.base_computer.artemis_pro", "quantity": 1, "used_socket": "expansion"}, {"connected_to": "device.base_computer.artemis", "quantity": 2, "used_socket": "expansion"}]
- `product.proposed_artemis_pro_small_office` version 1 → `device.rom_cartridge.aionix_server`: Unique ref has distinct connection placements: [{"connected_to": "device.base_computer.artemis_pro", "quantity": 1, "used_socket": "system_cartridge"}, {"connected_to": "device.base_computer.artemis", "quantity": 2, "used_socket": "system_cartridge"}]

### separate_device_revision

- `device.artemis_professional_video_128kb` version 2 → `assembly.device.artemis_professional_video_128kb.comdex82`: Assembly revision starts 1982-11-29; must create a second composition version and close the first. Inventory changes: [{"legacy": 0, "proposed": 2, "ref": "part.aion_2114"}]
- `device.mono_pro_17` version 2 → `assembly.device.mono_pro_17.comdex82`: Assembly revision starts 1982-11-29; must create a second composition version and close the first. Inventory changes: []

### full_cutover_inventory_change

- `offer.comdex82_artemis_autocad` version 1 → `assembly.offer.comdex82_artemis_autocad`: [{"legacy": 2, "proposed": 4, "ref": "part.aion_2114"}]

### nonhardware_cost_boundary

- `bundle.aurelia_mono` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.aurelia_color` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.aurelia_plus_mono` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.aurelia_plus_color` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.artemis_128_mono` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.artemis_128_mono` version 2 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.artemis_128_color` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.artemis_128_color` version 2 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.artemis_256_color` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.artemis_256_color` version 2 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.artemis_256_mono_pro` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.artemis_256_mono_pro` version 2 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.artemis_budget_128` version 1 → `software.business_tools_artemis`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.artemis_budget_128` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.artemis_budget_128` version 2 → `software.business_tools_artemis`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.artemis_budget_128` version 2 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.artemis_budget_128_hdd` version 1 → `software.business_tools_artemis`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.artemis_budget_128_hdd` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.artemis_budget_128_hdd` version 2 → `software.business_tools_artemis`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.artemis_budget_128_hdd` version 2 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_aurelia_office` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_aurelia_office` version 1 → `software.business_tools_aurelia`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_aurelia_office` version 1 → `software.abacus_1`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_aurelia_accounts` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_aurelia_accounts` version 1 → `software.business_tools_aurelia`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_aurelia_accounts` version 1 → `software.bpi_suite`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_aurelia_developer` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_aurelia_developer` version 1 → `software.business_tools_aurelia`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_aurelia_developer` version 1 → `software.simple_c_z80`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_aurelia_developer` version 1 → `software.aurelia_sdk`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_aurelia_plus_office` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_aurelia_plus_office` version 1 → `software.business_tools_aurelia`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_aurelia_plus_office` version 1 → `software.abacus_2`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_aurelia_plus_accounts` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_aurelia_plus_accounts` version 1 → `software.business_tools_aurelia`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_aurelia_plus_accounts` version 1 → `software.bpi_suite`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_aurelia_plus_developer` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_aurelia_plus_developer` version 1 → `software.business_tools_aurelia`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_aurelia_plus_developer` version 1 → `software.simple_c_z80`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_aurelia_plus_developer` version 1 → `software.aurelia_sdk`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_aurelia_plus_analysis` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_aurelia_plus_analysis` version 1 → `software.business_tools_aurelia`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_aurelia_plus_analysis` version 1 → `software.abacus_2`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_aurelia_plus_analysis` version 1 → `software.pulse_1`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `offer.comdex82_artemis_autocad` version 1 → `software.autocad_1_artemis`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `offer.ncc82_mouse_learning` version 1 → `software.entertainment_suite`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `offer.comdex82_upgrade_autocad` version 1 → `software.autocad_1_artemis`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `offer.retail.office_professional` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `offer.retail.office_professional` version 1 → `software.business_tools_artemis`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `offer.retail.office_professional` version 1 → `software.abacus_3`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `offer.retail.business_accounts` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `offer.retail.business_accounts` version 1 → `software.business_tools_artemis`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `offer.retail.business_accounts` version 1 → `software.bpi_suite`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `offer.retail.business_accounts` version 1 → `service.bpi_training`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `offer.retail.developer_workstation` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `offer.retail.developer_workstation` version 1 → `software.business_tools_artemis`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `offer.retail.developer_workstation` version 1 → `software.aion_c_ide`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `offer.retail.developer_workstation` version 1 → `software.artemis_sdk`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_accounts` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_accounts` version 1 → `software.business_tools_artemis`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_accounts` version 1 → `software.bpi_suite`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_accounts` version 2 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_accounts` version 2 → `software.business_tools_artemis`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_accounts` version 2 → `software.bpi_suite`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_developer` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_developer` version 1 → `software.business_tools_artemis`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_developer` version 1 → `software.aion_c_ide`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_developer` version 1 → `software.artemis_sdk`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_developer` version 2 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_developer` version 2 → `software.business_tools_artemis`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_developer` version 2 → `software.aion_c_ide`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_developer` version 2 → `software.artemis_sdk`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `product.retail.connected_office` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `product.retail.connected_office` version 1 → `software.bpi_client_server`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `product.retail.connected_office` version 1 → `edition.bpi_client_server.era_client`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `product.retail.connected_office` version 1 → `software.business_tools_artemis`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `product.retail.development_team` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `product.retail.development_team` version 1 → `software.aion_development_team`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `product.proposed_artemis_pro_small_office` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `product.proposed_artemis_pro_small_office` version 1 → `software.bpi_client_server`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `product.proposed_artemis_pro_small_office` version 1 → `edition.bpi_client_server.era_client`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `product.proposed_artemis_pro_small_office` version 1 → `software.business_tools_artemis`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.

## Exact per-product physical differences

```json
[
  {
    "owner": "product.athena",
    "version": 1,
    "assembly": "assembly.computer.athena.base",
    "unmerged_difference": [],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  },
  {
    "owner": "product.athena_server",
    "version": 1,
    "assembly": "assembly.computer.athena_server.base",
    "unmerged_difference": [],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  },
  {
    "owner": "bundle.aurelia_mono",
    "version": 1,
    "assembly": "assembly.bundle.aurelia_mono",
    "unmerged_difference": [],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  },
  {
    "owner": "bundle.aurelia_color",
    "version": 1,
    "assembly": "assembly.bundle.aurelia_color",
    "unmerged_difference": [],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  },
  {
    "owner": "bundle.aurelia_plus_mono",
    "version": 1,
    "assembly": "assembly.bundle.aurelia_plus_mono",
    "unmerged_difference": [],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  },
  {
    "owner": "bundle.aurelia_plus_color",
    "version": 1,
    "assembly": "assembly.bundle.aurelia_plus_color",
    "unmerged_difference": [],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  },
  {
    "owner": "bundle.artemis_128_mono",
    "version": 1,
    "assembly": "assembly.bundle.artemis_128_mono",
    "unmerged_difference": [],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  },
  {
    "owner": "bundle.artemis_128_mono",
    "version": 2,
    "assembly": "assembly.bundle.artemis_128_mono.networked",
    "unmerged_difference": [],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  },
  {
    "owner": "bundle.artemis_128_color",
    "version": 1,
    "assembly": "assembly.bundle.artemis_128_color",
    "unmerged_difference": [],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  },
  {
    "owner": "bundle.artemis_128_color",
    "version": 2,
    "assembly": "assembly.bundle.artemis_128_color.networked",
    "unmerged_difference": [],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  },
  {
    "owner": "bundle.artemis_256_color",
    "version": 1,
    "assembly": "assembly.bundle.artemis_256_color",
    "unmerged_difference": [],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  },
  {
    "owner": "bundle.artemis_256_color",
    "version": 2,
    "assembly": "assembly.bundle.artemis_256_color.networked",
    "unmerged_difference": [],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  },
  {
    "owner": "bundle.aurelia_network_upgrade",
    "version": 1,
    "assembly": "assembly.bundle.aurelia_network_upgrade",
    "unmerged_difference": [],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  },
  {
    "owner": "bundle.artemis_network_upgrade",
    "version": 1,
    "assembly": "assembly.bundle.artemis_network_upgrade",
    "unmerged_difference": [],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  },
  {
    "owner": "bundle.artemis_pro_512_server",
    "version": 1,
    "assembly": "assembly.bundle.artemis_pro_512_server",
    "unmerged_difference": [],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  },
  {
    "owner": "bundle.artemis_pro_1mb_server",
    "version": 1,
    "assembly": "assembly.bundle.artemis_pro_1mb_server",
    "unmerged_difference": [],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  },
  {
    "owner": "bundle.artemis_256_mono_pro",
    "version": 1,
    "assembly": "assembly.bundle.artemis_256_mono_pro",
    "unmerged_difference": [],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  },
  {
    "owner": "bundle.artemis_256_mono_pro",
    "version": 2,
    "assembly": "assembly.bundle.artemis_256_mono_pro.networked",
    "unmerged_difference": [],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  },
  {
    "owner": "bundle.artemis_pro_512_mono_pro",
    "version": 1,
    "assembly": "assembly.bundle.artemis_pro_512_mono_pro",
    "unmerged_difference": [],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  },
  {
    "owner": "bundle.artemis_pro_1mb_mono_pro",
    "version": 1,
    "assembly": "assembly.bundle.artemis_pro_1mb_mono_pro",
    "unmerged_difference": [],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  },
  {
    "owner": "bundle.artemis_budget_128",
    "version": 1,
    "assembly": "assembly.bundle.artemis_budget_128",
    "unmerged_difference": [],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  },
  {
    "owner": "bundle.artemis_budget_128",
    "version": 2,
    "assembly": "assembly.bundle.artemis_budget_128.networked",
    "unmerged_difference": [],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  },
  {
    "owner": "bundle.artemis_budget_128_hdd",
    "version": 1,
    "assembly": "assembly.bundle.artemis_budget_128_hdd",
    "unmerged_difference": [],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  },
  {
    "owner": "bundle.artemis_budget_128_hdd",
    "version": 2,
    "assembly": "assembly.bundle.artemis_budget_128_hdd.networked",
    "unmerged_difference": [],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  },
  {
    "owner": "offer.comdex82_artemis_autocad",
    "version": 1,
    "assembly": "assembly.offer.comdex82_artemis_autocad",
    "unmerged_difference": [],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": [
      {
        "ref": "part.aion_2114",
        "legacy": 2,
        "proposed": 4
      }
    ]
  },
  {
    "owner": "offer.ram_64kb_module",
    "version": 1,
    "assembly": "assembly.offer.ram_64kb_module",
    "unmerged_difference": [],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  },
  {
    "owner": "offer.ram_256kb_bank",
    "version": 1,
    "assembly": "assembly.offer.ram_256kb_bank",
    "unmerged_difference": [],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  }
]
```

## Proposed assembly ownership (not applied)

```json
[
  {
    "assembly": "assembly.computer.athena.base",
    "owner": "product.athena",
    "version": 1,
    "added_lines": 0
  },
  {
    "assembly": "assembly.computer.athena_server.base",
    "owner": "product.athena_server",
    "version": 1,
    "added_lines": 0
  },
  {
    "assembly": "assembly.bundle.aurelia_mono",
    "owner": "bundle.aurelia_mono",
    "version": 1,
    "added_lines": 0
  },
  {
    "assembly": "assembly.bundle.aurelia_color",
    "owner": "bundle.aurelia_color",
    "version": 1,
    "added_lines": 0
  },
  {
    "assembly": "assembly.bundle.aurelia_plus_mono",
    "owner": "bundle.aurelia_plus_mono",
    "version": 1,
    "added_lines": 0
  },
  {
    "assembly": "assembly.bundle.aurelia_plus_color",
    "owner": "bundle.aurelia_plus_color",
    "version": 1,
    "added_lines": 0
  },
  {
    "assembly": "assembly.bundle.artemis_128_mono",
    "owner": "bundle.artemis_128_mono",
    "version": 1,
    "added_lines": 0
  },
  {
    "assembly": "assembly.bundle.artemis_128_mono.networked",
    "owner": "bundle.artemis_128_mono",
    "version": 2,
    "added_lines": 0
  },
  {
    "assembly": "assembly.bundle.artemis_128_color",
    "owner": "bundle.artemis_128_color",
    "version": 1,
    "added_lines": 0
  },
  {
    "assembly": "assembly.bundle.artemis_128_color.networked",
    "owner": "bundle.artemis_128_color",
    "version": 2,
    "added_lines": 0
  },
  {
    "assembly": "assembly.bundle.artemis_256_color",
    "owner": "bundle.artemis_256_color",
    "version": 1,
    "added_lines": 0
  },
  {
    "assembly": "assembly.bundle.artemis_256_color.networked",
    "owner": "bundle.artemis_256_color",
    "version": 2,
    "added_lines": 0
  },
  {
    "assembly": "assembly.bundle.aurelia_network_upgrade",
    "owner": "bundle.aurelia_network_upgrade",
    "version": 1,
    "added_lines": 0
  },
  {
    "assembly": "assembly.bundle.artemis_network_upgrade",
    "owner": "bundle.artemis_network_upgrade",
    "version": 1,
    "added_lines": 0
  },
  {
    "assembly": "assembly.bundle.artemis_pro_512_server",
    "owner": "bundle.artemis_pro_512_server",
    "version": 1,
    "added_lines": 0
  },
  {
    "assembly": "assembly.bundle.artemis_pro_1mb_server",
    "owner": "bundle.artemis_pro_1mb_server",
    "version": 1,
    "added_lines": 0
  },
  {
    "assembly": "assembly.bundle.artemis_256_mono_pro",
    "owner": "bundle.artemis_256_mono_pro",
    "version": 1,
    "added_lines": 0
  },
  {
    "assembly": "assembly.bundle.artemis_256_mono_pro.networked",
    "owner": "bundle.artemis_256_mono_pro",
    "version": 2,
    "added_lines": 0
  },
  {
    "assembly": "assembly.bundle.artemis_pro_512_mono_pro",
    "owner": "bundle.artemis_pro_512_mono_pro",
    "version": 1,
    "added_lines": 0
  },
  {
    "assembly": "assembly.bundle.artemis_pro_1mb_mono_pro",
    "owner": "bundle.artemis_pro_1mb_mono_pro",
    "version": 1,
    "added_lines": 0
  },
  {
    "assembly": "assembly.bundle.artemis_budget_128",
    "owner": "bundle.artemis_budget_128",
    "version": 1,
    "added_lines": 0
  },
  {
    "assembly": "assembly.bundle.artemis_budget_128.networked",
    "owner": "bundle.artemis_budget_128",
    "version": 2,
    "added_lines": 0
  },
  {
    "assembly": "assembly.bundle.artemis_budget_128_hdd",
    "owner": "bundle.artemis_budget_128_hdd",
    "version": 1,
    "added_lines": 0
  },
  {
    "assembly": "assembly.bundle.artemis_budget_128_hdd.networked",
    "owner": "bundle.artemis_budget_128_hdd",
    "version": 2,
    "added_lines": 0
  },
  {
    "assembly": "assembly.offer.ram_64kb_module",
    "owner": "offer.ram_64kb_module",
    "version": 1,
    "added_lines": 0
  },
  {
    "assembly": "assembly.offer.ram_256kb_bank",
    "owner": "offer.ram_256kb_bank",
    "version": 1,
    "added_lines": 0
  },
  {
    "assembly": "assembly.device.artemis_professional_video_128kb.comdex82",
    "owner": "device.artemis_professional_video_128kb",
    "valid_from": "1982-11-29"
  },
  {
    "assembly": "assembly.device.mono_pro_17.comdex82",
    "owner": "device.mono_pro_17",
    "valid_from": "1982-11-29"
  }
]
```
