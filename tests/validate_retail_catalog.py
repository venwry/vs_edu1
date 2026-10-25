from data_paths import read_document, document_bytes, document_text
from data_paths import resolve_path
"""Validate the effective catalogue, price ceilings and incomplete-package labels."""
import hashlib
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
x=read_document('generated/models/retail-catalog-1982-results.json', root=R)
m=read_document('generated/models/pricing-results.json', root=R)
assert len(x['solutions'])==9 and len(x['upgrades'])==5
assert x['effective_from']=='1982-11-29'
assert len({p['id'] for p in x['solutions']+x['upgrades']})==14
for filename,digest in x['provenance'].items():
    assert hashlib.sha256(document_bytes(resolve_path(filename), root=R)).hexdigest()==digest
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
assert 'product.ncc82_professional_graphics' not in {p['ref'] for p in x['current_offer_prices']}
assert next(p for p in x['current_offer_prices'] if p['ref']=='software.aion_development_team')['retail']==745.23
assert next(p for p in x['solutions'] if p['id']=='professional_cad')['pricing']['cost_usd'] is None
assert next(p for p in x['solutions'] if p['id']=='office_essentials')['pricing']['amount_usd']==1961.08
assert annual['product.proposed_aurelia_plus_office']['snapshots']['1982']['retail_price_usd']==1969.15
print('PASS: references, provenance, current ceilings, original history, supplier unknowns and quotation gates.')

assert set(x['snapshots'])=={f'{y}-{month}-15' for y in range(1978,1983) for month in ['06','12']}
for date,view in x['snapshots'].items():
    if '-12-' in date: continue
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

for date,view in x['snapshots'].items():
    if '-12-' not in date:continue
    for row in view['current_offer_prices']:
        if row['ref'] in annual:assert annual[row['ref']]['offering_start']<=date
        if row['date']>date:assert 'proxy' in row['basis'].lower()
    if date<'1982-12-15':assert not any(p['id']=='professional_cad' for p in view['solutions'])
d79=x['snapshots']['1979-12-15']
assert next(p for p in d79['solutions'] if p['id']=='office_essentials')['components'][0]['ref']=='product.proposed_aurelia_plus_office'
assert any(p['ref']=='software.abacus_2' for p in d79['current_offer_prices'])
assert not any(p['ref']=='software.abacus_3' for p in d79['current_offer_prices'])
d80=x['snapshots']['1980-12-15']
assert any('Abacus 3' in item for p in d80['solutions'] for item in p['includes'])
assert next(p for p in x['snapshots']['1981-12-15']['solutions'] if p['id']=='development_team')['pricing']['amount_usd']==745.23
d82=x['snapshots']['1982-12-15']
assert next(p for p in d82['solutions'] if p['id']=='professional_cad')['pricing']['amount_usd']==9909.72
assert next(p for p in d82['upgrades'] if p['id']=='professional_drawing')['pricing']['amount_usd']==1604.8
assert any(p['ref']=='software.autocad_1_artemis' for p in d82['current_offer_prices'])
print('PASS: December COMDEX availability, assessment provenance, Team launch and November CAD prices.')
