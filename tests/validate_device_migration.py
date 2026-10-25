"""Audit device BOM ownership, physical definitions, family splitting and archival invariance."""
import json,hashlib,sys,copy,tempfile,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from data_store import read_document,store_document,normalize_component_ids,registry
from validate_data import validate_collections
f=read_document('tests/fixtures/device-migration.json');reg=registry()
digest=lambda v:hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
validate_collections()
assert not (ROOT/'data/peripherals.json').exists()
devices=read_document('data/devices.json')['devices'];stored=read_document('data/assemblies.json')['assemblies'];by={d['id']:d for d in devices}
assert len(by)==len(devices)
assert set(f['expected_device_ids'])-set(by)=={'device.artemis_ram_64kb_module'}
assert not set(f['moved_assembly_ids'])&{a['id'] for a in stored}
assert all('bom_assembly_refs' not in d for d in devices)
assert 'bom_assembly_definition' not in by['device.artemis_ram_module_64kb']
for n in [4,8,16]:
 d=by[f'device.network_hub.{n}_port'];assert d['specification']['port_count']==n
 assert 'port_count_options' not in d['specification']
 lines={l['ref']:l for l in d['composition_history'][0]['composition_definition']}
 assert lines['part.device.network_hub.network_connector']['quantity']==n
 assert lines['part.device.network_hub.per_port_transceiver_termination_and_protection_assembly']['quantity']==n
 for kind in ['pcb','psu','enclosure']:assert lines[f'part.device.network_hub.{n}_port_{kind}']['quantity']==1
cost=read_document('generated/models/manufacturing-costs.json')
for n in [4,8,16]:
 id=f'device.network_hub.{n}_port';rows=[r for r in cost['products'] if r['catalog_ref']==id];assert len(rows)==1 and rows[0]['id']==id and rows[0]['assembly_ref']==id
for path,h in f['frozen_files'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h,path
# Editing the legacy in-memory assembly view writes back to the device owner, not a duplicate row.
with tempfile.TemporaryDirectory() as t:
 root=Path(t)
 for directory in ['data','schemas']:shutil.copytree(ROOT/directory,root/directory)
 bom=read_document('catalog:hardware-bom',root);snapshot={p:p.read_bytes() for p in (root/'data').glob('*.json')}
 store_document('catalog:hardware-bom',bom,root)
 assert all(p.read_bytes()==b for p,b in snapshot.items()),'Roundtrip rewrote source ownership/order'
 row=next(a for a in bom['assemblies'] if a['id']=='device.network_card_aurelia');row['lines'][0]['quantity']=2
 store_document('catalog:hardware-bom',bom,root)
 assert next(d for d in read_document('data/devices.json',root)['devices'] if d['id']==row['id'])['composition_history'][0]['composition_definition'][0]['quantity']==2
 assert (root/'data/assemblies.json').read_bytes()==snapshot[root/'data/assemblies.json']
 # A device-to-device cycle must be rejected before any source write.
 row['lines'][0]['ref']=row['id'];before={p:p.read_bytes() for p in (root/'data').glob('*.json')}
 try:store_document('catalog:hardware-bom',bom,root)
 except ValueError:pass
 else:raise AssertionError('Device BOM cycle accepted')
 assert all(p.read_bytes()==b for p,b in before.items())
print('PASS: original device definitions retained, hub variants, immutable archives and write-through integrity')
