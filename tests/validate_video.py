from data_paths import read_document, document_bytes
"""Validate shared Aurelia video resource budgets and BOM integration."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
catalog = read_document('generated/catalogs/logix-aion-technical-catalog-v2.json', root=root)
bom = read_document('generated/catalogs/hardware-bom.json', root=root)
records = {r['id']: r for items in catalog.values() if isinstance(items, list)
           for r in items if isinstance(r, dict) and 'id' in r}
hosts = ['computer.aurelia', 'computer.aurelia_plus']
chip = records['part.aurelia_video_chip']
cards = ['device.apple2_video_card', 'device.s100_video_card']
assert set(chip['used_in']) == set(hosts + cards)
for card in cards:
    spec = records[card]['specification']
    assert spec['video_ram_chip_count'] * records[spec['video_ram_chip_ref']]['specification']['capacity_kbit'] // 8 == spec['video_ram_kb'] == 16
    assembly = next(a for a in bom['assemblies'] if a['id'] == 'assembly.' + card)
    quantities = {line['ref']: line['quantity'] for line in assembly['lines']}
    assert quantities['part.aurelia_video_chip'] == 1
    assert quantities['part.aion_4116'] == 8
    assert quantities['part.aion_2114'] == 2
    assert 'part.aurelia_system_controller' not in quantities
design = chip['specification']['implementation_design']
buffers = design['internal_buffers']
assert buffers['pixel_fifo_page_count'] == 4
assert buffers['pixel_fifo_page_bytes'] == 40
assert buffers['pixel_bits'] == 4
assert buffers['pixel_fifo_bytes'] == buffers['pixel_fifo_page_count'] * buffers['pixel_fifo_page_bytes'] == 160
assert buffers['total_storage_bytes'] == sum(buffers[k] for k in [
    'character_attribute_row_cache_bytes', 'next_character_attribute_row_cache_bytes',
    'sprite_row_shifters_bytes', 'sprite_staging_bytes', 'pixel_fifo_bytes']) == 560
assert buffers['included_in_die_estimates']
ram_part = records['part.aion_4116']
assert ram_part['vendor'] == 'AION Labs'
assert ram_part['specification']['ports'] == ['single random read/write port']
assert ram_part['specification']['serial_register_bits'] == 0
# Storage budgets and fabrication costs are separate: both must reference the same dies.
costs = read_document('generated/models/manufacturing-costs.json', root=root)
models = costs['chip_fabrication_models']
assert models[chip['id']]['1978']['die_area_mm2'] == 52
assert models[ram_part['id']]['1978']['die_area_mm2'] == 18
assert abs(models[chip['id']]['1978']['good_packaged_chip_cost_usd'] +
           8 * models[ram_part['id']]['1978']['good_packaged_chip_cost_usd'] + 2 * models['part.aion_2114']['1978']['good_packaged_chip_cost_usd'] - 57.9031) < .001

for host in hosts:
    c = records[host]
    v = c['video']
    pop = c['memory']['video_physical_population']
    ram = records[pop['chip_ref']]['specification']
    capacity = pop['chip_count'] * ram['organization_words'] * ram['data_width_bits'] // 8
    assert capacity == c['memory']['video_ram_kb'] * 1024 == 16384
    assert pop['chip_count'] == pop['bank_data_width_bits'] == 8
    assert v['controller_ref'] == chip['id']
    s = v['sprites']
    assert s['pattern_bytes_per_sprite'] == s['width'] * s['height'] * s['bits_per_pixel'] // 8 == 128
    assert s['pattern_bytes_total'] == s['count'] * s['pattern_bytes_per_sprite'] == 640
    assert s['descriptor_bytes_total'] == s['descriptor_bank_count'] * s['count'] * s['descriptor_bytes_per_sprite'] == 80
    assert s['pattern_bytes_total'] + s['descriptor_bytes_total'] + s['spare_sprite_sram_bytes'] == s['reserved_sprite_sram_bytes'] == 1024
    assert s['available_in_all_modes'] and not s['pattern_double_buffered']
    pop_s = c['memory']['sprite_physical_population']
    ram_s = records[pop_s['chip_ref']]['specification']
    assert pop_s['chip_count'] * ram_s['organization_words'] * ram_s['data_width_bits'] // 8 == 1024
    assert pop_s == v['sprite_memory'] and pop_s['separate_bus']
    assert not ram_s['refresh_required']
    assert s['count'] == s['maximum_per_scanline'] == 5
    assert {m['columns'] for m in v['text_modes']} == {40, 80}
    for m in v['text_modes']:
        assert m['font_bytes'] == m['character_count'] * m['glyph_height'] == 2048
        assert m['character_map_bytes_per_buffer'] >= m['columns'] * m['rows']
        assert len(m['configurations']) == 4
        for cfg in m['configurations']:
            size = cfg['text_buffer_count'] * (m['character_map_bytes_per_buffer'] + m['attribute_map_bytes_per_buffer']) + m['font_bytes']
            assert size == cfg['allocated_bytes'] <= capacity
            assert size + cfg['remaining_video_ram_bytes'] == capacity
    assert {(m['width'], m['height'], m['bits_per_pixel']) for m in v['bitmap_modes']} == {
        (640, 200, 1), (320, 200, 2), (320, 200, 1), (320, 100, 4), (320, 100, 2), (160, 100, 4)}
    for m in v['bitmap_modes']:
        size = m['width'] * m['height'] * m['bits_per_pixel'] // 8
        assert size == m['bytes_per_framebuffer'] == m['stride_bytes'] * m['height']
        assert m['double_buffering'] == (2 * size <= capacity)
        assert m['sprites_available'] == 5
        expected = {(p, n) for p in ([1, 2] if m['double_buffering'] else [1]) for n in [0, 5]}
        assert {(x['framebuffer_count'], x['sprite_count']) for x in m['configurations']} == expected
        for cfg in m['configurations']:
            used = size * cfg['framebuffer_count']
            assert used == cfg['allocated_bytes'] <= capacity
            assert used + cfg['remaining_video_ram_bytes'] == capacity
    a = next(a for a in bom['assemblies'] if a['id'] == 'assembly.' + host + '.base')
    lines = {l['ref']: l for l in a['lines']}
    assert lines['part.aurelia_video_chip']['quantity'] == 1
    assert lines['part.aion_4116']['quantity'] == 8
    assert lines['part.aion_2114']['quantity'] == 2
    assert lines['part.aurelia_system_controller']['quantity'] == 1
    assert c['memory']['system_controller_ref'] == 'part.aurelia_system_controller'
    controller = records[c['memory']['system_controller_ref']]['specification']
    assert controller['refresh']['independent_of_cpu'] and controller['refresh']['all_installed_banks']
    assert c['processor']['clock_mhz'] in controller['host_clock_mhz']
    assert controller['dma']['active_transfer_engines'] == 1
    mm = records[c['memory']['organization_ref']]['specification']
    assert mm['controller_ref'] == c['memory']['system_controller_ref']
    assert mm['dma'] == controller['dma'] and mm['system_refresh'] == controller['refresh']
    assert not any('video_ram_chips' in ref or 'video_controller_revision' in ref for ref in lines)
assert records[hosts[0]]['video']['text_modes'] == records[hosts[1]]['video']['text_modes']
assert records[hosts[0]]['video']['bitmap_modes'] == records[hosts[1]]['video']['bitmap_modes']
profiles = {r['id']: r for r in records['technology.logix_digital_video']['specification']['raster_profiles']}
for monitor in ['device.mono_monitor_1', 'device.color_monitor_1', 'device.mono_monitor_2', 'device.color_monitor_2']:
    caps = records[monitor]['specification']['capabilities']
    assert set(caps['raster_ids']) <= profiles.keys()
    assert caps['preferred_raster_id'] in caps['raster_ids']
    assert all(profiles[r]['pixel_clock_mhz'] <= caps['maximum_pixel_clock_mhz'] for r in caps['raster_ids'])
    assert ('raster_640_200' in caps['raster_ids']) == monitor.endswith('_2')
print('Validated shared video modes, all buffer/sprite budgets, monitor profiles and eleven-chip video BOMs and integrated system controllers.')


assert records[hosts[0]]['video'] == records[hosts[1]]['video']
assert records[hosts[0]]['memory']['video_physical_population'] == records[hosts[1]]['memory']['video_physical_population']
for host in hosts:
    assert not {'text_mode', 'graphics_modes'} & records[host]['video'].keys()
    assert not {'text_mode', 'bitmap_mode'} & records[host]['video']['memory_layout'].keys()
# Scan current project sources and generated reports, excluding repository metadata and caches.
for path in root.rglob('*'):
    if not path.is_file() or any(p.startswith('.') or p == '__pycache__' for p in path.relative_to(root).parts):
        continue
    assert ('v' + 'ram').encode() not in path.read_bytes().lower(), path
