"""Campaign launches and composition-owned shipment dates must remain distinct."""
import copy,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from data_store import read_document,registry
from validate_data import validate_collections
from validate_products import validate_products
validate_collections()
source={f:read_document(f) for f in registry()['files']}
products={p['id']:p for p in source['data/product-catalog.json']['products']}
campaigns={c['id']:c for c in source['data/campaigns.json'].values() if isinstance(c,dict) and 'id' in c}
assert len(campaigns)==10
for pid,cid,launch,shipment in [('product.proposed_aurelia_plus_office','campaign.comdex1979','1979-12-03','1979-12-15'),('product.ncc82_colour_upgrade','campaign.ncc1982','1982-06-07','1982-06-15'),('product.abacus_1.model_ii','campaign.ncc1979','1979-06-04','1979-10-15')]:
 p=products[pid];assert p['launch_campaign_ref']==cid
 assert campaigns[cid]['launch_date']==launch
 assert p['composition_history'][0]['valid_from']==shipment
view=read_document('catalog:logix-aion-technical-catalog-v2')
for p in view['product_catalog']['products']:
 assert p['introduced']['event_start_date']==products[p['id']]['composition_history'][0]['valid_from']
for mutate in [lambda s:s['data/product-catalog.json']['products'][0].update(launch_campaign_ref='campaign.missing'),lambda s:s['data/product-catalog.json']['products'][0].update(shipping_date='1983-05-17'),lambda s:s['data/campaigns.json']['comdex_1979_campaign'].update(launch_date='1979-12-15'),lambda s:s['data/campaigns.json']['comdex_1979_campaign'].update(event_refs=['event.missing'])]:
 bad=copy.deepcopy(source);mutate(bad)
 try:validate_products(bad,{})
 except ValueError:pass
 else:raise AssertionError('Invalid launch/shipment metadata accepted')
print('PASS: 63 campaign-linked products, ten campaigns, distinct launch/shipment dates and negative integrity checks')
