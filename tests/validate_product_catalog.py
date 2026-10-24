"""Commercial ownership, socket authority and unchanged archived physical/economic facts."""
import sys,json,hashlib,copy,tempfile,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from data_store import read_document,registry,project_collections
from validate_data import validate_collections
from validate_products import validate_products
validate_collections()
source={f:read_document(f) for f in registry()['files']};pc=source['data/product-catalog.json'];products={p['id']:p for p in pc['products']}
assert all(not (R/'data'/f).exists() for f in ['computers.json','offers.json','product-boms.json','retail-catalog.json'])
assert {line:sum(p['computer_line']==line for p in products.values()) for line in ['Aurelia','Artemis','Athena']}=={'Aurelia':4,'Artemis':8,'Athena':2}
assert len(pc['retired_configuration_ids'])==9
for p in products.values():
 if p['record_kind']=='platform':
  assert not any(k in p for k in ['memory','video','storage','chipset','compatible_devices','compatible_software'])
 if p.get('computer_line'):
  assert p['main_product']['device_ref'].startswith('device.chassis.')
  assert all(c['used_socket'] is not None for c in p['connected_devices'])
f=read_document('tests/fixtures/product-catalog-migration.json');b=read_document('catalog:hardware-bom');a={x['id']:x for x in b['assemblies']}
def flat(id,q=1):
 if id not in a:return [[id,q]]
 return [v for l in a[id]['lines'] for v in flat(l['ref'],None if q is None or l['quantity'] is None else q*l['quantity'])]
for id,expected in f['assembly_inventories'].items():
 if id in pc['retired_configuration_ids']:assert id not in a;continue
 actual=hashlib.sha256(json.dumps(sorted(flat(id),key=lambda x:(x[0],str(x[1]))),sort_keys=True,separators=(',',':')).encode()).hexdigest()
 assert actual==expected,id
for path,expected in f['financial_files'].items():assert hashlib.sha256((R/path).read_bytes()).hexdigest()==expected,path
# Invalid edited source must fail before it can be written.
def reject(mutator):
 docs=copy.deepcopy(source);p=next(p for p in docs['data/product-catalog.json']['products'] if p['id']=='bundle.artemis_128_mono');mutator(p,docs)
 try:validate_products(docs,project_collections(docs))
 except ValueError:return
 raise AssertionError('Invalid commercial population accepted')
reject(lambda p,d:p['connected_devices'][0].update(quantity=100))
reject(lambda p,d:p['connected_devices'][0].update(used_socket='does_not_exist'))
reject(lambda p,d:p.update(computer_line='Athena'))
reject(lambda p,d:p['attached_products'].append({'software_ref':'software.aionix','quantity':1}))
reject(lambda p,d:next(e for e in p['connected_devices'] if e['device_ref']=='device.ram_64kb_x32').update(quantity=1))
# The chassis, not a product-local whitelist, controls what fits.
reject(lambda p,d:next(s for dev in d['data/devices.json']['devices'] if dev['id']==p['main_product']['device_ref'] for g in dev['expansion_socket_groups'] for s in g['sockets'] if s['id']=='ram').update(compatible_device_refs=[]))
print('PASS: 14 line-qualified products, source consolidation, retained BOM equivalence, immutable finances and negative socket/entitlement checks')
