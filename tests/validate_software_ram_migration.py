from data_paths import read_document, document_bytes, document_text
"""Semantic regression checks for product editions and shared physical modules."""
import json, hashlib, subprocess, sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(p):return read_document(p, root=R)
c=read('generated/catalogs/logix-aion-technical-catalog-v2.json');b=read('generated/catalogs/hardware-bom.json');site=read('generated/catalogs/site-pages.json')
records={r['id']:r for v in c.values() if isinstance(v,list) for r in v if isinstance(r,dict) and 'id' in r}
products={r['id']:r for r in c['software_products']};editions={r['id']:r for r in c['platform_editions']}
assert len(products)==14 and len(editions)==32
assert len({p['name'] for p in products.values()})==len(products)
for p in products.values():
 assert set(p['edition_refs'])=={e['id'] for e in editions.values() if e['product_ref']==p['id']}
for e in editions.values():
 assert e['product_ref'] in products and 'edition_refs' not in e and 'category' not in e
 assert e['version'] is None or isinstance(e['version'],str)
assert records['software.abacus_2']['name']=='Abacus 2.0 (CP/M edition)'
assert records['edition.abacus_2.era']['name']=='Abacus 2.0 (AIONix edition)'
assert records['software.abacus_2']['product_ref']==records['edition.abacus_2.era']['product_ref']=='software.product.abacus'
assert 'artemis_native_extensions' not in records['software.abacus_2']
assert records['edition.abacus_2.era']['artemis_native_extensions']
for old,new in site['record_redirects'].items():
 assert old not in records and new in records and new not in site['record_redirects']
assert 'device.artemis_ram_64kb_bank_kit' not in records
assert 'device.artemis_ram_256kb_bank_kit' not in records
assert records['computer.artemis']['memory']['configurations'][2]['ram_kb']==256
ar=next(x for x in records['computer.artemis']['memory']['configurations'] if x['id']=='m128_256')
at=records['computer.athena']['memory']['configurations'][0]
assert ar['module_ref']==at['module_ref']=='device.ram_128kb_x32'
assert ar['data_chip_count']==at['data_chip_count']==128
card=records['device.aurelia_ram_16kb_card']
assert card['category']=='memory_expansion' and card['capacity_kb']==16
p=R/'generated/models/manufacturing-costs.json';before=hashlib.sha256(p.read_bytes()).digest()
run=subprocess.run([sys.executable,str(R/'tools/build_cost_assessment.py')],capture_output=True,text=True)
assert run.returncode!=0 and 'Cost rebuild blocked: qualify revised module routing/allowances' in run.stderr
assert hashlib.sha256(p.read_bytes()).digest()==before
print('PASS: 14 products, 32 editions, identity redirects, shared modules, preserved capacities and fail-closed cost publication')
