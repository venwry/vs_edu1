"""Restored multi-host products retain placements and avoid duplicate NIC cables."""
import copy,json,sys,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from data_store import read_document,registry
from validate_data import validate_collections
from validate_products import validate_products
from simulate_compositions import simulate
validate_collections()
source={f:read_document(f) for f in registry()['files']}
p={x['id']:x for x in source['data/product-catalog.json']['products']}
expected={'product.retail.connected_office':3,'product.retail.development_team':5,'product.proposed_artemis_pro_small_office':3}
assert {x['id'] for x in p.values() if x['category']=='computer_system'}==set(expected)
for id,n in expected.items():
 x=p[id];assert x['computer_line'] is None
 for h in x['composition_history']:
  ls=h['composition_definition'];assert sum(l['quantity'] for l in ls if l['element_type']=='main_product')==n
  assert sum(l['quantity'] for l in ls if l['ref']=='device.network_card_artemis')==n
  assert not any(l['ref'] in ['part.logix_network_cable','part.logix_supplemental_distribution_media'] for l in ls)
  assert any(l['ref'].startswith('device.network_hub.') for l in ls)
  assert any(l.get('placements') for l in ls)
  assert not any(l['ref'] in p for l in ls)
  assert 'legacy_assembly_ref' not in h
assert p['product.proposed_artemis_pro_small_office']['commercial_terms']['shipping_date'] is None
for id in ['product.retail.connected_office','product.retail.development_team']:assert p[id]['catalogue_status']=='quotation_only'
assert {x['product_ref'] for x in source['data/product-catalog.json']['catalog_editions'][0]['solutions']}>= {'product.retail.connected_office','product.retail.development_team'}
# Existing bookmarked IDs and archived price references resolve to the restored records.
reg=registry()
for old,new in [('offer.retail.connected_office','product.retail.connected_office'),('offer.retail.development_team','product.retail.development_team'),('bundle.proposed_artemis_pro_small_office','product.proposed_artemis_pro_small_office')]:assert reg['record_id_aliases'][old]==new
pricing=read_document('generated/models/pricing-results.json')
assert 'product.proposed_artemis_pro_small_office' in {row['id'] for row in pricing['products']}
assert 'bundle.proposed_artemis_pro_small_office' not in {row['id'] for row in pricing['products']}
bad=copy.deepcopy(source);x=next(x for x in bad['data/product-catalog.json']['products'] if x['id'] in expected)
x['composition_history'][0]['composition_definition']=[l for l in x['composition_history'][0]['composition_definition'] if l['element_type']!='main_product']
try:validate_products(bad,{})
except ValueError:pass
else:raise AssertionError('Computer system without computers accepted')
r=simulate();assert r['summary']['findings_by_kind']['multi_computer_package']==3
assert r['summary']['findings_by_kind']['no_legacy_product_bom']==25
for f,h in read_document('tests/fixtures/composition-migration.json')['financial_files'].items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
print('PASS: three restored systems, canonical aliases, host placements, no duplicated cables, historical availability and unchanged financial files')
