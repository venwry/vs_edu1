from data_paths import read_document, document_bytes, document_text
"""Validate the launch, cost cutoff, pricing policy and explicitly frozen financial outputs."""
import json,hashlib,math,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from memory_manufacturing import selected,evaluate,policy
load=lambda n:read_document(n, root=R)
program=load('generated/catalogs/team-development-program.json'); costs=load('generated/models/manufacturing-costs.json');pricing=load('generated/models/pricing-results.json');review=load('generated/models/manufacturing-review-1982.json');catalog=load('generated/catalogs/logix-aion-technical-catalog-v2.json')
assert program['status'].startswith('Integrated')
assert sum(r['usd'] for r in program['campaign_costs'])==program['totals']['campaign_provision_usd']==276000
assert sum(r['usd'] for r in program['pending_investment_costs'])==program['totals']['development_provision_usd']==1380000
assert program['totals']['gross_pending_provision_usd']==1656000
assert program['financial_integration']['development_treatment']=='Gross budget less allocated existing payroll; remainder expensed in industrial ledger.'
assert review['selected_recipe']==selected(1982)['id']=='dram64_3um_repair'
assert not next(r for r in review['candidates'] if r['node_um']=='2.0')['eligible']
assert all(r['process_node_um']==3 for r in costs['chip_fabrication_models']['part.era1'].values())
assert math.isclose(costs['chip_fabrication_models']['part.aion_4164']['1982']['good_packaged_chip_cost_usd'],next(r for r in review['candidates'] if r['selected'])['good_packaged_chip_cost_usd'],abs_tol=.0001)
rows={r['id']:r for r in pricing['products']};team=rows['software.aion_development_team'];s=team['snapshots']['1982']
assert team['offering_start']=='1981-11-19'
assert all(team['snapshots'][str(y)]['retail_price_usd'] is None for y in range(1978,1982))
assert s['pricing_balance']['status']=='adoption_subsidy_50_percent'
assert s['competitor']['normalized_price_usd'] is None
assert s['retail_price_usd']==745.23
assert s['unit_profit_usd']==-279.46
assert team['launch_snapshot']['retail_price_usd']==745.23
assert program['delivery']['onboarding_staff_hours']==20 and program['delivery']['first_year_support_staff_hours']==12
assert s['manufacturing_cost_usd']>800 # Includes 32 staff-hours; not just duplicated disks.
for r in pricing['products']:
 x=r['snapshots']['1982']
 if x.get('competitor',{}).get('normalized_price_usd'):assert x['competitor']['assessment_type']=='unverified_proxy'
p=next(r for r in catalog['software_products'] if r['id']==team['id'])
assert len(p['edition_refs'])==3
story=load('generated/catalogs/logix-aion-story.json');events={e['id']:e for phase in story['phases'] for e in phase['events']}
for e in ['team_pilots','team_dealer_training','team_launch','team_followup','cost_review_1982']:assert 'event.'+e in events
assert events['event.cost_review_1982']['date']['start']=='1982-06-15'
print('PASS: Team Edition, staged budgets, dated RAM selection, 1982 pricing and frozen financial outputs.')

