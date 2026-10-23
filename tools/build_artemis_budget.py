from data_store import read_document, document_bytes, document_text
"""Reproducible budget-system overlay. Run after base costs/pricing, before retail and sales.
Frozen component estimates in generated/catalogs/artemis-budget-inputs.json avoid recursive repricing.
"""
import json,math,hashlib
from copy import deepcopy
from pathlib import Path
R=Path(__file__).resolve().parents[1]
load=lambda n:read_document(n, root=R)
def save(n,x):(R/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
I=load('generated/catalogs/artemis-budget-inputs.json');M=load('generated/models/manufacturing-costs.json');P=load('generated/models/pricing-results.json')
refs=['bundle.artemis_budget_128','bundle.artemis_budget_128_hdd']
M['products']=[p for p in M['products'] if p['id'] not in refs];P['products']=[p for p in P['products'] if p['id'] not in refs]
def assess(date,disk):
 y=date[:4];source=str(max(int(y),1980));b=deepcopy(I['base_cost_snapshots'][source]['breakdown_usd'])
 base=I['base_cost_snapshots'][source]
 factor=1
 b={k:round(v*factor,2) for k,v in b.items()}
 components=[{'cost_ref':'bundle.artemis_128_color','quantity':1,'extended_cost_usd':round(base['total_usd']*factor,2),'basis':'Dated 128 KiB Color II base; NIC included from May 1981'}]
 for ref in ['software.business_tools_artemis']+(['software.abacus_3'] if date>='1980-11-19' else []):
  ss=I['software_cost_snapshots'][ref];s=ss[source] if ss[source].get('total_usd') is not None else ss['1981']
  for k,v in s['breakdown_usd'].items():b[k]=round(b[k]+v*factor,2)
  components.append({'cost_ref':ref,'quantity':1,'extended_cost_usd':round(s['total_usd']*factor,2)})
 if disk:
  for k,v in I['hdd_subsystem_additions_usd'][y].items():b[k]=round(b[k]+v,2)
  components.append({'cost_ref':'allowance.artemis_budget_5mb_subsystem','quantity':1,'extended_cost_usd':sum(I['hdd_subsystem_additions_usd'][y].values())})
 cost=round(sum(b.values()),2);cmp=I['pricing']['comparator_1982_hdd_usd' if disk else 'comparator_1982_floppy_usd'] if y=='1982' else None
 price=round(math.sqrt(cost*cmp/.75) if cmp else cost/.5625,2);fee=round(price*.25,2);net=round(price-fee,2);profit=round(net-cost,2)
 return {'date':date,'status':'available_proposal','retail_price_usd':price,'manufacturing_cost_usd':cost,'cost_low_usd':round(cost*.8,2),'cost_high_usd':round(cost*1.3,2),'cost_breakdown_usd':b,'cost_components':components,'computerland_fee_rate':.25,'computerland_fee_usd':fee,'revenue_after_fee_usd':net,'unit_profit_usd':profit,'contribution_margin_on_net_revenue_pct':round(profit/net*100,2),'separate_purchase_price_usd':None,'price_floor_usd':round(cost/.75,2),'competitor':{'normalized_price_usd':cmp,'discount_pct':round((1-price/cmp)*100,2) if cmp else None,'assessment_type':'scenario_hardware_price_anchor' if cmp else 'cost_based_fallback','assessment':'IBM reference configuration only in 1982; substitute OS/software qualification required. No anachronistic IBM competitor before 1982.'},'pricing_balance':{'status':'balanced_scenario_comparator' if cmp else 'fallback','margin_pct':round(profit/net*100,2),'discount_pct':round((1-price/cmp)*100,2) if cmp else None},'warnings':['Engineering estimate, not a supplier quote or guaranteed margin.','128 KiB workloads require qualification; later application versions are not backdated.'],'cost_date_basis':'Dated cost overlay; HDD enclosure, integration and support included'}
report={'inputs':'generated/catalogs/artemis-budget-inputs.json','products':[]}
for disk,ref in zip([False,True],refs):
 name='Artemis 128 — Budget '+('Hard-Disk Office (5 MB)' if disk else 'Colour Office')
 snaps={str(y):assess(f'{y}-06-15',disk) if y>=1980 else {'date':f'{y}-06-15','status':'not_yet_available','retail_price_usd':None,'manufacturing_cost_usd':None} for y in range(1978,1983)}
 launch=assess('1980-05-19',disk)
 p={'id':ref,'name':name,'type':'Complete computer systems','offering_start':'1980-05-19','offering_end':None,'unit':'complete system, two floppies, 12-inch Color II, dated software and support','channel':'ComputerLand','computerland_fee_rate':.25,'status':'approved_scenario','notes':[I['software_timing']],'components':[{'cost_ref':ref,'quantity':1}],'snapshots':snaps,'launch_snapshot':launch,'announced_only':False}
 # Components must be self-contained for dated selection; detailed cost composition remains in report.
 detailed=deepcopy(p)
 for s in list(p['snapshots'].values())+[p['launch_snapshot']]:
  if s.get('retail_price_usd') is not None:s['cost_components']=[{'cost_ref':ref,'quantity':1,'unit_cost_usd':s['manufacturing_cost_usd'],'extended_cost_usd':s['manufacturing_cost_usd']}]
 p['dated_snapshots']=[assess('1980-11-19',disk)]
 p['dated_snapshots'][0]['cost_components']=[{'cost_ref':ref,'quantity':1,'extended_cost_usd':p['dated_snapshots'][0]['manufacturing_cost_usd']}]
 P['products'].append(p)
 ms={y:{'status':'offered_estimate' if s.get('retail_price_usd') is not None else 'not_yet_offered','total_usd':s.get('manufacturing_cost_usd'),'low_usd':s.get('cost_low_usd'),'high_usd':s.get('cost_high_usd'),'breakdown_usd':s.get('cost_breakdown_usd',{}),'bom_assembly_ref':'assembly.'+ref,'bom_lines':[{'component_ref':'budgetcost.'+l['cost_ref'],'quantity':l['quantity'],'extended_recurring_cost_usd':l['extended_cost_usd']} for l in detailed['snapshots'][y].get('cost_components',[])]} for y,s in snaps.items()}
 for row in detailed['snapshots'].values():
  for l in row.get('cost_components',[]):M['component_cost_assumptions']['budgetcost.'+l['cost_ref']]={'name':l['cost_ref'],'basis':'Complete subassembly/software allocation from generated/catalogs/artemis-budget-inputs.json; do not add again to total.'}
 M['products'].append({'id':ref,'catalog_ref':ref,'name':name,'group':'Bundles','unit':p['unit'],'available_from':'1980-05-19','assumptions':[I['basis'],I['hdd_basis']] if disk else [I['basis']],'snapshots':ms,'launch_assessment':launch})
 report['products'].append(detailed)
M['budget_inputs_sha256']=P['budget_inputs_sha256']=hashlib.sha256(document_bytes('generated/catalogs/artemis-budget-inputs.json', root=R)).hexdigest()
save('generated/models/artemis-budget-review.json',report);save('generated/models/manufacturing-costs.json',M);save('generated/models/pricing-results.json',P)
print([(p['id'],p['snapshots']['1982']['manufacturing_cost_usd'],p['snapshots']['1982']['retail_price_usd']) for p in P['products'] if p['id'] in refs])
