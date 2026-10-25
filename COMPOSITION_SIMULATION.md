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
  "unmerged_equal": 21,
  "merged_static_equal": 27,
  "merged_temporal_equal": 27,
  "full_cutover_equal": 26,
  "unknown_components": 135,
  "findings_by_kind": {
    "unknown_quantity": 1309,
    "manufacturing_metadata": 26,
    "assembly_duplicate_line": 20,
    "assembly_only_line": 6,
    "component_after_parent": 1,
    "no_legacy_product_bom": 25,
    "multi_computer_package": 3,
    "multiple_placements": 7,
    "quotation_scope_unresolved": 2,
    "separate_device_revision": 2,
    "full_cutover_inventory_change": 1,
    "nonhardware_cost_boundary": 82
  }
}
```

Static comparisons ignore version dates to isolate ownership/packout differences. Temporal comparisons additionally enforce the requested parent-start rule. Financial values are not recalculated.

## Every finding

### unknown_quantity

Unknown quantities remain null. Every affected component and owner/version is listed below.

- `part.artemis_dma`: `bundle.artemis_128_mono@1`, `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@1`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@1`, `bundle.artemis_256_color@2`, `bundle.artemis_pro_512_server@1`, `bundle.artemis_pro_1mb_server@1`, `bundle.artemis_256_mono_pro@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `bundle.artemis_budget_128@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@1`, `bundle.artemis_budget_128_hdd@2`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@1`, `bundle.proposed_artemis_developer@2`, `device.base_computer.artemis@1`, `device.base_computer.artemis_pro@1`
- `part.artemis_fdd_hdd_controller`: `bundle.artemis_128_mono@1`, `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@1`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@1`, `bundle.artemis_256_color@2`, `bundle.artemis_pro_512_server@1`, `bundle.artemis_pro_1mb_server@1`, `bundle.artemis_256_mono_pro@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `bundle.artemis_budget_128@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@1`, `bundle.artemis_budget_128_hdd@2`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@1`, `bundle.proposed_artemis_developer@2`, `device.base_computer.artemis@1`, `device.base_computer.artemis_pro@1`
- `part.artemis_mmu`: `bundle.artemis_128_mono@1`, `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@1`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@1`, `bundle.artemis_256_color@2`, `bundle.artemis_pro_512_server@1`, `bundle.artemis_pro_1mb_server@1`, `bundle.artemis_256_mono_pro@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `bundle.artemis_budget_128@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@1`, `bundle.artemis_budget_128_hdd@2`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@1`, `bundle.proposed_artemis_developer@2`, `device.base_computer.artemis@1`, `device.base_computer.artemis_pro@1`
- `part.artemis_ram_module_128kb.capacity_identification_straps`: `product.athena@1`, `product.athena_server@1`, `bundle.artemis_128_mono@1`, `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@1`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@1`, `bundle.artemis_256_color@2`, `bundle.artemis_pro_512_server@1`, `bundle.artemis_pro_1mb_server@1`, `bundle.artemis_256_mono_pro@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `bundle.artemis_budget_128@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@1`, `bundle.artemis_budget_128_hdd@2`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `offer.ram_64kb_module@1`, `offer.ram_256kb_bank@1`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@1`, `bundle.proposed_artemis_developer@2`, `device.ram_64kb_x32@1`, `device.ram_128kb_x32@1`, `device.ram_256kb_x32@1`, `device.ram_256kb_x32_2um@1`
- `part.artemis_ram_module_128kb.data_buffers_and_byte_enable_logic`: `product.athena@1`, `product.athena_server@1`, `bundle.artemis_128_mono@1`, `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@1`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@1`, `bundle.artemis_256_color@2`, `bundle.artemis_pro_512_server@1`, `bundle.artemis_pro_1mb_server@1`, `bundle.artemis_256_mono_pro@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `bundle.artemis_budget_128@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@1`, `bundle.artemis_budget_128_hdd@2`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `offer.ram_64kb_module@1`, `offer.ram_256kb_bank@1`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@1`, `bundle.proposed_artemis_developer@2`, `device.ram_64kb_x32@1`, `device.ram_128kb_x32@1`, `device.ram_256kb_x32@1`, `device.ram_256kb_x32_2um@1`
- `part.artemis_ram_module_128kb.decoupling_and_bulk_capacitors`: `product.athena@1`, `product.athena_server@1`, `bundle.artemis_128_mono@1`, `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@1`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@1`, `bundle.artemis_256_color@2`, `bundle.artemis_pro_512_server@1`, `bundle.artemis_pro_1mb_server@1`, `bundle.artemis_256_mono_pro@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `bundle.artemis_budget_128@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@1`, `bundle.artemis_budget_128_hdd@2`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `offer.ram_64kb_module@1`, `offer.ram_256kb_bank@1`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@1`, `bundle.proposed_artemis_developer@2`, `device.ram_64kb_x32@1`, `device.ram_128kb_x32@1`, `device.ram_256kb_x32@1`, `device.ram_256kb_x32_2um@1`
- `part.artemis_ram_module_128kb.module_connector_contacts`: `product.athena@1`, `product.athena_server@1`, `bundle.artemis_128_mono@1`, `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@1`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@1`, `bundle.artemis_256_color@2`, `bundle.artemis_pro_512_server@1`, `bundle.artemis_pro_1mb_server@1`, `bundle.artemis_256_mono_pro@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `bundle.artemis_budget_128@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@1`, `bundle.artemis_budget_128_hdd@2`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `offer.ram_64kb_module@1`, `offer.ram_256kb_bank@1`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@1`, `bundle.proposed_artemis_developer@2`, `device.ram_64kb_x32@1`, `device.ram_128kb_x32@1`, `device.ram_256kb_x32@1`, `device.ram_256kb_x32_2um@1`
- `part.aurelia_monitor_dac`: `bundle.aurelia_mono@1`, `bundle.proposed_aurelia_office@1`, `bundle.proposed_aurelia_accounts@1`, `bundle.proposed_aurelia_developer@1`, `device.mono_monitor_1@1`
- `part.bundle.artemis_network_upgrade.bundle_cables_media_manuals_and_carton_packout`: `bundle.artemis_network_upgrade@1`
- `part.bundle.aurelia_network_upgrade.bundle_cables_media_manuals_and_carton_packout`: `bundle.aurelia_network_upgrade@1`
- `part.color_monitor_controller`: `bundle.aurelia_color@1`, `bundle.aurelia_plus_color@1`, `bundle.artemis_128_color@1`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@1`, `bundle.artemis_256_color@2`, `bundle.artemis_budget_128@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@1`, `bundle.artemis_budget_128_hdd@2`, `device.color_monitor_1@1`, `device.color_monitor_2@1`
- `part.computer.artemis.boot_rom_chips`: `bundle.artemis_128_mono@1`, `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@1`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@1`, `bundle.artemis_256_color@2`, `bundle.artemis_256_mono_pro@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_budget_128@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@1`, `bundle.artemis_budget_128_hdd@2`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@1`, `bundle.proposed_artemis_developer@2`, `device.base_computer.artemis@1`
- `part.computer.artemis.clock_reset_interrupts_mapper_and_bus_buffers`: `bundle.artemis_128_mono@1`, `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@1`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@1`, `bundle.artemis_256_color@2`, `bundle.artemis_256_mono_pro@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_budget_128@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@1`, `bundle.artemis_budget_128_hdd@2`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@1`, `bundle.proposed_artemis_developer@2`, `device.base_computer.artemis@1`
- `part.computer.artemis.connectors_passives_fasteners_and_harnesses`: `bundle.artemis_128_mono@1`, `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@1`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@1`, `bundle.artemis_256_color@2`, `bundle.artemis_256_mono_pro@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_budget_128@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@1`, `bundle.artemis_budget_128_hdd@2`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@1`, `bundle.proposed_artemis_developer@2`, `device.base_computer.artemis@1`
- `part.computer.artemis.paired_bank_dram_controller_refresh_and_data_buffers`: `bundle.artemis_128_mono@1`, `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@1`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@1`, `bundle.artemis_256_color@2`, `bundle.artemis_256_mono_pro@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_budget_128@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@1`, `bundle.artemis_budget_128_hdd@2`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@1`, `bundle.proposed_artemis_developer@2`, `device.base_computer.artemis@1`
- `part.computer.artemis_pro.boot_rom_chips`: `bundle.artemis_pro_512_server@1`, `bundle.artemis_pro_1mb_server@1`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `offer.retail.connected_office@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_pro_small_office@1`, `device.base_computer.artemis_pro@1`
- `part.computer.artemis_pro.clock_reset_interrupts_mapper_and_bus_buffers`: `bundle.artemis_pro_512_server@1`, `bundle.artemis_pro_1mb_server@1`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `offer.retail.connected_office@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_pro_small_office@1`, `device.base_computer.artemis_pro@1`
- `part.computer.artemis_pro.connectors_passives_fasteners_and_harnesses`: `bundle.artemis_pro_512_server@1`, `bundle.artemis_pro_1mb_server@1`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `offer.retail.connected_office@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_pro_small_office@1`, `device.base_computer.artemis_pro@1`
- `part.computer.artemis_pro.paired_bank_dram_controller_refresh_and_data_buffers`: `bundle.artemis_pro_512_server@1`, `bundle.artemis_pro_1mb_server@1`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `offer.retail.connected_office@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_pro_small_office@1`, `device.base_computer.artemis_pro@1`
- `part.computer.aurelia.boot_rom_chips`: `bundle.aurelia_mono@1`, `bundle.aurelia_color@1`, `bundle.proposed_aurelia_office@1`, `bundle.proposed_aurelia_accounts@1`, `bundle.proposed_aurelia_developer@1`, `device.base_computer.aurelia@1`
- `part.computer.aurelia.clock_reset_interrupts_and_bus_buffers`: `bundle.aurelia_mono@1`, `bundle.aurelia_color@1`, `bundle.proposed_aurelia_office@1`, `bundle.proposed_aurelia_accounts@1`, `bundle.proposed_aurelia_developer@1`, `device.base_computer.aurelia@1`
- `part.computer.aurelia.connectors_passives_fasteners_and_harnesses`: `bundle.aurelia_mono@1`, `bundle.aurelia_color@1`, `bundle.proposed_aurelia_office@1`, `bundle.proposed_aurelia_accounts@1`, `bundle.proposed_aurelia_developer@1`, `device.base_computer.aurelia@1`
- `part.computer.aurelia.floppy_controller_data_separator_and_buffers`: `bundle.aurelia_mono@1`, `bundle.aurelia_color@1`, `bundle.proposed_aurelia_office@1`, `bundle.proposed_aurelia_accounts@1`, `bundle.proposed_aurelia_developer@1`, `device.base_computer.aurelia@1`
- `part.computer.aurelia_plus.boot_rom_chips`: `bundle.aurelia_plus_mono@1`, `bundle.aurelia_plus_color@1`, `bundle.proposed_aurelia_plus_office@1`, `bundle.proposed_aurelia_plus_accounts@1`, `bundle.proposed_aurelia_plus_developer@1`, `bundle.proposed_aurelia_plus_analysis@1`, `device.base_computer.aurelia_plus@1`
- `part.computer.aurelia_plus.clock_reset_interrupts_and_bus_buffers`: `bundle.aurelia_plus_mono@1`, `bundle.aurelia_plus_color@1`, `bundle.proposed_aurelia_plus_office@1`, `bundle.proposed_aurelia_plus_accounts@1`, `bundle.proposed_aurelia_plus_developer@1`, `bundle.proposed_aurelia_plus_analysis@1`, `device.base_computer.aurelia_plus@1`
- `part.computer.aurelia_plus.connectors_passives_fasteners_and_harnesses`: `bundle.aurelia_plus_mono@1`, `bundle.aurelia_plus_color@1`, `bundle.proposed_aurelia_plus_office@1`, `bundle.proposed_aurelia_plus_accounts@1`, `bundle.proposed_aurelia_plus_developer@1`, `bundle.proposed_aurelia_plus_analysis@1`, `device.base_computer.aurelia_plus@1`
- `part.computer.aurelia_plus.floppy_controller_data_separator_and_buffers`: `bundle.aurelia_plus_mono@1`, `bundle.aurelia_plus_color@1`, `bundle.proposed_aurelia_plus_office@1`, `bundle.proposed_aurelia_plus_accounts@1`, `bundle.proposed_aurelia_plus_developer@1`, `bundle.proposed_aurelia_plus_analysis@1`, `device.base_computer.aurelia_plus@1`
- `part.device.apple2_expansion_card.boot_and_driver_rom`: `device.apple2_expansion_card@1`
- `part.device.apple2_expansion_card.disk_ii_sequencer_interface`: `device.apple2_expansion_card@1`
- `part.device.apple2_expansion_card.external_cable_and_regional_mains_packout`: `device.apple2_expansion_card@1`
- `part.device.apple2_expansion_card.flexibus_two_port_transceivers_connectors`: `device.apple2_expansion_card@1`
- `part.device.apple2_expansion_card.host_bus_decode_and_buffering`: `device.apple2_expansion_card@1`
- `part.device.apple2_expansion_card.passives_protection_and_internal_harnesses`: `device.apple2_expansion_card@1`
- `part.device.apple2_video_card.apple_host_interface`: `device.apple2_video_card@1`
- `part.device.apple2_video_card.boot_and_driver_rom`: `device.apple2_video_card@1`
- `part.device.apple2_video_card.digital_video_transceivers_and_connector`: `device.apple2_video_card@1`
- `part.device.apple2_video_card.passives_protection_and_internal_harnesses`: `device.apple2_video_card@1`
- `part.device.apple2_video_card.video_clock_reset`: `device.apple2_video_card@1`
- `part.device.apple2_video_card.video_ram_window_and_bus_arbitration`: `device.apple2_video_card@1`
- `part.device.artemis_cpm80_module.boot_rom_or_host_upload_implementation`: `offer.retail.cpm_migration@1`, `device.artemis_cpm80_module@1`
- `part.device.artemis_cpm80_module.bus_width_conversion_and_clock_reset`: `offer.retail.cpm_migration@1`, `device.artemis_cpm80_module@1`
- `part.device.artemis_cpm80_module.external_cable_and_regional_mains_packout`: `offer.retail.cpm_migration@1`, `device.artemis_cpm80_module@1`
- `part.device.artemis_cpm80_module.local_64_kib_ram_implementation`: `offer.retail.cpm_migration@1`, `device.artemis_cpm80_module@1`
- `part.device.artemis_cpm80_module.local_refresh_controller`: `offer.retail.cpm_migration@1`, `device.artemis_cpm80_module@1`
- `part.device.artemis_cpm80_module.mailbox_window_arbitration_and_doorbells`: `offer.retail.cpm_migration@1`, `device.artemis_cpm80_module@1`
- `part.device.artemis_cpm80_module.passives_protection_and_internal_harnesses`: `offer.retail.cpm_migration@1`, `device.artemis_cpm80_module@1`
- `part.device.athena.fdd.controller_cable`: `product.athena@1`, `device.athena.fdd@1`
- `part.device.athena_server.fdd.controller_cable`: `product.athena_server@1`, `device.athena_server.fdd@1`
- `part.device.aurelia_ram_16kb_card.external_cable_and_regional_mains_packout`: `device.aurelia_ram_16kb_card@1`
- `part.device.aurelia_ram_16kb_card.identification_storage_and_buffers`: `device.aurelia_ram_16kb_card@1`
- `part.device.aurelia_ram_16kb_card.mapper_decode_and_refresh_interface`: `device.aurelia_ram_16kb_card@1`
- `part.device.aurelia_ram_16kb_card.passives_protection_and_internal_harnesses`: `device.aurelia_ram_16kb_card@1`
- `part.device.aurelia_ram_16kb_card.slot_connector_contacts`: `device.aurelia_ram_16kb_card@1`
- `part.device.color_monitor_1.passives_protection_and_internal_harnesses`: `bundle.aurelia_color@1`, `device.color_monitor_1@1`
- `part.device.color_monitor_1.rgb_dac_and_amplifiers_not_included_by_oem`: `bundle.aurelia_color@1`, `device.color_monitor_1@1`
- `part.device.color_monitor_1.video_link_receiver`: `bundle.aurelia_color@1`, `device.color_monitor_1@1`
- `part.device.color_monitor_2.hv_deflection_and_psu_not_included_by_oem`: `bundle.aurelia_plus_color@1`, `bundle.artemis_128_color@1`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@1`, `bundle.artemis_256_color@2`, `bundle.artemis_budget_128@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@1`, `bundle.artemis_budget_128_hdd@2`, `device.color_monitor_2@1`
- `part.device.color_monitor_2.passives_protection_and_internal_harnesses`: `bundle.aurelia_plus_color@1`, `bundle.artemis_128_color@1`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@1`, `bundle.artemis_256_color@2`, `bundle.artemis_budget_128@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@1`, `bundle.artemis_budget_128_hdd@2`, `device.color_monitor_2@1`
- `part.device.color_monitor_2.video_receiver_and_rgb_amplifiers`: `bundle.aurelia_plus_color@1`, `bundle.artemis_128_color@1`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@1`, `bundle.artemis_256_color@2`, `bundle.artemis_budget_128@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@1`, `bundle.artemis_budget_128_hdd@2`, `device.color_monitor_2@1`
- `part.device.flexibus_keyboard.external_cable_and_regional_mains_packout`: `bundle.aurelia_mono@1`, `bundle.aurelia_color@1`, `bundle.aurelia_plus_mono@1`, `bundle.aurelia_plus_color@1`, `bundle.artemis_128_mono@1`, `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@1`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@1`, `bundle.artemis_256_color@2`, `bundle.artemis_256_mono_pro@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `bundle.artemis_budget_128@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@1`, `bundle.artemis_budget_128_hdd@2`, `bundle.proposed_aurelia_office@1`, `bundle.proposed_aurelia_accounts@1`, `bundle.proposed_aurelia_developer@1`, `bundle.proposed_aurelia_plus_office@1`, `bundle.proposed_aurelia_plus_accounts@1`, `bundle.proposed_aurelia_plus_developer@1`, `bundle.proposed_aurelia_plus_analysis@1`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@1`, `bundle.proposed_artemis_developer@2`, `device.flexibus_keyboard@1`
- `part.device.flexibus_keyboard.flexibus_interface_electronics`: `bundle.aurelia_mono@1`, `bundle.aurelia_color@1`, `bundle.aurelia_plus_mono@1`, `bundle.aurelia_plus_color@1`, `bundle.artemis_128_mono@1`, `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@1`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@1`, `bundle.artemis_256_color@2`, `bundle.artemis_256_mono_pro@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `bundle.artemis_budget_128@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@1`, `bundle.artemis_budget_128_hdd@2`, `bundle.proposed_aurelia_office@1`, `bundle.proposed_aurelia_accounts@1`, `bundle.proposed_aurelia_developer@1`, `bundle.proposed_aurelia_plus_office@1`, `bundle.proposed_aurelia_plus_accounts@1`, `bundle.proposed_aurelia_plus_developer@1`, `bundle.proposed_aurelia_plus_analysis@1`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@1`, `bundle.proposed_artemis_developer@2`, `device.flexibus_keyboard@1`
- `part.device.flexibus_keyboard.key_switches`: `bundle.aurelia_mono@1`, `bundle.aurelia_color@1`, `bundle.aurelia_plus_mono@1`, `bundle.aurelia_plus_color@1`, `bundle.artemis_128_mono@1`, `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@1`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@1`, `bundle.artemis_256_color@2`, `bundle.artemis_256_mono_pro@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `bundle.artemis_budget_128@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@1`, `bundle.artemis_budget_128_hdd@2`, `bundle.proposed_aurelia_office@1`, `bundle.proposed_aurelia_accounts@1`, `bundle.proposed_aurelia_developer@1`, `bundle.proposed_aurelia_plus_office@1`, `bundle.proposed_aurelia_plus_accounts@1`, `bundle.proposed_aurelia_plus_developer@1`, `bundle.proposed_aurelia_plus_analysis@1`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@1`, `bundle.proposed_artemis_developer@2`, `device.flexibus_keyboard@1`
- `part.device.flexibus_keyboard.keycaps`: `bundle.aurelia_mono@1`, `bundle.aurelia_color@1`, `bundle.aurelia_plus_mono@1`, `bundle.aurelia_plus_color@1`, `bundle.artemis_128_mono@1`, `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@1`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@1`, `bundle.artemis_256_color@2`, `bundle.artemis_256_mono_pro@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `bundle.artemis_budget_128@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@1`, `bundle.artemis_budget_128_hdd@2`, `bundle.proposed_aurelia_office@1`, `bundle.proposed_aurelia_accounts@1`, `bundle.proposed_aurelia_developer@1`, `bundle.proposed_aurelia_plus_office@1`, `bundle.proposed_aurelia_plus_accounts@1`, `bundle.proposed_aurelia_plus_developer@1`, `bundle.proposed_aurelia_plus_analysis@1`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@1`, `bundle.proposed_artemis_developer@2`, `device.flexibus_keyboard@1`
- `part.device.flexibus_keyboard.matrix_diodes`: `bundle.aurelia_mono@1`, `bundle.aurelia_color@1`, `bundle.aurelia_plus_mono@1`, `bundle.aurelia_plus_color@1`, `bundle.artemis_128_mono@1`, `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@1`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@1`, `bundle.artemis_256_color@2`, `bundle.artemis_256_mono_pro@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `bundle.artemis_budget_128@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@1`, `bundle.artemis_budget_128_hdd@2`, `bundle.proposed_aurelia_office@1`, `bundle.proposed_aurelia_accounts@1`, `bundle.proposed_aurelia_developer@1`, `bundle.proposed_aurelia_plus_office@1`, `bundle.proposed_aurelia_plus_accounts@1`, `bundle.proposed_aurelia_plus_developer@1`, `bundle.proposed_aurelia_plus_analysis@1`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@1`, `bundle.proposed_artemis_developer@2`, `device.flexibus_keyboard@1`
- `part.device.flexibus_keyboard.passives_protection_and_internal_harnesses`: `bundle.aurelia_mono@1`, `bundle.aurelia_color@1`, `bundle.aurelia_plus_mono@1`, `bundle.aurelia_plus_color@1`, `bundle.artemis_128_mono@1`, `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@1`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@1`, `bundle.artemis_256_color@2`, `bundle.artemis_256_mono_pro@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `bundle.artemis_budget_128@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@1`, `bundle.artemis_budget_128_hdd@2`, `bundle.proposed_aurelia_office@1`, `bundle.proposed_aurelia_accounts@1`, `bundle.proposed_aurelia_developer@1`, `bundle.proposed_aurelia_plus_office@1`, `bundle.proposed_aurelia_plus_accounts@1`, `bundle.proposed_aurelia_plus_developer@1`, `bundle.proposed_aurelia_plus_analysis@1`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@1`, `bundle.proposed_artemis_developer@2`, `device.flexibus_keyboard@1`
- `part.device.flexibus_keyboard.scan_controller_and_firmware_storage`: `bundle.aurelia_mono@1`, `bundle.aurelia_color@1`, `bundle.aurelia_plus_mono@1`, `bundle.aurelia_plus_color@1`, `bundle.artemis_128_mono@1`, `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@1`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@1`, `bundle.artemis_256_color@2`, `bundle.artemis_256_mono_pro@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `bundle.artemis_budget_128@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@1`, `bundle.artemis_budget_128_hdd@2`, `bundle.proposed_aurelia_office@1`, `bundle.proposed_aurelia_accounts@1`, `bundle.proposed_aurelia_developer@1`, `bundle.proposed_aurelia_plus_office@1`, `bundle.proposed_aurelia_plus_accounts@1`, `bundle.proposed_aurelia_plus_developer@1`, `bundle.proposed_aurelia_plus_analysis@1`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@1`, `bundle.proposed_artemis_developer@2`, `device.flexibus_keyboard@1`
- `part.device.flexidisk.external_cable_and_regional_mains_packout`: `device.flexidisk@1`
- `part.device.flexidisk.floppy_controller_and_data_separator`: `device.flexidisk@1`
- `part.device.flexidisk.local_firmware_processor_and_sector_ram`: `device.flexidisk@1`
- `part.device.flexidisk.passives_protection_and_internal_harnesses`: `device.flexidisk@1`
- `part.device.flexidisk_ii.aurelia_and_apple_ii_format_controller`: `device.flexidisk_ii@1`
- `part.device.flexidisk_ii.external_cable_and_regional_mains_packout`: `device.flexidisk_ii@1`
- `part.device.flexidisk_ii.local_firmware_processor_and_sector_ram`: `device.flexidisk_ii@1`
- `part.device.flexidisk_ii.passives_protection_and_internal_harnesses`: `device.flexidisk_ii@1`
- `part.device.flexiprint40.external_cable_and_regional_mains_packout`: `bundle.proposed_aurelia_accounts@1`, `bundle.proposed_aurelia_plus_accounts@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `bundle.proposed_artemis_accounts@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `device.flexiprint40@1`
- `part.device.flexiprint40.local_sequencer_firmware_font_rom_and_buffer_ram`: `bundle.proposed_aurelia_accounts@1`, `bundle.proposed_aurelia_plus_accounts@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `bundle.proposed_artemis_accounts@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `device.flexiprint40@1`
- `part.device.flexiprint40.motor_and_printhead_drivers_excluded_by_mechanism`: `bundle.proposed_aurelia_accounts@1`, `bundle.proposed_aurelia_plus_accounts@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `bundle.proposed_artemis_accounts@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `device.flexiprint40@1`
- `part.device.flexiprint40.passives_protection_and_internal_harnesses`: `bundle.proposed_aurelia_accounts@1`, `bundle.proposed_aurelia_plus_accounts@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `bundle.proposed_artemis_accounts@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `device.flexiprint40@1`
- `part.device.mono_monitor_1.hv_deflection_and_psu_not_included_by_oem`: `bundle.aurelia_mono@1`, `bundle.proposed_aurelia_office@1`, `bundle.proposed_aurelia_accounts@1`, `bundle.proposed_aurelia_developer@1`, `device.mono_monitor_1@1`
- `part.device.mono_monitor_1.passives_protection_and_internal_harnesses`: `bundle.aurelia_mono@1`, `bundle.proposed_aurelia_office@1`, `bundle.proposed_aurelia_accounts@1`, `bundle.proposed_aurelia_developer@1`, `device.mono_monitor_1@1`
- `part.device.mono_monitor_1.video_amplifier`: `bundle.aurelia_mono@1`, `bundle.proposed_aurelia_office@1`, `bundle.proposed_aurelia_accounts@1`, `bundle.proposed_aurelia_developer@1`, `device.mono_monitor_1@1`
- `part.device.mono_monitor_1.video_receiver_and_sync_circuitry`: `bundle.aurelia_mono@1`, `bundle.proposed_aurelia_office@1`, `bundle.proposed_aurelia_accounts@1`, `bundle.proposed_aurelia_developer@1`, `device.mono_monitor_1@1`
- `part.device.mono_monitor_2.hv_deflection_and_psu_not_included_by_oem`: `bundle.aurelia_plus_mono@1`, `bundle.artemis_128_mono@1`, `bundle.artemis_128_mono@2`, `bundle.proposed_aurelia_plus_office@1`, `bundle.proposed_aurelia_plus_accounts@1`, `bundle.proposed_aurelia_plus_developer@1`, `bundle.proposed_aurelia_plus_analysis@1`, `offer.retail.connected_office@1`, `bundle.proposed_artemis_pro_small_office@1`, `device.mono_monitor_2@1`
- `part.device.mono_monitor_2.passives_protection_and_internal_harnesses`: `bundle.aurelia_plus_mono@1`, `bundle.artemis_128_mono@1`, `bundle.artemis_128_mono@2`, `bundle.proposed_aurelia_plus_office@1`, `bundle.proposed_aurelia_plus_accounts@1`, `bundle.proposed_aurelia_plus_developer@1`, `bundle.proposed_aurelia_plus_analysis@1`, `offer.retail.connected_office@1`, `bundle.proposed_artemis_pro_small_office@1`, `device.mono_monitor_2@1`
- `part.device.mono_monitor_2.video_link_receiver_and_grayscale_amplifier`: `bundle.aurelia_plus_mono@1`, `bundle.artemis_128_mono@1`, `bundle.artemis_128_mono@2`, `bundle.proposed_aurelia_plus_office@1`, `bundle.proposed_aurelia_plus_accounts@1`, `bundle.proposed_aurelia_plus_developer@1`, `bundle.proposed_aurelia_plus_analysis@1`, `offer.retail.connected_office@1`, `bundle.proposed_artemis_pro_small_office@1`, `device.mono_monitor_2@1`
- `part.device.network_card_artemis.32_bit_slot_interface_and_pio_dma_selection`: `product.athena@1`, `product.athena_server@1`, `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@2`, `bundle.artemis_network_upgrade@1`, `bundle.artemis_pro_512_server@1`, `bundle.artemis_pro_1mb_server@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@2`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@2`, `device.network_card_artemis@1`
- `part.device.network_card_artemis.differential_data_and_clock_transceivers`: `product.athena@1`, `product.athena_server@1`, `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@2`, `bundle.artemis_network_upgrade@1`, `bundle.artemis_pro_512_server@1`, `bundle.artemis_pro_1mb_server@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@2`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@2`, `device.network_card_artemis@1`
- `part.device.network_card_artemis.external_cable_and_regional_mains_packout`: `product.athena@1`, `product.athena_server@1`, `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@2`, `bundle.artemis_network_upgrade@1`, `bundle.artemis_pro_512_server@1`, `bundle.artemis_pro_1mb_server@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@2`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@2`, `device.network_card_artemis@1`
- `part.device.network_card_artemis.firmware_rom`: `product.athena@1`, `product.athena_server@1`, `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@2`, `bundle.artemis_network_upgrade@1`, `bundle.artemis_pro_512_server@1`, `bundle.artemis_pro_1mb_server@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@2`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@2`, `device.network_card_artemis@1`
- `part.device.network_card_artemis.network_controller_framing_crc_and_buffers`: `product.athena@1`, `product.athena_server@1`, `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@2`, `bundle.artemis_network_upgrade@1`, `bundle.artemis_pro_512_server@1`, `bundle.artemis_pro_1mb_server@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@2`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@2`, `device.network_card_artemis@1`
- `part.device.network_card_artemis.passives_protection_and_internal_harnesses`: `product.athena@1`, `product.athena_server@1`, `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@2`, `bundle.artemis_network_upgrade@1`, `bundle.artemis_pro_512_server@1`, `bundle.artemis_pro_1mb_server@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@2`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@2`, `device.network_card_artemis@1`
- `part.device.network_card_aurelia.differential_data_and_clock_transceivers`: `bundle.aurelia_network_upgrade@1`, `device.network_card_aurelia@1`
- `part.device.network_card_aurelia.external_cable_and_regional_mains_packout`: `bundle.aurelia_network_upgrade@1`, `device.network_card_aurelia@1`
- `part.device.network_card_aurelia.firmware_rom`: `bundle.aurelia_network_upgrade@1`, `device.network_card_aurelia@1`
- `part.device.network_card_aurelia.network_controller_framing_crc_and_buffers`: `bundle.aurelia_network_upgrade@1`, `device.network_card_aurelia@1`
- `part.device.network_card_aurelia.passives_protection_and_internal_harnesses`: `bundle.aurelia_network_upgrade@1`, `device.network_card_aurelia@1`
- `part.device.network_card_aurelia.z80_host_interface`: `bundle.aurelia_network_upgrade@1`, `device.network_card_aurelia@1`
- `part.device.network_hub.shared_arbiter_clock_and_firmware`: `offer.retail.connected_office@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_pro_small_office@1`, `device.network_hub.4_port@1`, `device.network_hub.8_port@1`, `device.network_hub.16_port@1`
- `part.device.s100_flexibus_card.boot_and_driver_rom`: `device.s100_flexibus_card@1`
- `part.device.s100_flexibus_card.flexibus_two_port_transceivers_connectors`: `device.s100_flexibus_card@1`
- `part.device.s100_flexibus_card.passives_protection_and_internal_harnesses`: `device.s100_flexibus_card@1`
- `part.device.s100_flexibus_card.s100_host_interface`: `device.s100_flexibus_card@1`
- `part.device.s100_video_card.boot_and_driver_rom`: `device.s100_video_card@1`
- `part.device.s100_video_card.digital_video_transceivers_and_connector`: `device.s100_video_card@1`
- `part.device.s100_video_card.passives_protection_and_internal_harnesses`: `device.s100_video_card@1`
- `part.device.s100_video_card.s100_host_interface`: `device.s100_video_card@1`
- `part.device.s100_video_card.video_clock_reset`: `device.s100_video_card@1`
- `part.device.s100_video_card.video_ram_window_and_bus_arbitration`: `device.s100_video_card@1`
- `part.device.storage.computer.artemis.525_inch_double_density_floppy_mechanism.controller_cable`: `bundle.artemis_128_mono@1`, `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@1`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@1`, `bundle.artemis_256_color@2`, `bundle.artemis_256_mono_pro@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_budget_128@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@1`, `bundle.artemis_budget_128_hdd@2`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@1`, `bundle.proposed_artemis_developer@2`, `device.storage.computer.artemis.525_inch_double_density_floppy_mechanism@1`
- `part.device.storage.computer.artemis_pro.525_inch_double_density_floppy_mechanism.controller_cable`: `bundle.artemis_pro_512_server@1`, `bundle.artemis_pro_1mb_server@1`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `offer.retail.connected_office@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_pro_small_office@1`, `device.storage.computer.artemis_pro.525_inch_double_density_floppy_mechanism@1`
- `part.device.storage.computer.aurelia.525_inch_single_density_floppy_mechanism.controller_cable`: `bundle.aurelia_mono@1`, `bundle.aurelia_color@1`, `bundle.proposed_aurelia_office@1`, `bundle.proposed_aurelia_accounts@1`, `bundle.proposed_aurelia_developer@1`, `device.storage.computer.aurelia.525_inch_single_density_floppy_mechanism@1`
- `part.device.storage.computer.aurelia_plus.525_inch_double_density_floppy_mechanism.controller_cable`: `bundle.aurelia_plus_mono@1`, `bundle.aurelia_plus_color@1`, `bundle.proposed_aurelia_plus_office@1`, `bundle.proposed_aurelia_plus_accounts@1`, `bundle.proposed_aurelia_plus_developer@1`, `bundle.proposed_aurelia_plus_analysis@1`, `device.storage.computer.aurelia_plus.525_inch_double_density_floppy_mechanism@1`
- `part.flexibus_device_controller`: `bundle.proposed_aurelia_accounts@1`, `bundle.proposed_aurelia_plus_accounts@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `bundle.proposed_artemis_accounts@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `device.flexiprint40@1`, `device.flexidisk@1`, `device.flexidisk_ii@1`
- `part.flexibus_host_controller`: `bundle.aurelia_mono@1`, `bundle.aurelia_color@1`, `bundle.aurelia_plus_mono@1`, `bundle.aurelia_plus_color@1`, `bundle.artemis_128_mono@1`, `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@1`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@1`, `bundle.artemis_256_color@2`, `bundle.artemis_pro_512_server@1`, `bundle.artemis_pro_1mb_server@1`, `bundle.artemis_256_mono_pro@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `bundle.artemis_budget_128@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@1`, `bundle.artemis_budget_128_hdd@2`, `bundle.proposed_aurelia_office@1`, `bundle.proposed_aurelia_accounts@1`, `bundle.proposed_aurelia_developer@1`, `bundle.proposed_aurelia_plus_office@1`, `bundle.proposed_aurelia_plus_accounts@1`, `bundle.proposed_aurelia_plus_developer@1`, `bundle.proposed_aurelia_plus_analysis@1`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@1`, `bundle.proposed_artemis_developer@2`, `device.apple2_expansion_card@1`, `device.s100_flexibus_card@1`, `device.base_computer.aurelia@1`, `device.base_computer.aurelia_plus@1`, `device.base_computer.artemis@1`, `device.base_computer.artemis_pro@1`
- `part.logix_network_cable`: `offer.retail.connect_office@1`
- `part.logix_supplemental_distribution_media`: `bundle.aurelia_mono@1`, `bundle.aurelia_color@1`, `bundle.aurelia_plus_mono@1`, `bundle.aurelia_plus_color@1`, `bundle.artemis_128_mono@1`, `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@1`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@1`, `bundle.artemis_256_color@2`, `bundle.artemis_pro_512_server@1`, `bundle.artemis_pro_1mb_server@1`, `bundle.artemis_256_mono_pro@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `bundle.artemis_budget_128@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@1`, `bundle.artemis_budget_128_hdd@2`
- `part.mono_monitor2_controller`: `bundle.aurelia_plus_mono@1`, `bundle.artemis_128_mono@1`, `bundle.artemis_128_mono@2`, `bundle.proposed_aurelia_plus_office@1`, `bundle.proposed_aurelia_plus_accounts@1`, `bundle.proposed_aurelia_plus_developer@1`, `bundle.proposed_aurelia_plus_analysis@1`, `offer.retail.connected_office@1`, `bundle.proposed_artemis_pro_small_office@1`, `device.mono_monitor_2@1`
- `part.software.aionix.cartridge_pcb_and_connector_if_cartridge_delivered`: `bundle.artemis_128_mono@1`, `bundle.artemis_128_color@1`, `bundle.artemis_256_color@1`, `bundle.artemis_256_mono_pro@1`, `bundle.artemis_budget_128@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@1`, `bundle.artemis_budget_128_hdd@2`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `bundle.proposed_artemis_accounts@1`, `bundle.proposed_artemis_developer@1`, `device.rom_cartridge.aionix@1`
- `part.software.aionix.cartridge_shell_label_and_instructions`: `bundle.artemis_128_mono@1`, `bundle.artemis_128_color@1`, `bundle.artemis_256_color@1`, `bundle.artemis_256_mono_pro@1`, `bundle.artemis_budget_128@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@1`, `bundle.artemis_budget_128_hdd@2`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `bundle.proposed_artemis_accounts@1`, `bundle.proposed_artemis_developer@1`, `device.rom_cartridge.aionix@1`
- `part.software.aionix.rom_eprom_eeprom_or_media_selection`: `bundle.artemis_128_mono@1`, `bundle.artemis_128_color@1`, `bundle.artemis_256_color@1`, `bundle.artemis_256_mono_pro@1`, `bundle.artemis_budget_128@1`, `bundle.artemis_budget_128@2`, `bundle.artemis_budget_128_hdd@1`, `bundle.artemis_budget_128_hdd@2`, `offer.comdex82_artemis_autocad@1`, `offer.comdex82_reference_hardware@1`, `bundle.proposed_artemis_accounts@1`, `bundle.proposed_artemis_developer@1`, `device.rom_cartridge.aionix@1`
- `part.software.aionix_server.cartridge_pcb_and_connector_if_cartridge_delivered`: `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@2`, `bundle.artemis_network_upgrade@1`, `bundle.artemis_pro_512_server@1`, `bundle.artemis_pro_1mb_server@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@2`, `device.rom_cartridge.aionix_server@1`
- `part.software.aionix_server.cartridge_shell_label_and_instructions`: `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@2`, `bundle.artemis_network_upgrade@1`, `bundle.artemis_pro_512_server@1`, `bundle.artemis_pro_1mb_server@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@2`, `device.rom_cartridge.aionix_server@1`
- `part.software.aionix_server.rom_eprom_eeprom_or_media_selection`: `bundle.artemis_128_mono@2`, `bundle.artemis_128_color@2`, `bundle.artemis_256_color@2`, `bundle.artemis_network_upgrade@1`, `bundle.artemis_pro_512_server@1`, `bundle.artemis_pro_1mb_server@1`, `bundle.artemis_256_mono_pro@2`, `bundle.artemis_pro_512_mono_pro@1`, `bundle.artemis_pro_1mb_mono_pro@1`, `offer.retail.office_professional@1`, `offer.retail.business_accounts@1`, `offer.retail.connected_office@1`, `offer.retail.developer_workstation@1`, `offer.retail.development_team@1`, `bundle.proposed_artemis_accounts@2`, `bundle.proposed_artemis_pro_small_office@1`, `bundle.proposed_artemis_developer@2`, `device.rom_cartridge.aionix_server@1`
- `part.software.business_tools_artemis.cartridge_pcb_and_connector_if_cartridge_delivered`: `device.rom_cartridge.business_tools_artemis@1`
- `part.software.business_tools_artemis.cartridge_shell_label_and_instructions`: `device.rom_cartridge.business_tools_artemis@1`
- `part.software.business_tools_artemis.rom_eprom_eeprom_or_media_selection`: `device.rom_cartridge.business_tools_artemis@1`
- `part.software.business_tools_aurelia.cartridge_pcb_and_connector_if_cartridge_delivered`: `device.rom_cartridge.business_tools_aurelia@1`
- `part.software.business_tools_aurelia.cartridge_shell_label_and_instructions`: `device.rom_cartridge.business_tools_aurelia@1`
- `part.software.business_tools_aurelia.rom_eprom_eeprom_or_media_selection`: `device.rom_cartridge.business_tools_aurelia@1`
- `part.software.cpm_aurelia.cartridge_pcb_and_connector_if_cartridge_delivered`: `bundle.aurelia_mono@1`, `bundle.aurelia_color@1`, `bundle.aurelia_plus_mono@1`, `bundle.aurelia_plus_color@1`, `bundle.proposed_aurelia_office@1`, `bundle.proposed_aurelia_accounts@1`, `bundle.proposed_aurelia_developer@1`, `bundle.proposed_aurelia_plus_office@1`, `bundle.proposed_aurelia_plus_accounts@1`, `bundle.proposed_aurelia_plus_developer@1`, `bundle.proposed_aurelia_plus_analysis@1`, `device.rom_cartridge.cpm_aurelia@1`
- `part.software.cpm_aurelia.cartridge_shell_label_and_instructions`: `bundle.aurelia_mono@1`, `bundle.aurelia_color@1`, `bundle.aurelia_plus_mono@1`, `bundle.aurelia_plus_color@1`, `bundle.proposed_aurelia_office@1`, `bundle.proposed_aurelia_accounts@1`, `bundle.proposed_aurelia_developer@1`, `bundle.proposed_aurelia_plus_office@1`, `bundle.proposed_aurelia_plus_accounts@1`, `bundle.proposed_aurelia_plus_developer@1`, `bundle.proposed_aurelia_plus_analysis@1`, `device.rom_cartridge.cpm_aurelia@1`
- `part.software.cpm_aurelia.rom_eprom_eeprom_or_media_selection`: `bundle.aurelia_mono@1`, `bundle.aurelia_color@1`, `bundle.aurelia_plus_mono@1`, `bundle.aurelia_plus_color@1`, `bundle.proposed_aurelia_office@1`, `bundle.proposed_aurelia_accounts@1`, `bundle.proposed_aurelia_developer@1`, `bundle.proposed_aurelia_plus_office@1`, `bundle.proposed_aurelia_plus_accounts@1`, `bundle.proposed_aurelia_plus_developer@1`, `bundle.proposed_aurelia_plus_analysis@1`, `device.rom_cartridge.cpm_aurelia@1`
- `part.software.cpm_aurelia_networking.cartridge_pcb_and_connector_if_cartridge_delivered`: `bundle.aurelia_network_upgrade@1`, `device.rom_cartridge.cpm_aurelia_networking@1`
- `part.software.cpm_aurelia_networking.cartridge_shell_label_and_instructions`: `bundle.aurelia_network_upgrade@1`, `device.rom_cartridge.cpm_aurelia_networking@1`
- `part.software.cpm_aurelia_networking.rom_eprom_eeprom_or_media_selection`: `bundle.aurelia_network_upgrade@1`, `device.rom_cartridge.cpm_aurelia_networking@1`

### manufacturing_metadata

- `product.athena` version 1 → `assembly.computer.athena.base`: Routing, requirements and cost_rollup_status need explicit owner/version assignment; not represented by composition lines.
- `product.athena_server` version 1 → `assembly.computer.athena_server.base`: Routing, requirements and cost_rollup_status need explicit owner/version assignment; not represented by composition lines.
- `bundle.aurelia_mono` version 1 → `assembly.bundle.aurelia_mono`: Routing, requirements and cost_rollup_status need explicit owner/version assignment; not represented by composition lines.
- `bundle.aurelia_color` version 1 → `assembly.bundle.aurelia_color`: Routing, requirements and cost_rollup_status need explicit owner/version assignment; not represented by composition lines.
- `bundle.aurelia_plus_mono` version 1 → `assembly.bundle.aurelia_plus_mono`: Routing, requirements and cost_rollup_status need explicit owner/version assignment; not represented by composition lines.
- `bundle.aurelia_plus_color` version 1 → `assembly.bundle.aurelia_plus_color`: Routing, requirements and cost_rollup_status need explicit owner/version assignment; not represented by composition lines.
- `bundle.artemis_128_mono` version 1 → `assembly.bundle.artemis_128_mono`: Routing, requirements and cost_rollup_status need explicit owner/version assignment; not represented by composition lines.
- `bundle.artemis_128_mono` version 2 → `assembly.bundle.artemis_128_mono.networked`: Routing, requirements and cost_rollup_status need explicit owner/version assignment; not represented by composition lines.
- `bundle.artemis_128_color` version 1 → `assembly.bundle.artemis_128_color`: Routing, requirements and cost_rollup_status need explicit owner/version assignment; not represented by composition lines.
- `bundle.artemis_128_color` version 2 → `assembly.bundle.artemis_128_color.networked`: Routing, requirements and cost_rollup_status need explicit owner/version assignment; not represented by composition lines.
- `bundle.artemis_256_color` version 1 → `assembly.bundle.artemis_256_color`: Routing, requirements and cost_rollup_status need explicit owner/version assignment; not represented by composition lines.
- `bundle.artemis_256_color` version 2 → `assembly.bundle.artemis_256_color.networked`: Routing, requirements and cost_rollup_status need explicit owner/version assignment; not represented by composition lines.
- `bundle.aurelia_network_upgrade` version 1 → `assembly.bundle.aurelia_network_upgrade`: Routing, requirements and cost_rollup_status need explicit owner/version assignment; not represented by composition lines.
- `bundle.artemis_network_upgrade` version 1 → `assembly.bundle.artemis_network_upgrade`: Routing, requirements and cost_rollup_status need explicit owner/version assignment; not represented by composition lines.
- `bundle.artemis_pro_512_server` version 1 → `assembly.bundle.artemis_pro_512_server`: Routing, requirements and cost_rollup_status need explicit owner/version assignment; not represented by composition lines.
- `bundle.artemis_pro_1mb_server` version 1 → `assembly.bundle.artemis_pro_1mb_server`: Routing, requirements and cost_rollup_status need explicit owner/version assignment; not represented by composition lines.
- `bundle.artemis_256_mono_pro` version 1 → `assembly.bundle.artemis_256_mono_pro`: Routing, requirements and cost_rollup_status need explicit owner/version assignment; not represented by composition lines.
- `bundle.artemis_256_mono_pro` version 2 → `assembly.bundle.artemis_256_mono_pro.networked`: Routing, requirements and cost_rollup_status need explicit owner/version assignment; not represented by composition lines.
- `bundle.artemis_pro_512_mono_pro` version 1 → `assembly.bundle.artemis_pro_512_mono_pro`: Routing, requirements and cost_rollup_status need explicit owner/version assignment; not represented by composition lines.
- `bundle.artemis_pro_1mb_mono_pro` version 1 → `assembly.bundle.artemis_pro_1mb_mono_pro`: Routing, requirements and cost_rollup_status need explicit owner/version assignment; not represented by composition lines.
- `bundle.artemis_budget_128` version 1 → `assembly.bundle.artemis_budget_128`: Routing, requirements and cost_rollup_status need explicit owner/version assignment; not represented by composition lines.
- `bundle.artemis_budget_128` version 2 → `assembly.bundle.artemis_budget_128.networked`: Routing, requirements and cost_rollup_status need explicit owner/version assignment; not represented by composition lines.
- `bundle.artemis_budget_128_hdd` version 1 → `assembly.bundle.artemis_budget_128_hdd`: Routing, requirements and cost_rollup_status need explicit owner/version assignment; not represented by composition lines.
- `bundle.artemis_budget_128_hdd` version 2 → `assembly.bundle.artemis_budget_128_hdd.networked`: Routing, requirements and cost_rollup_status need explicit owner/version assignment; not represented by composition lines.
- `offer.ram_64kb_module` version 1 → `assembly.offer.ram_64kb_module`: Routing, requirements and cost_rollup_status need explicit owner/version assignment; not represented by composition lines.
- `offer.ram_256kb_bank` version 1 → `assembly.offer.ram_256kb_bank`: Routing, requirements and cost_rollup_status need explicit owner/version assignment; not represented by composition lines.

### assembly_duplicate_line

- `bundle.aurelia_mono` version 1 → `part.logix_supplemental_distribution_media`: Same constituent already owned by composition; append would double count.
- `bundle.aurelia_color` version 1 → `part.logix_supplemental_distribution_media`: Same constituent already owned by composition; append would double count.
- `bundle.aurelia_plus_mono` version 1 → `part.logix_supplemental_distribution_media`: Same constituent already owned by composition; append would double count.
- `bundle.aurelia_plus_color` version 1 → `part.logix_supplemental_distribution_media`: Same constituent already owned by composition; append would double count.
- `bundle.artemis_128_mono` version 1 → `part.logix_supplemental_distribution_media`: Same constituent already owned by composition; append would double count.
- `bundle.artemis_128_mono` version 2 → `part.logix_supplemental_distribution_media`: Same constituent already owned by composition; append would double count.
- `bundle.artemis_128_color` version 1 → `part.logix_supplemental_distribution_media`: Same constituent already owned by composition; append would double count.
- `bundle.artemis_128_color` version 2 → `part.logix_supplemental_distribution_media`: Same constituent already owned by composition; append would double count.
- `bundle.artemis_256_color` version 1 → `part.logix_supplemental_distribution_media`: Same constituent already owned by composition; append would double count.
- `bundle.artemis_256_color` version 2 → `part.logix_supplemental_distribution_media`: Same constituent already owned by composition; append would double count.
- `bundle.artemis_pro_512_server` version 1 → `part.logix_supplemental_distribution_media`: Same constituent already owned by composition; append would double count.
- `bundle.artemis_pro_1mb_server` version 1 → `part.logix_supplemental_distribution_media`: Same constituent already owned by composition; append would double count.
- `bundle.artemis_256_mono_pro` version 1 → `part.logix_supplemental_distribution_media`: Same constituent already owned by composition; append would double count.
- `bundle.artemis_256_mono_pro` version 2 → `part.logix_supplemental_distribution_media`: Same constituent already owned by composition; append would double count.
- `bundle.artemis_pro_512_mono_pro` version 1 → `part.logix_supplemental_distribution_media`: Same constituent already owned by composition; append would double count.
- `bundle.artemis_pro_1mb_mono_pro` version 1 → `part.logix_supplemental_distribution_media`: Same constituent already owned by composition; append would double count.
- `bundle.artemis_budget_128` version 1 → `part.logix_supplemental_distribution_media`: Same constituent already owned by composition; append would double count.
- `bundle.artemis_budget_128` version 2 → `part.logix_supplemental_distribution_media`: Same constituent already owned by composition; append would double count.
- `bundle.artemis_budget_128_hdd` version 1 → `part.logix_supplemental_distribution_media`: Same constituent already owned by composition; append would double count.
- `bundle.artemis_budget_128_hdd` version 2 → `part.logix_supplemental_distribution_media`: Same constituent already owned by composition; append would double count.

### assembly_only_line

- `bundle.aurelia_network_upgrade` version 1 → `part.bundle.aurelia_network_upgrade.bundle_cables_media_manuals_and_carton_packout`: Not present in product composition: None each; role avoid double counting accessory supplied cables
- `bundle.artemis_network_upgrade` version 1 → `part.bundle.artemis_network_upgrade.bundle_cables_media_manuals_and_carton_packout`: Not present in product composition: None each; role avoid double counting accessory supplied cables
- `bundle.artemis_budget_128_hdd` version 1 → `part.hdd_5mb`: Not present in product composition: 1 each; role 5 MB drive; external enclosure, power and interface costed separately in budget assessment
- `bundle.artemis_budget_128_hdd` version 2 → `part.hdd_5mb`: Not present in product composition: 1 each; role 5 MB drive; external enclosure, power and interface costed separately in budget assessment
- `offer.ram_64kb_module` version 1 → `part.device.artemis_ram_64kb_bank_kit.kit_packout_and_instructions`: Not present in product composition: 1 each; role
- `offer.ram_256kb_bank` version 1 → `part.device.artemis_ram_256kb_bank_kit.kit_packout_and_instructions`: Not present in product composition: 1 each; role

### component_after_parent

- `bundle.artemis_budget_128_hdd` version 1 → `part.hdd_5mb`: Component introduction 1981-05-04 is after parent start 1980-05-19

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
- `offer.retail.connected_office` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `offer.retail.developer_workstation` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `offer.retail.development_team` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `offer.retail.connect_office` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `offer.retail.cpm_migration` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `bundle.proposed_artemis_accounts` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `bundle.proposed_artemis_accounts` version 2: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `bundle.proposed_artemis_pro_small_office` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `bundle.proposed_artemis_developer` version 1: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.
- `bundle.proposed_artemis_developer` version 2: Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.

### multi_computer_package

- `offer.retail.connected_office` version 1: Multiple supplied computers: connection placements must be allocated per host; aggregate capacity does not prove each machine is valid.
- `offer.retail.development_team` version 1: Multiple supplied computers: connection placements must be allocated per host; aggregate capacity does not prove each machine is valid.
- `bundle.proposed_artemis_pro_small_office` version 1: Multiple supplied computers: connection placements must be allocated per host; aggregate capacity does not prove each machine is valid.

### multiple_placements

- `offer.retail.connected_office` version 1 → `device.network_card_artemis`: Unique ref has distinct connection placements: [{"connected_to": "device.base_computer.artemis_pro", "quantity": 1, "used_socket": "expansion"}, {"connected_to": "device.base_computer.artemis", "quantity": 2, "used_socket": "expansion"}]
- `offer.retail.connected_office` version 1 → `device.rom_cartridge.aionix_server`: Unique ref has distinct connection placements: [{"connected_to": "device.base_computer.artemis_pro", "quantity": 1, "used_socket": "system_cartridge"}, {"connected_to": "device.base_computer.artemis", "quantity": 2, "used_socket": "system_cartridge"}]
- `offer.retail.development_team` version 1 → `device.artemis_video_card`: Unique ref has distinct connection placements: [{"connected_to": "device.base_computer.artemis_pro", "quantity": 1, "used_socket": "video_card"}, {"connected_to": "device.base_computer.artemis", "quantity": 4, "used_socket": "video_card"}]
- `offer.retail.development_team` version 1 → `device.network_card_artemis`: Unique ref has distinct connection placements: [{"connected_to": "device.base_computer.artemis_pro", "quantity": 1, "used_socket": "expansion"}, {"connected_to": "device.base_computer.artemis", "quantity": 4, "used_socket": "expansion"}]
- `offer.retail.development_team` version 1 → `device.rom_cartridge.aionix_server`: Unique ref has distinct connection placements: [{"connected_to": "device.base_computer.artemis_pro", "quantity": 1, "used_socket": "system_cartridge"}, {"connected_to": "device.base_computer.artemis", "quantity": 4, "used_socket": "system_cartridge"}]
- `bundle.proposed_artemis_pro_small_office` version 1 → `device.network_card_artemis`: Unique ref has distinct connection placements: [{"connected_to": "device.base_computer.artemis_pro", "quantity": 1, "used_socket": "expansion"}, {"connected_to": "device.base_computer.artemis", "quantity": 2, "used_socket": "expansion"}]
- `bundle.proposed_artemis_pro_small_office` version 1 → `device.rom_cartridge.aionix_server`: Unique ref has distinct connection placements: [{"connected_to": "device.base_computer.artemis_pro", "quantity": 1, "used_socket": "system_cartridge"}, {"connected_to": "device.base_computer.artemis", "quantity": 2, "used_socket": "system_cartridge"}]

### quotation_scope_unresolved

- `offer.retail.connect_office` version 1: Site survey/application qualification must determine remaining equipment, quantities and services; this is not a complete fixed-price package.
- `offer.retail.cpm_migration` version 1: Site survey/application qualification must determine remaining equipment, quantities and services; this is not a complete fixed-price package.

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
- `offer.retail.connected_office` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `offer.retail.connected_office` version 1 → `software.bpi_client_server`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `offer.retail.connected_office` version 1 → `edition.bpi_client_server.era_client`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `offer.retail.connected_office` version 1 → `software.business_tools_artemis`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `offer.retail.developer_workstation` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `offer.retail.developer_workstation` version 1 → `software.business_tools_artemis`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `offer.retail.developer_workstation` version 1 → `software.aion_c_ide`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `offer.retail.developer_workstation` version 1 → `software.artemis_sdk`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `offer.retail.development_team` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `offer.retail.development_team` version 1 → `software.aion_development_team`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_accounts` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_accounts` version 1 → `software.business_tools_artemis`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_accounts` version 1 → `software.bpi_suite`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_accounts` version 2 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_accounts` version 2 → `software.business_tools_artemis`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_accounts` version 2 → `software.bpi_suite`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_pro_small_office` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_pro_small_office` version 1 → `software.bpi_client_server`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_pro_small_office` version 1 → `edition.bpi_client_server.era_client`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_pro_small_office` version 1 → `software.business_tools_artemis`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_developer` version 1 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_developer` version 1 → `software.business_tools_artemis`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_developer` version 1 → `software.aion_c_ide`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_developer` version 1 → `software.artemis_sdk`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_developer` version 2 → `service.regular_support`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_developer` version 2 → `software.business_tools_artemis`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_developer` version 2 → `software.aion_c_ide`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.
- `bundle.proposed_artemis_developer` version 2 → `software.artemis_sdk`: Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.

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
    "unmerged_difference": [
      {
        "ref": "part.bundle.aurelia_network_upgrade.bundle_cables_media_manuals_and_carton_packout",
        "legacy": null,
        "proposed": 0
      }
    ],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  },
  {
    "owner": "bundle.artemis_network_upgrade",
    "version": 1,
    "assembly": "assembly.bundle.artemis_network_upgrade",
    "unmerged_difference": [
      {
        "ref": "part.bundle.artemis_network_upgrade.bundle_cables_media_manuals_and_carton_packout",
        "legacy": null,
        "proposed": 0
      }
    ],
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
    "unmerged_difference": [
      {
        "ref": "part.hdd_5mb",
        "legacy": 1,
        "proposed": 0
      }
    ],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  },
  {
    "owner": "bundle.artemis_budget_128_hdd",
    "version": 2,
    "assembly": "assembly.bundle.artemis_budget_128_hdd.networked",
    "unmerged_difference": [
      {
        "ref": "part.hdd_5mb",
        "legacy": 1,
        "proposed": 0
      }
    ],
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
    "unmerged_difference": [
      {
        "ref": "part.device.artemis_ram_64kb_bank_kit.kit_packout_and_instructions",
        "legacy": 1,
        "proposed": 0
      }
    ],
    "merged_static_difference": [],
    "merged_temporal_difference": [],
    "full_cutover_difference": []
  },
  {
    "owner": "offer.ram_256kb_bank",
    "version": 1,
    "assembly": "assembly.offer.ram_256kb_bank",
    "unmerged_difference": [
      {
        "ref": "part.device.artemis_ram_256kb_bank_kit.kit_packout_and_instructions",
        "legacy": 1,
        "proposed": 0
      }
    ],
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
    "added_lines": 1
  },
  {
    "assembly": "assembly.bundle.artemis_network_upgrade",
    "owner": "bundle.artemis_network_upgrade",
    "version": 1,
    "added_lines": 1
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
    "added_lines": 1
  },
  {
    "assembly": "assembly.bundle.artemis_budget_128_hdd.networked",
    "owner": "bundle.artemis_budget_128_hdd",
    "version": 2,
    "added_lines": 1
  },
  {
    "assembly": "assembly.offer.ram_64kb_module",
    "owner": "offer.ram_64kb_module",
    "version": 1,
    "added_lines": 1
  },
  {
    "assembly": "assembly.offer.ram_256kb_bank",
    "owner": "offer.ram_256kb_bank",
    "version": 1,
    "added_lines": 1
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
