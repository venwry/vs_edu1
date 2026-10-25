"""Software source ownership, delivery graphs and commercial-package integrity."""
import copy,hashlib,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from data_store import read_document,registry,project_collections
from validate_data import validate_collections
from validate_products import validate_products
from completion_audit import historical_bom
validate_collections()
source={f:read_document(f) for f in registry()['files']}
assert len(source)==21 and not (R/'data/software-products.json').exists()
es=source['data/software-editions.json'];assert 'platform_editions' not in es
E={e['id']:e for e in es['software_editions']};D={d['id']:d for d in source['data/devices.json']['devices']};P={p['id']:p for p in source['data/product-catalog.json']['products']}
assert len(E)==32 and len({e['software_line_id'] for e in E.values()})==14
assert len(P)==63
for e in E.values():
 assert not set(e)&{'delivery','sold_separately','product_ref','physical_media_refs'}
 assert all(e[k] for k in ['software_line_id','software_line_name','software_line_category','vendor'])
 assert e['composition_history']
for id in ['software.cpm_model_ii','software.microsoft_basic_aurelia']:
 assert E[id]['distribution']['fulfillment']=='external_supplier'
 assert E[id]['composition_history'][0]['composition_definition']==[]
 assert not any(p['category']=='software' and any(l['ref']==id for h in p['composition_history'] for l in h['composition_definition']) for p in P.values())
for d in D.values():
 assert 'software_refs' not in d
 if d['category']=='rom_cartridge':
  ls=d['composition_history'][0]['composition_definition'];refs=[l['ref'] for l in ls if l['ref'] in E];assert len(refs)==1
  s=E[refs[0]];assert s['distribution']['medium']=='cartridge'
  parts=s['composition_history'][0]['composition_definition'];assert len(parts)==2
  assert any(l['ref'].endswith('.license_document') for l in parts)
  assert any(l['ref'].endswith('.software_documentation') for l in parts)
for id in ['software.aurelia_sdk','software.artemis_sdk']:
 refs={l['ref']:l for l in E[id]['composition_history'][0]['composition_definition']}
 for suffix in ['interfaces_media','examples_media','utilities_media']:assert refs['part.'+id+'.'+suffix]['quantity'] is None
 assert 'Compiler/IDE is separately supplied' in E[id]['distribution']['toolchain']
for id in ['product.aion_development_team','product.bpi_client_server']:
 p=P[id];refs={l['ref'] for l in p['composition_history'][0]['composition_definition']}
 assert len(refs)==5 and all(not r.startswith('product.') for r in refs)
 assert sum(r.endswith('.package_license') for r in refs)==1
 assert sum(r.endswith('.package_packaging') for r in refs)==1
 assert p['commercial_terms']['hardware_included'] is False
 for r in refs&E.keys():assert not any(l['ref'].endswith(('.license_document','.software_packaging')) for l in E[r]['composition_history'][0]['composition_definition'])
t=P['product.aion_development_team']['commercial_terms'];assert (t['total_distribution_diskettes'],t['total_printed_pages'],t['concurrent_developer_sessions'])==(12,1000,4)
assert P['product.bpi_client_server']['commercial_terms']['client_seat_count'] is None
cartridge_editions={e['id'] for e in E.values() if e['distribution']['medium']=='cartridge'}
for p in P.values():
 for h in p['composition_history']:
  assert not any(l['ref'] in P for l in h['composition_definition'])
  assert not any(l['ref'] in cartridge_editions for l in h['composition_definition']),p['id']
# Reject mismatched line labels, cross-domain cycles, duplicate cartridge delivery.
def reject(change):
 docs=copy.deepcopy(source);change(docs)
 try:validate_products(docs,{})
 except ValueError:return
 raise AssertionError('Invalid software graph accepted')
reject(lambda d:d['data/software-editions.json']['software_editions'][1].update(software_line_name='different Abacus name'))
def cycle(d):
 e=next(e for e in d['data/software-editions.json']['software_editions'] if e['id']=='software.aionix')
 e['composition_history'][0]['composition_definition'][0]['ref']='device.rom_cartridge.aionix'
reject(cycle)
def duplicate(d):
 p=next(p for p in d['data/product-catalog.json']['products'] if p['id']=='product.artemis_128_mono')
 p['composition_history'][0]['composition_definition'].append(dict(ref='software.aionix',quantity=1,unit='each',role='',condition='always',quantity_status='defined',element_type='attached_product'))
reject(duplicate)
# Legacy groups are derived only; old inventories may change only by the explicit reviewed delta.
view=read_document('catalog:logix-aion-technical-catalog-v2');assert len(view['software_products'])==14
for line in view['software_products']:assert set(line['edition_refs'])=={e['id'] for e in E.values() if e['software_line_id']==line['id']}
historical_bom(read_document('catalog:hardware-bom'))
for f,h in read_document('tests/fixtures/composition-migration.json')['financial_files'].items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
print('PASS: 32 edition owners, 14 derived lines, 19 commercial products, cartridge/software graph, media unknowns, package licence boundaries and unchanged finances')
