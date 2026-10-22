from data_paths import resolve_path
"""Cross-model gates for the 1980–82 reassessment; do not merely test rendering."""
import json,math,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/n).read_text())
s=read('generated/models/sales-forecast.json');i=read('generated/models/industrial-investment-1974-1981.json');roi=read('generated/models/roi-1974-1980.json');m=read('generated/models/market-outlook-1980-1982.json')
central=next(x for x in s['scenarios'] if x['id']=='central');cash=next(x for x in roi['scenarios'] if x['id']=='central')
assert len(central['monthly'])==60 and len(central['quarterly'])==20
assert cash['quarterly'][-1]['quarter']=='1982-Q4'
assert s['policy']['capacity_headroom']==.05
for row in central['monthly']:
 month=row['month']
 if not row['computer_units']:continue
 assert row['products']=={f:i['monthly_demand'][month]['products'].get(f,0) for f in row['products']}
 assert row['computer_units']==sum(row['products'].values())
 if month<'1981-07':assert row['products'].get('artemis_pro',0)==0
 if month<'1981-11':assert row['team_licenses']==0
 costed=sum(x['units'] for x in i['product_cost_links'] if x['month']==month and x['product_ref']=='software.aion_development_team')
 assert costed==row['team_licenses']
 for x in i['product_cost_links']:
  if x['month']==month and x['product_ref']=='software.aion_development_team':assert x['unit_cost_usd']>800
for row in central['quarterly']:
 q=row['quarter'];cap=next(x for x in i['quarterly_capacity'] if x['quarter']==q);f=next(x for x in cash['quarterly'] if x['quarter']==q)
 assert row['computer_units']==cap['customer_computers']==f['computer_units']
 assert row['computer_units']==sum(x['computer_units'] for x in central['monthly'] if x['month'][:4]+'-Q'+str((int(x['month'][5:])-1)//3+1)==q)
 idx=i['quarterly_capacity'].index(cap)
 peak=max(x['peak_month_customer_demand'] for x in i['quarterly_capacity'][idx:idx+3])
 assert cap['installed_computer_capacity_month']==math.ceil(peak*1.05)
for row in i['quarterly_component_requirements']:assert row['supplier_reserved_quantity']>=row['production_quantity']*1.05-.01
assert sum(x['gross_development_usd'] for x in i['team_development_reconciliation'])==1380000
assert sum(x['gross_campaign_usd'] for x in roi['team_campaign_reconciliation'])==276000
for x in i['team_development_reconciliation']:
 assert abs(x['gross_development_usd']-x['existing_payroll_allocated_usd']-x['incremental_development_usd'])<.01
 ledger=next(r for r in i['quarterly_entity_costs'] if r['quarter']==x['quarter'] and r['entity']=='AION Software')
 assert ledger['cost_type_usd']['team_incremental_development']==x['incremental_development_usd']
# 1982 process capital is paid even when equipment enters service in 1983.
assert sum(x['usd'] for x in i['capital_schedule'] if x['quarter'].startswith('1982') and x['cost_type']=='memory_process_equipment')==700000
assert all(a['service_quarter']=='1983-Q3' for a in roi['asset_depreciation_schedule'] if a['quarter'] in ['1982-Q3','1982-Q4'] and a['cost_type']=='memory_process_equipment')
assert i['memory_manufacturing']['development_line']['production_output_credited']==0
assert not any(x['path'].endswith('.md') for x in m['sources'])
for src in m['sources']:assert hashlib.sha256((R/resolve_path(src['path'])).read_bytes()).hexdigest()==src['sha256'],src['path']
assert not list(R.rglob('*.md'))
print('PASS: 36 months, quarterly sales/production/ROI matching, launch gates, 5% headroom, Team cost reconciliation, forward capital and provenance.')
