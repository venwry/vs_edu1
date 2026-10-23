from data_paths import read_document, document_bytes, document_text
"""Check dated November economics and removal of retired report pages."""
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
review = read_document('generated/models/manufacturing-costs.json', root=ROOT)['reviews']['comdex-1982']
rows = {p['id']: p for p in review['prices']}
money = lambda n: Decimal(str(n)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
assert review['date'] == '1982-11-29'
for row in rows.values():
    if row['pricing_status'] == 'no_proxy_cost_based':
        retail = money(row['retail_price_usd'])
        cost = money(row['manufacturing_cost_usd'])
        assert abs(retail - money(cost / Decimal('.5625'))) <= Decimal('.01')
        assert money(row['dealer_fee_usd']) == money(retail * Decimal('.25'))
        assert money(row['unit_contribution_usd']) == retail - money(row['dealer_fee_usd']) - cost
    elif row['pricing_status'] == 'mixed_supplier_component_sum':
        assert money(row['retail_price_usd']) == sum(money(rows[k]['retail_price_usd']) for k in row['components'])
        assert row['manufacturing_cost_usd'] is None
        assert row['unit_contribution_usd'] is None
assert rows['software.autocad_1_artemis']['manufacturing_cost_usd'] is None
card = next(p for p in review['cost_assessment']['products'] if p['id'] == 'device.artemis_professional_video_128kb')
assert next(p for p in card['bom_lines'] if p['component_ref'] == 'bompart.part.aion_2114')['quantity'] == 2
for filename in ('market-outlook.html', 'memory-manufacturing.html'):
    assert not (ROOT / filename).exists()
    for path in [ROOT / 'data/site.json', *ROOT.glob('*.html'), *ROOT.glob('*.js'), *ROOT.glob('tools/*template.html')]:
        assert filename not in path.read_text(), (path, filename)
print('PASS: November pricing arithmetic, independent Autodesk costs, sprite RAM and retired-page links.')
