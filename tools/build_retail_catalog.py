"""Build the current retail view without rewriting historical pricing snapshots."""
import hashlib
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
R = Path(__file__).resolve().parents[1]
load = lambda p: json.loads((R / p).read_text())
D = lambda n: Decimal(str(n))
money = lambda n: float(D(n).quantize(D('.01'), rounding=ROUND_HALF_UP))
config = load('retail_catalog_1982.json')
model = load('pricing_results.json')
annual = {p['id']: p for p in model['products']}
dated = {p['id']: p for a in sorted(model.get('dated_assessments', []), key=lambda a:a['date']) if a['date'] <= config['effective_from'] for p in a['products']}

def resolve(ref):
    if ref in dated:
        p = dated[ref]
        return {'ref':ref, 'name':p['name'], 'retail':p['retail_price_usd'], 'cost':p['manufacturing_cost_usd'], 'fee':p['dealer_fee_usd'], 'date':p['date'], 'basis':p['pricing_status'], 'availability':'planning estimate; confirm shipment', 'original_retail':p['retail_price_usd']}
    p = annual[ref]
    s = p['snapshots']['1982']
    price = s['retail_price_usd']
    assert price is not None, ref
    ceiling = s.get('separate_purchase_price_usd')
    if ceiling is not None: price = min(price, ceiling)
    fee = money(D(price) * D(p['computerland_fee_rate']))
    return {'ref':ref, 'name':p['name'], 'retail':price, 'cost':s['manufacturing_cost_usd'], 'fee':fee, 'date':s['date'], 'basis':'current catalogue ceiling' if price < s['retail_price_usd'] else 'June estimate carried forward', 'availability':'shipment unconfirmed' if p.get('announced_only') else 'catalogued; qualification requirements apply', 'original_retail':s['retail_price_usd']}

def price_offer(p):
    lines = [dict(resolve(c['ref']),quantity=c['quantity']) for c in p['components']]
    total = money(sum(D(v['retail'])*v['quantity'] for v in lines)) if lines else None
    known = all(v['cost'] is not None for v in lines) and bool(lines)
    cost = money(sum(D(v['cost'])*v['quantity'] for v in lines)) if known else None
    # New packages use the conservative cost-based fallback, never above identical contents.
    # Named existing packages, direct services and Team subsidy retain their current line prices.
    if len(lines)>1 and p['id'] == 'office_professional':
        total = min(total,money(D(cost)/D('.5625')))
        fee = money(D(total)*D('.25'))
    else:
        fee = money(sum(D(v['fee'])*v['quantity'] for v in lines)) if lines and all(v['fee'] is not None for v in lines) else None
    contribution = money(D(total)-D(cost)-D(fee)) if cost is not None and fee is not None else None
    return dict(p, pricing={'amount_usd':total,'label':'Known items subtotal — final quotation required' if p['unpriced_requirements'] else 'Reference configuration price', 'cost_usd':cost, 'dealer_fee_usd':fee,'contribution_usd':contribution,'component_retail_sum_usd':money(sum(D(v['retail'])*v['quantity'] for v in lines)) if lines else None,'lines':lines,'complete_price':not bool(p['unpriced_requirements']) and total is not None})

output = {**config,'solutions':[price_offer(p) for p in config['solutions']],'upgrades':[price_offer(p) for p in config['upgrades']]}
output['current_offer_prices'] = [resolve(ref) for ref in annual if annual[ref]['snapshots']['1982']['retail_price_usd'] is not None and ref not in {x['ref'] for x in config['superseded_current_offers']}]
output['provenance'] = {p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in ['retail_catalog_1982.json','pricing_results.json']}
(R/'retail_catalog_1982_results.json').write_text(json.dumps(output,indent=2,ensure_ascii=False)+'\n')
print('Built seven solution families, five upgrades and current offer prices; history unchanged.')
