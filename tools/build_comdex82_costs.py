from data_store import read_document, document_bytes, document_text
"""Append dated November revision costs and prices; preserve annual June snapshots."""
from pathlib import Path
import json,copy,math,runpy,hashlib
from decimal import Decimal,ROUND_HALF_UP
R=Path(__file__).resolve().parents[1]
load=lambda n:read_document(n, root=R)
def save(n,x):(R/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def cents(x):return float(Decimal(str(x)).quantize(Decimal('.01'),rounding=ROUND_HALF_UP))
# Load the common engine; its deterministic output remains the annual baseline.
g=runpy.run_path(str(R/'tools/build_cost_assessment.py'))
costs=load('generated/models/manufacturing-costs.json'); prices=load('generated/models/pricing-results.json'); policy=load('generated/catalogs/comdex-1982-cost-inputs.json');i=4
base_rows={x['id']:x for x in costs['products']}; inputcopy=copy.deepcopy(g['inputs'])
# November silicon allowance, no assumed shrink or unqualified July RAM substitution.
ref='part.professional_graphics_controller';g['chip_area'][ref]=policy['graphics_controller_die_area_mm2']
chip=g['chip_cost'](ref,i);inputcopy[ref]['annual_cost_buckets_usd']['1982']={k:round(v,5) for k,v in chip.items() if v}
for ref,amount in policy['monitor_component_overrides_usd'].items():
 inputcopy[ref]['annual_cost_buckets_usd']['1982']={'bom_materials':amount}
original_routing=g['routing']
def routing(a):
 if a=='assembly.device.artemis_professional_video_128kb.comdex82':return (1.5,2.2,1.75)
 if a=='assembly.device.mono_pro_17.comdex82':return (2.5,9,3)
 return original_routing(a)
g['rollup'].__globals__['routing']=routing
for a in ['assembly.device.artemis_professional_video_128kb.comdex82','assembly.device.mono_pro_17.comdex82']:
 # Prevent prelaunch learning discount on newly qualified revision routing.
 g['ncc']['routing'][a]={'hours':routing(a)[0],'kwh':routing(a)[1],'consumables_usd':routing(a)[2]}
rows=[]
def row(id,name,v,lines=None,assumptions=None):
 bd={k:cents(v.get(k,0)) for k in g['K']};cost=cents(sum(bd.values()));entry={'id':id,'name':name,'date':'1982-11-29','cost_usd':cost,'low_usd':cents(cost*.7),'high_usd':cents(cost*1.6),'breakdown_usd':bd,'bom_lines':lines or [],'assumptions':assumptions or [],'status':'unquoted_engineering_planning_estimate'};rows.append(entry);return entry
def device(ref):
 r=copy.deepcopy(base_rows[ref]);r['assembly_ref']='assembly.'+ref+'.comdex82'
 v,flat,a=g['estimate'](r,i,inputcopy)
 return row(ref,r['name']+' — November revision',v,[{'component_ref':k,'quantity':q,'unit_cost_usd':sum(inputcopy[k]['annual_cost_buckets_usd']['1982'].values()),'extended_cost_usd':cents(q*sum(inputcopy[k]['annual_cost_buckets_usd']['1982'].values()))} for k,q in flat.items()],['Dated November revision; June row is unchanged.','Existing June nominal labor, energy and qualified RAM costs carried forward explicitly; no unsupported November cost decline.'])
card=device('device.artemis_professional_video_128kb');monitor=device('device.mono_pro_17')
# Complete reference hardware: remove included old card at factory assembly cost, install new colour card once.
base=base_rows['bundle.artemis_pro_1mb_server']['snapshots']['1982'];v=copy.deepcopy(base['breakdown_usd'])
oldcard,_=g['rollup']('device.artemis_video_card',i)
newcard,_=g['rollup']('device.artemis_video_card_64kb',i)
for k in g['K']:v[k]+=newcard[k]-oldcard[k]
for ref in ['device.flexibus_keyboard','device.color_pro_14','device.logix_mouse']:
 for k,value in base_rows[ref]['snapshots']['1982']['breakdown_usd'].items():v[k]+=value
for r in [card,monitor]:
 for k,value in r['breakdown_usd'].items():v[k]+=value
full=row('offer.comdex82_reference_hardware','Artemis PRO 1 MiB dual-display reference hardware',v,assumptions=['Base 1 MiB/5 MB server includes OS and one primary card; replace its 32 KiB card with 64 KiB at assembly cost, not a second retail card.','One keyboard, Color Pro 14, November professional card, Mono Pro 17 and mouse. Accessories delivered in their costed separate cartons; no extra complete-system packout charged.','5 MB is a bounded reference configuration, not a guarantee for all workloads. Larger storage, plotter, installation and training quoted separately.','Server shipment and complete CAD configuration acceptance remain qualification gates.'])
rowby={x['id']:x for x in rows}
v={k:card['breakdown_usd'][k]+monitor['breakdown_usd'][k]+base_rows['device.logix_mouse']['snapshots']['1982']['breakdown_usd'][k] for k in g['K']}
upgrade=row('offer.comdex82_professional_hardware','November professional graphics upgrade with mouse',v,assumptions=['Existing qualified host/primary display required; omit mouse at component price when already owned.'])
priced=[]
for r in rows:
 p=cents(r['cost_usd']/((1-.25)*.75));fee=cents(p*.25);net=cents(p-fee);profit=cents(net-r['cost_usd'])
 priced.append({'id':r['id'],'name':r['name'],'date':r['date'],'retail_price_usd':p,'manufacturing_cost_usd':r['cost_usd'],'dealer_fee_rate':.25,'dealer_fee_usd':fee,'net_revenue_usd':net,'unit_contribution_usd':profit,'margin_pct':cents(100*profit/net),'pricing_status':'no_proxy_cost_based','basis':'No verified equivalent comparator: existing 25% net-contribution fallback. Retail is a planning estimate, not a supplier quote.','cost_low_usd':r['low_usd'],'cost_high_usd':r['high_usd']})
software={'id':'software.autocad_1_artemis','name':'Autodesk AutoCAD 1.0 — Artemis licence','date':'1982-11-29','retail_price_usd':1000,'manufacturing_cost_usd':None,'dealer_fee_rate':None,'dealer_fee_usd':None,'net_revenue_usd':None,'unit_contribution_usd':None,'margin_pct':None,'pricing_status':'independent_vendor_historical_price_anchor','basis':'Original AutoCAD 1.0 US list price $1000, reused as a provisional alternate-history Artemis licence price. Autodesk costs, reseller terms and royalties unknown; no Logix software margin inferred.','source':policy['autocad_price_source']};priced.append(software)
by={x['id']:x for x in priced}
for id,hw,name in [('offer.comdex82_artemis_autocad','offer.comdex82_reference_hardware','Artemis PRO Professional CAD — hardware and AutoCAD'),('offer.comdex82_upgrade_autocad','offer.comdex82_professional_hardware','Professional graphics upgrade and AutoCAD')]:
 priced.append({'id':id,'name':name,'date':'1982-11-29','retail_price_usd':cents(by[hw]['retail_price_usd']+1000),'manufacturing_cost_usd':None,'dealer_fee_rate':None,'dealer_fee_usd':None,'net_revenue_usd':None,'unit_contribution_usd':None,'margin_pct':None,'pricing_status':'mixed_supplier_component_sum','components':[hw,'software.autocad_1_artemis'],'known_logix_hardware_cost_usd':by[hw]['manufacturing_cost_usd'],'known_logix_hardware_contribution_usd':by[hw]['unit_contribution_usd'],'basis':'Sum of hardware and separately owned Autodesk licence. Total manufacturing cost/contribution unknown; never treat the $1000 licence as free-cost Logix revenue.'})
assessment={'date':'1982-11-29','inputs_file':'generated/catalogs/comdex-1982-cost-inputs.json','inputs_sha256':hashlib.sha256(document_bytes('generated/catalogs/comdex-1982-cost-inputs.json', root=R)).hexdigest(),'basis':policy['basis'],'controller_model':copy.deepcopy(g['chip_models']['part.professional_graphics_controller']['1982']),'products':rows}
costs['dated_assessments']=[assessment];costs['metadata']['source_sha256']['generated/catalogs/comdex-1982-cost-inputs.json']=assessment['inputs_sha256']
prices['dated_assessments']=[{'date':'1982-11-29','basis':policy['basis'],'products':priced}]
review={'date':'1982-11-29','cost_assessment':assessment,'prices':priced,'financial_boundary':'Unit estimates only; June snapshots and Team adoption price retained. No sales-volume, ROI or investment update inferred.'}
costs.setdefault('reviews',{})['comdex-1982']=review;save('generated/models/manufacturing-costs.json',costs)
prices['metadata']['cost_model_sha256']=hashlib.sha256(document_bytes('generated/models/manufacturing-costs.json', root=R)).hexdigest();save('generated/models/pricing-results.json',prices)
# Pricing and Navigator render the generated models; the retired report is not emitted.
print('Updated November costs and retail prices:',[(x['id'],x['retail_price_usd']) for x in priced])
