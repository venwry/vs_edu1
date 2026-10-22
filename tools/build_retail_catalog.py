"""Build current and ten dated retail views without rewriting historical pricing snapshots."""
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

def resolve(ref, year=None):
    if year is None and ref in dated:
        p = dated[ref]
        return {'ref':ref, 'name':p['name'], 'retail':p['retail_price_usd'], 'cost':p['manufacturing_cost_usd'], 'fee':p['dealer_fee_usd'], 'date':p['date'], 'basis':p['pricing_status'], 'availability':'planning estimate; confirm shipment', 'original_retail':p['retail_price_usd']}
    p = annual[ref]
    s = p['snapshots'][year or '1982']
    price = s['retail_price_usd']
    assert price is not None, ref
    ceiling = s.get('separate_purchase_price_usd')
    if year is None and ceiling is not None: price = min(price, ceiling)
    fee = money(D(price) * D(p['computerland_fee_rate']))
    return {'ref':ref, 'name':p['name'], 'retail':price, 'cost':s['manufacturing_cost_usd'], 'fee':fee, 'date':s['date'], 'basis':'current catalogue ceiling' if price < s['retail_price_usd'] else ('June estimate carried forward' if year is None else 'Recorded June 15 snapshot'), 'availability':'shipment unconfirmed' if p.get('announced_only') else 'catalogued; qualification requirements apply', 'original_retail':s['retail_price_usd']}

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
# Build historical purpose-oriented views from dated package definitions, not November contents.
# No later bundle ceiling, revision or software edition is backdated into these snapshots.
from copy import deepcopy
cost_names = {}
for product in model['products']:
    cost_names[product['id']] = product['name']

def available(ref, year):
    p = annual.get(ref)
    if not p: return False
    date = year + '-06-15'
    s = p['snapshots'].get(year, {})
    return bool(p['offering_start'] <= date and (not p.get('offering_end') or date <= p['offering_end'])
                and s.get('retail_price_usd') is not None
                and s.get('status') == 'available_proposal' and not p.get('announced_only'))

def historical_offer(template, ref, year):
    p = annual[ref]
    snap = p['snapshots'][year]
    line = dict(resolve(ref,year), quantity=1)
    result = deepcopy(template)
    result['components'] = [{'ref':ref,'quantity':1}]
    result['includes'] = [str(c['quantity'])+' × '+cost_names.get(c['cost_ref'],c['cost_ref']) for c in snap['cost_components']]
    result['unpriced_requirements'] = []
    result['options'] = []
    result['purpose'] = 'Dated configuration: '+p['name']+'.'
    result['pricing'] = {'amount_usd':snap['retail_price_usd'], 'label':'June 15 reference configuration price',
      'cost_usd':snap['manufacturing_cost_usd'], 'dealer_fee_usd':snap['computerland_fee_usd'],
      'contribution_usd':snap['unit_profit_usd'], 'component_retail_sum_usd':snap.get('separate_purchase_price_usd'),
      'lines':[line], 'complete_price':True}
    result['scope_note'] = 'Price covers this dated package only. Optional installation, training, backup supplies and output equipment are additional unless explicitly included.'
    return result

families = {
 'budget_colour':['bundle.artemis_budget_128'],
 'budget_hdd':['bundle.artemis_budget_128_hdd'],
 'office_essentials':['bundle.proposed_aurelia_plus_office','bundle.proposed_aurelia_office'],
 'office_professional':['bundle.proposed_artemis_office','bundle.proposed_artemis_office_color','bundle.proposed_artemis_analysis','bundle.proposed_aurelia_plus_analysis'],
 'business_accounts':['bundle.proposed_artemis_accounts','bundle.proposed_aurelia_plus_accounts','bundle.proposed_aurelia_accounts'],
 'developer_workstation':['bundle.proposed_artemis_developer','bundle.proposed_artemis_developer_color','bundle.proposed_aurelia_plus_developer','bundle.proposed_aurelia_developer'],
 'connected_office':['bundle.proposed_artemis_pro_small_office'],
}
upgrade_refs = {
 'colour_reports':['offer.ncc82_colour_upgrade'],
 'professional_drawing':['offer.ncc82_professional_graphics'],
 'mouse_starter':['offer.ncc82_mouse_learning'],
 'connect_office':['bundle.artemis_network_upgrade','bundle.aurelia_network_upgrade'],
 'cpm_migration':['bundle.proposed_artemis_migration','bundle.proposed_artemis_migration_color'],
}
output['snapshots'] = {}
for year in map(str,range(1978,1983)):
    view = deepcopy(config)
    view['effective_from'] = year+'-06-15'
    view['historical_snapshot'] = True
    view['solutions'],view['upgrades'] = [],[]
    for field,mapping in [('solutions',families),('upgrades',upgrade_refs)]:
        for template in config[field]:
            refs = [ref for ref in mapping.get(template['id'],[]) if available(ref,year)]
            if not refs: continue
            card = historical_offer(template,refs[0],year)
            card['variants'] = [historical_offer(template,ref,year) for ref in refs[1:]]
            if template['id']=='cpm_migration':card['name']='Move from CP/M to Artemis — complete system'
            if template['id']=='connect_office':card['name']='Connect an existing workstation'
            view[field].append(card)
    view['current_offer_prices'] = [resolve(ref,year) for ref in annual if available(ref,year)]
    current_refs = {p['ref'] for p in view['current_offer_prices']}
    view['secondary_sections'] = []
    for group in config['secondary_sections']:
        group = deepcopy(group)
        group['refs'] = [ref for ref in group['refs'] if ref in current_refs]
        if not group['refs']: continue
        if group['id']=='value_legacy':
            group['name']='Other system configurations'
            group['description']='Systems offered at the selected date; no later clearance or retirement policy is applied.'
        elif group['id']=='legacy_software':
            group['name']='Additional software and displays'
            group['description']='Editions and displays offered at the selected date, including earlier compatible versions.'
        else: group['description']='Available catalogue entries at the selected date; confirm compatibility for the selected system.'
        view['secondary_sections'].append(group)
    view['announced_offers'] = [p['name'] for p in model['products'] if p['offering_start'] <= view['effective_from'] and p['snapshots'][year].get('status')=='announced_shipping_unconfirmed']
    output['snapshots'][view['effective_from']] = view
# December views expose COMDEX releases. Price dates remain explicit: new releases
# without a launch assessment use the first matching later June assessment only
# as a retrospective planning proxy, never as a claimed December quotation.
def december_assessment(ref, date):
    p = annual[ref]
    if p['offering_start'] > date or (p.get('offering_end') and p['offering_end'] < date) or p.get('announced_only'):
        return None
    if ref.startswith('bundle.artemis_budget_128'):
        choices=[v for v in list(p['snapshots'].values())+[p['launch_snapshot']]+p.get('dated_snapshots',[]) if v.get('retail_price_usd') is not None and v['date']<=date]
        return max(choices,key=lambda v:v['date']), 'Dated budget-system assessment carried forward'
    launch = p.get('launch_snapshot')
    if launch and launch['date'] <= date:
        return launch, 'Launch price; '+launch.get('cost_date_basis','dated launch assessment')
    expected = {c['cost_ref']:c['quantity'] for c in p['components']}
    for variant in sorted(p.get('component_variants',[]),key=lambda v:v['effective_from']):
        if variant['effective_from'] <= date:
            for old,new in variant['replace'].items():
                if old in expected: expected[new]=expected.pop(old)
    candidates=[]
    for snap in p['snapshots'].values():
        if snap.get('retail_price_usd') is None or snap.get('status')!='available_proposal':continue
        actual={c['cost_ref']:c['quantity'] for c in snap['cost_components']}
        if actual != expected:continue
        if any(ref in annual and annual[ref]['offering_start'] > date for ref in actual):continue
        candidates.append(snap)
    prior=[snap for snap in candidates if snap['date']<=date]
    if prior:return max(prior,key=lambda v:v['date']), 'Earlier assessment carried forward; no December repricing assumed'
    if candidates:return min(candidates,key=lambda v:v['date']), 'Retrospective planning proxy from the first matching later assessment; December price not recorded'
    return None

def december_line(ref,date):
    assessment=december_assessment(ref,date)
    if not assessment:return None
    snap,basis=assessment
    return {'ref':ref,'name':annual[ref]['name'],'retail':snap['retail_price_usd'],'cost':snap['manufacturing_cost_usd'],
      'fee':snap['computerland_fee_usd'],'date':snap['date'],'basis':basis,'availability':'catalogued; qualification requirements apply',
      'original_retail':snap['retail_price_usd']}

def december_card(template,ref,date):
    snap,basis=december_assessment(ref,date)
    result=deepcopy(template)
    result.update(components=[{'ref':ref,'quantity':1}],includes=[str(c['quantity'])+' × '+cost_names.get(c['cost_ref'],c['cost_ref']) for c in snap['cost_components']],
      options=[],unpriced_requirements=[],purpose='Dated configuration: '+annual[ref]['name']+'.',variants=[])
    result['pricing']={'amount_usd':snap['retail_price_usd'],'label':'Reference price — '+basis,
      'cost_usd':snap['manufacturing_cost_usd'],'dealer_fee_usd':snap['computerland_fee_usd'],'contribution_usd':snap['unit_profit_usd'],
      'component_retail_sum_usd':snap.get('separate_purchase_price_usd'),'lines':[dict(december_line(ref,date),quantity=1)],'complete_price':True}
    result['scope_note']='Price covers the listed configuration only. Assessment date and any retrospective proxy are shown explicitly.'
    return result

for year in map(str,range(1978,1983)):
    date=year+'-12-15'
    if year=='1982':
        # Accepted November catalogue, including the jointly presented AutoCAD system.
        view=deepcopy({k:v for k,v in output.items() if k!='snapshots'})
        view['effective_from']=date
        view['historical_snapshot']=False
        view['solutions']=[p for p in view['solutions'] if p['id'] not in ['connected_office','development_team']]
        view['current_offer_prices']=[p for p in view['current_offer_prices'] if not annual[p['ref']].get('announced_only')]
        # Include independent Autodesk licensing in the dated software choices.
        view['current_offer_prices'].append(resolve('software.autocad_1_artemis'))
    else:
        view=deepcopy(output['snapshots'][year+'-06-15'])
        view['effective_from']=date
        view['solutions'],view['upgrades']=[],[]
        for field,mapping in [('solutions',families),('upgrades',upgrade_refs)]:
            for template in config[field]:
                refs=[ref for ref in mapping.get(template['id'],[]) if december_assessment(ref,date)]
                if not refs:continue
                card=december_card(template,refs[0],date)
                card['variants']=[december_card(template,ref,date) for ref in refs[1:]]
                if template['id']=='cpm_migration':card['name']='Move from CP/M to Artemis — complete system'
                if template['id']=='connect_office':card['name']='Connect an existing workstation'
                view[field].append(card)
        view['current_offer_prices']=[line for ref in annual if (line:=december_line(ref,date))]
    # Team software is available from COMDEX 1981; don't imply its server bundle has shipped.
    if year in ['1981','1982']:
        template=next(p for p in config['solutions'] if p['id']=='development_team')
        card=december_card(template,'software.aion_development_team',date)
        card.update(name='AION Development System — Team Edition',includes=['One server / four concurrent developers; hardware excluded','20 onboarding hours and 12 first-year support hours','C IDE, repository and collaboration tools'])
        view['solutions'].append(card)
    available_refs={p['ref'] for p in view['current_offer_prices']}
    view['secondary_sections']=[]
    for group in config['secondary_sections']:
        group=deepcopy(group)
        group['refs']=[ref for ref in group['refs'] if ref in available_refs]
        if not group['refs']:continue
        if year!='1982':
            group['name']={'value_legacy':'Other system configurations','legacy_software':'Additional software and displays'}.get(group['id'],group['name'])
            group['description']='Offerings introduced by the selected date; later retirement policies are not applied.'
        view['secondary_sections'].append(group)
    view['announced_offers']=[p['name'] for p in model['products'] if p['offering_start']<=date and p.get('announced_only')]
    view['price_date_notice']='December prices use dated launch or November assessments when present, otherwise an explicitly labelled carry-forward or retrospective planning proxy. No new December cost survey is implied.'
    output['snapshots'][date]=view
# Show actual dated budget contents rather than an opaque self-reference.
for date,view in output['snapshots'].items():
 for card in view['solutions']:
  if card['id'] in ['budget_colour','budget_hdd']:
   card['includes']=['Artemis 128 KiB, two floppies, Color II 12-inch 640×200 display and keyboard','AIONix, Business Tools and one-year Regular Support']
   if date>='1980-11-19':card['includes'].append('Abacus 3; bounded 128 KiB workloads')
   if date>='1981-05-04':card['includes'].append('Standard network interface')
   if card['id']=='budget_hdd':card['includes'].append('5 MB qualified hard-disk subsystem with enclosure, power and interface')
output['snapshots']=dict(sorted(output['snapshots'].items()))
output['provenance'] = {p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in ['retail_catalog_1982.json','pricing_results.json']}
(R/'retail_catalog_1982_results.json').write_text(json.dumps(output,indent=2,ensure_ascii=False)+'\n')
print('Built current catalogue and June 15 and December 15 views for 1978–1982; historical prices unchanged.')
