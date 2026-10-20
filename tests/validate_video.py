"""Validate shared Aurelia video resource budgets and BOM integration."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
catalog = json.loads((root / 'logix_aion_technical_catalog_v2.json').read_text())
bom = json.loads((root / 'hardware_bom.json').read_text())
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
    assert quantities['bompart.part.aurelia_video_chip'] == 1
    assert quantities['bompart.part.aion_4116'] == 8
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
costs = json.loads((root / 'manufacturing_costs.json').read_text())
models = costs['chip_fabrication_models']
assert models[chip['id']]['1978']['die_area_mm2'] == 48
assert models[ram_part['id']]['1978']['die_area_mm2'] == 18
assert abs(models[chip['id']]['1978']['good_packaged_chip_cost_usd'] +
           8 * models[ram_part['id']]['1978']['good_packaged_chip_cost_usd'] - 46.3048) < .001

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
    assert s['total_pattern_and_position_bytes'] == s['count'] * (128 + s['position_bytes_per_sprite']) == 660
    assert s['reserved_video_ram_bytes'] == 768
    assert s['count'] == s['maximum_per_scanline'] == 5
    assert {m['columns'] for m in v['text_modes']} == {40, 80}
    for m in v['text_modes']:
        assert m['font_bytes'] == m['character_count'] * m['glyph_height'] == 2048
        assert m['character_map_bytes_per_buffer'] >= m['columns'] * m['rows']
        assert len(m['configurations']) == 4
        for cfg in m['configurations']:
            size = cfg['text_buffer_count'] * (m['character_map_bytes_per_buffer'] + m['attribute_map_bytes_per_buffer']) + m['font_bytes']
            size += s['reserved_video_ram_bytes'] if cfg['sprite_count'] else 0
            assert size == cfg['allocated_bytes'] <= capacity
            assert size + cfg['remaining_video_ram_bytes'] == capacity
    assert {(m['width'], m['height'], m['bits_per_pixel']) for m in v['bitmap_modes']} == {
        (640, 200, 1), (320, 200, 2), (320, 200, 1), (320, 100, 4), (320, 100, 2), (160, 100, 4)}
    for m in v['bitmap_modes']:
        size = m['width'] * m['height'] * m['bits_per_pixel'] // 8
        assert size == m['bytes_per_framebuffer'] == m['stride_bytes'] * m['height']
        expected = {(1, 0)} if size == 16000 else {(1, 0), (2, 0), (1, 5)}
        assert {(x['framebuffer_count'], x['sprite_count']) for x in m['configurations']} == expected
        for cfg in m['configurations']:
            used = size * cfg['framebuffer_count'] + (768 if cfg['sprite_count'] else 0)
            assert used == cfg['allocated_bytes'] <= capacity
            assert used + cfg['remaining_video_ram_bytes'] == capacity
    a = next(a for a in bom['assemblies'] if a['id'] == 'assembly.' + host + '.base')
    lines = {l['ref']: l for l in a['lines']}
    assert lines['bompart.part.aurelia_video_chip']['quantity'] == 1
    assert lines['bompart.part.aion_4116']['quantity'] == 8
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
print('Validated shared video modes, all buffer/sprite budgets, monitor profiles and nine-chip BOMs.')


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
