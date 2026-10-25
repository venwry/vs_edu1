from data_paths import read_document, document_bytes
"""Validate hardware arithmetic, population rules and BOM cost boundaries."""
import json
from pathlib import Path
from collections import Counter
import jsonschema
root=Path(__file__).resolve().parents[1]
def read(name):return read_document(name, root=root)
t=read('generated/catalogs/logix-aion-technical-catalog-v2.json');bom=read('generated/catalogs/hardware-bom.json')
jsonschema.Draft202012Validator(read('schemas/legacy/hardware_bom.schema.json')).validate(bom)
records={r['id']:r for v in t.values() if isinstance(v,list) for r in v if isinstance(r,dict) and 'id'in r}
products={r['catalog_ref']:r for r in bom['products']};components={r['id']:r for r in bom['components']};assemblies={r['id']:r for r in bom['assemblies']}
assert len(products)==len(bom['products']);assert len(components)==len(bom['components']);assert len(assemblies)==len(bom['assemblies'])
assert {r['id'] for r in t['computers']} <= set(products) <= set(records)
assert all(d['id'] in assemblies or d['manufacturing_status']=='excluded_from_active_production' for d in t['devices'])
assert {r['catalog_ref'] for r in bom['offers']}=={r['id'] for r in t['offered_bundles']}
for p in products.values():
 assert set(p['assembly_refs'])<=assemblies.keys()|{id for id,p in components.items() if p['bom_role']=='material'}
 assert bool(p['assembly_refs'])==(p['production_status']!='excluded'),p['catalog_ref']
for c in components.values():
 assert 'catalog_ref' not in c and records[c['id']]==c
 if c['id'] in ['part.dram_128kbit','device.artemis_ram_module_64kb','device.artemis_ram_module_prototype']:assert c['bom_role']=='specification'
for a in assemblies.values():
 for l in a['lines']:
  assert l['ref'] in components or l['ref'] in assemblies,(a['id'],l['ref'])
  assert (l['quantity'] is None)==(l['quantity_status']=='unresolved')
 assert a['cost_rollup_status']=='blocked_pending_component_and_routing_definition'
def explode(id,stack=()):
 assert id not in stack,('cycle',stack,id)
 if id in components:return Counter({id:1})
 out=Counter()
 for l in assemblies[id]['lines']:
  child=explode(l['ref'],stack+(id,))
  if l['quantity'] is not None:out.update({k:v*l['quantity'] for k,v in child.items()})
 return out # known-quantity inventory ONLY, never a price for unresolved lines
for id in assemblies:explode(id)
for id in ['device.ram_64kb_x32','device.ram_128kb_x32','device.ram_256kb_x32','device.ram_256kb_x32_2um']:
 s=records[id]['specification'];chip=records[s['chip_type_ref']]['specification']
 assert s['data_width_bits']==32 and s['chips_per_rank']==32
 assert s['chips']==s['ranks']*32 and chip['data_width_bits']==1
 assert s['chips']*chip['capacity_kbit']/8==s['capacity_kb']
 assert s['bank_capacity_kb']==2*s['capacity_kb'] and s['bank_data_width_bits']==32
 inv=explode(id);assert inv[s['chip_type_ref']]==s['chips']
for id in ['computer.artemis','computer.artemis_pro']:
 mem=records[id]['memory'];assert 'module_ref' not in mem
 assert mem['ram_sockets']==8 and mem['bank_count']==4
 assert mem['modules_per_bank']==2 and mem['bank_data_width_bits']==32 and mem['mixed_density_allowed'] is False
 assert len({c['id'] for c in mem['configurations']})==len(mem['configurations'])
 assert mem['default_configuration'] in {c['id'] for c in mem['configurations']}
 for cfg in mem['configurations']:
  module=records[cfg['module_ref']]['specification']
  assert cfg['populated_modules']==cfg['populated_banks']*2<=8
  assert cfg['ram_kb']==module['capacity_kb']*cfg['populated_modules']
  assert cfg['data_chip_count']==module['chips']*cfg['populated_modules']
  assert len(cfg['bank_population'])==cfg['populated_banks']
  assert [slot for bank in cfg['bank_population'] for slot in bank['slots']]==list(range(cfg['populated_modules']))
  from compositions import resolve
  inv=Counter()
  for l in resolve(cfg['product_ref'],version=1)['leaves']:
   if l['total_quantity'] is not None and cfg['module_ref'] in l['path']:inv[l['ref']]+=l['total_quantity']
  assert inv[module['chip_type_ref']]==cfg['data_chip_count']
shipping={id:{c['ram_kb']:(c['populated_modules'],c['populated_banks'],c['data_chip_count']) for c in records[id]['memory']['configurations'] if c['shipping_configuration']} for id in ['computer.artemis','computer.artemis_pro']}
assert shipping['computer.artemis']=={128:(2,1,64),256:(2,1,128)}
assert set(shipping['computer.artemis_pro'])=={512,1024} # Shipment follows the product composition start.
assert {c['ram_kb'] for c in records['computer.artemis_pro']['memory']['configurations']}=={512,1024}
for id,expected in [('computer.aurelia',48),('computer.aurelia_plus',64)]:
 pop=records[id]['memory']['physical_population'];assert pop['data_chip_count']*records[pop['chip_ref']]['specification']['capacity_kbit']/8==expected
for id in ['product.ram_64kb_module','product.ram_256kb_bank']:
 offer=records[id];cfg=offer['configuration'];assert sum(records[m['module_ref']]['specification']['capacity_kb']*m['quantity'] for m in cfg['modules'])==cfg['capacity_kb']
 assert records['device.aurelia_ram_16kb_card']['category']=='memory_expansion'
for b in t['offered_bundles']:
 cfg=b.get('computer_configuration',{})
 if cfg.get('ram_configuration_id'):
  c=next(c for c in records[b['computer_ref']]['memory']['configurations'] if c['id']==cfg['ram_configuration_id'])
  assert c['shipping_configuration'] and c['ram_kb']==cfg['ram_kb']
for offer in bom['offers']:
 a=assemblies[offer['assembly_ref']]
 assert offer['included_host']==(offer['kind'] in ['computer','computer_software_bundle','computer_system'])
 if offer['kind']=='expansion_kit':assert not any(l['ref'].startswith('assembly.computer.') for l in a['lines'])
 if 'artemis_pro' in offer['catalog_ref'] and offer['kind']!='computer_system':
  inv=explode(a['id']);assert inv['part.device.network_card_artemis.network_card_pcb']==1
 for v in offer.get('variants',[]):
  inv=explode(v['assembly_ref']);assert inv['part.device.network_card_artemis.network_card_pcb']==1
  refs=[l['ref'] for l in assemblies[v['assembly_ref']]['lines']]
  assert 'device.rom_cartridge.aionix_server' in refs and 'device.rom_cartridge.aionix' not in refs
assert {a for a in assemblies if a.startswith('device.network_hub.')}=={f'device.network_hub.{n}_port' for n in [4,8,16]}
print(f'Validated RAM arithmetic and paired banks; {len(products)} hardware records, {len(assemblies)} BOM assemblies and all {len(bom["offers"])} offers. Unresolved lines remain blocked for costing.')
