"""Validate the planned Athena configurations independently of historical forecasts."""
import json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
catalog = json.loads((root / 'generated/catalogs/logix-aion-technical-catalog-v2.json').read_text())
plan = json.loads((root / 'generated/catalogs/athena-1983-program.json').read_text())
records = {r['id']: r for values in catalog.values() if isinstance(values, list)
           for r in values if isinstance(r, dict) and 'id' in r}
for product, capacity, modules, module_size, disk in [
    ('computer.athena', 256, 2, 128, 5),
    ('computer.athena_server', 1024, 4, 256, 20),
]:
    computer = records[product]
    config = computer['memory']['configurations'][0]
    module = records[config['module_ref']]['specification']
    chip = records[module['chip_type_ref']]['specification']
    assert config['ram_kb'] == capacity == modules * module_size
    assert config['populated_modules'] == modules
    assert module['capacity_kb'] == module_size == module['chips'] * chip['capacity_kbit'] // 8
    assert chip['node_um'] == 2 and chip['capacity_kbit'] == 64
    assert module['chips'] == module['ranks'] * 16
    assert config['populated_banks'] * 2 == modules
    assert computer['memory']['video_ram_kb'] == 64
    assert computer['storage']['internal_hdd']['capacity_mb'] == disk
    fdd = computer['storage']['internal_fdd']
    assert (fdd['count'], fdd['size_inch'], fdd['format']) == (1, 5.25, 'DS/DD')
    assert computer['network']['included'] and computer['network']['card_count'] == 1
    assert computer['io_and_expansion']['rom_eeprom_cartridge_slots']['count'] == 0
    assert computer['io_and_expansion']['eeprom_bios']['included']
    assert not config['shipping_configuration']
    bom = next(b for b in plan['computer_boms'] if b['computer_ref'] == product)
    counts = {line['ref']: line['quantity'] for line in bom['lines']}
    assert counts[config['module_ref']] == modules
    assert counts['part.era2'] == counts['device.artemis_video_card_64kb'] == counts['device.network_card_artemis'] == 1
assert records['part.era1']['manufacturing_planning']['node_um'] == 3
assert records['part.era2']['manufacturing_planning']['initial_manufacturer'] == 'AION Labs only'
assert records['software.aionix2']['edition_refs'] == []
assert plan['launch']['premiere_date'] == '1983-05-16'
print('PASS: Athena base/server RAM, 2 µm chips, storage, graphics, NIC, EEPROM-only boot and planning status.')
