"""Validate the effective catalogue, price ceilings and incomplete-package labels."""
import hashlib
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
x=json.loads((R/'retail_catalog_1982_results.json').read_text())
m=json.loads((R/'pricing_results.json').read_text())
assert len(x['solutions'])==7 and len(x['upgrades'])==5
assert x['effective_from']=='1982-11-29'
assert len({p['id'] for p in x['solutions']+x['upgrades']})==12
for filename,digest in x['provenance'].items():
    assert hashlib.sha256((R/filename).read_bytes()).hexdigest()==digest
for p in x['solutions']+x['upgrades']:
    v=p['pricing']
    if p['unpriced_requirements']:assert not v['complete_price']
    if v['amount_usd'] is not None:
        assert v['amount_usd']<=v['component_retail_sum_usd']
    if v['cost_usd'] is not None:
        assert abs(v['amount_usd']-v['cost_usd']-v['dealer_fee_usd']-v['contribution_usd'])<.011
annual={p['id']:p for p in m['products']}
for p in x['current_offer_prices']:
    s=annual[p['ref']]['snapshots']['1982']
    if p['ref'] not in {'device.artemis_professional_video_128kb','device.mono_pro_17'} and s.get('separate_purchase_price_usd') is not None:
        assert p['retail']<=s['separate_purchase_price_usd']
assert 'offer.ncc82_professional_graphics' not in {p['ref'] for p in x['current_offer_prices']}
assert next(p for p in x['current_offer_prices'] if p['ref']=='software.aion_development_team')['retail']==745.23
assert next(p for p in x['solutions'] if p['id']=='professional_cad')['pricing']['cost_usd'] is None
assert next(p for p in x['solutions'] if p['id']=='office_essentials')['pricing']['amount_usd']==1961.08
assert annual['bundle.proposed_aurelia_plus_office']['snapshots']['1982']['retail_price_usd']==1969.15
print('PASS: references, provenance, current ceilings, original history, supplier unknowns and quotation gates.')

assert set(x['snapshots'])=={f'{y}-06-15' for y in range(1978,1983)}
for date,view in x['snapshots'].items():
    year=date[:4]
    for row in view['current_offer_prices']:
        product=annual[row['ref']]
        assert product['offering_start']<=date
        assert not product.get('announced_only')
        assert row['date']==date
        assert row['retail']==product['snapshots'][year]['retail_price_usd']
    for card in view['solutions']+view['upgrades']:
        for variant in [card]+card['variants']:
            ref=variant['components'][0]['ref']
            assert variant['pricing']['amount_usd']==annual[ref]['snapshots'][year]['retail_price_usd']
            assert variant['pricing']['lines'][0]['date']==date
    assert not any(p['id']=='professional_cad' for p in view['solutions'])
assert next(p for p in x['snapshots']['1982-06-15']['upgrades'] if p['id']=='professional_drawing')['pricing']['amount_usd']==1496.62
for year in ['1978','1979','1980','1981']:
    assert not any(p['id'] in ['mouse_starter','professional_drawing','colour_reports'] for p in x['snapshots'][year+'-06-15']['upgrades'])
assert not any('Abacus 3' in item for p in x['snapshots']['1980-06-15']['solutions'] for item in p['includes'])
assert any('Abacus 3' in item for p in x['snapshots']['1981-06-15']['solutions'] for item in p['includes'])
print('PASS: five dated views, exact historical prices, introduction gates and June/November separation.')
