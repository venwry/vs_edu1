"""Canonical product categories/IDs, complete projection coverage and archive aliases."""
import json,hashlib,sys,copy
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from data_store import read_document,registry
from validate_products import validate_products
from validate_data import validate_collections
validate_collections()
source={f:read_document(f) for f in registry()['files']};products=source['data/product-catalog.json']['products'];ids={p['id'] for p in products}
assert Counter(p['category'] for p in products)=={'computer':15,'computer_software_bundle':15,'expansion_kit':11,'software':19,'computer_system':3}
assert len(ids)==63
for p in products:
 assert p['id'].startswith('computer_system.' if p['category']=='computer_system' else 'product.')
 assert not {'record_kind','source_group'}&p.keys()
view=read_document('catalog:logix-aion-technical-catalog-v2')
assert {p['id'] for p in view['product_catalog']['products']}==ids
listed=[p['id'] for key in ['offered_bundles','proposed_bundles','commercial_offerings'] for p in view[key]]
assert Counter(listed)==Counter(ids)
assert len(view['computers'])==6
assert {k:sum(p['computer_line']==k for p in products) for k in ['Aurelia','Artemis','Athena']}=={'Aurelia':4,'Artemis':8,'Athena':2}
assert not any('record_kind' in p or 'source_group' in p for key in ['computers','offered_bundles','proposed_bundles','commercial_offerings'] for p in view[key])
raw=json.loads((R/'generated/models/pricing-results.json').read_text());normalized=read_document('generated/models/pricing-results.json');aliases=registry()['record_id_aliases']
for before,after in zip(raw['products'],normalized['products']):assert after['id']==aliases.get(before['id'],before['id'])
assert aliases['bundle.artemis_128_mono']=='product.artemis_128_mono'
assert aliases['product.retail.connected_office']=='computer_system.retail.connected_office'
for mutation in [lambda p:p.update(category='system_bundle'),lambda p:p.update(id='bundle.invalid'),lambda p:p.update(source_group='retail'),lambda p:p.update(category='software')]:
 docs=copy.deepcopy(source);p=next(p for p in docs['data/product-catalog.json']['products'] if p['id']=='product.artemis_128_mono');mutation(p)
 try:validate_products(docs,{})
 except ValueError:pass
 else:raise AssertionError('Invalid product discriminator accepted')
for path,digest in read_document('tests/fixtures/composition-migration.json')['financial_files'].items():assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
print('PASS: 63 products, five categories, canonical ID prefixes, complete views, 14 selectors, obsolete fields rejected and unchanged financial archives')
