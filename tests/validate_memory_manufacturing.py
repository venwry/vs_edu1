"""Economic invariants and release gates for the RAM manufacturing revision."""
from pathlib import Path
import sys,json,hashlib,math
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from memory_manufacturing import policy,evaluate,selected
def read(n):return json.loads((R/n).read_text())
p=policy();c=read('manufacturing_costs.json');i=read('industrial_investment_1974_1981.json');impact=read('memory_manufacturing_impact.json');baseline=read('memory_manufacturing_baseline.json')
for r in p['memory_recipes']:
 v=evaluate(r)
 assert 0<v['raw_die_yield']<=v['die_yield']<=r['nonarea_yield']<=1
 assert evaluate(dict(r,repair_fraction_of_spatial_failures=0))['die_yield']==v['raw_die_yield']
for year,date in [(1981,'1981-06-15'),(1982,'1982-07-01'),(1983,'1983-10-01')]:
 r=selected(year,date);cost=lambda x:evaluate(x,p['wafer_cost_by_year'][str(year)][x['node_um']])['good_packaged_chip_cost_usd']
 assert r['available_from']<=date
 assert cost(r)==min(cost(x) for x in p['memory_recipes'] if x['available_from']<=date)
assert selected(1981)['node_um']=='3.0'
assert selected(1982,'1982-06-30')['node_um']!='2.0'
assert selected(1983,'1983-09-30')['node_um']!='1.5'
for y,v in c['chip_fabrication_models']['part.era1'].items():
 assert v['die_area_mm2']==55 and v['process_node_um']==3
assert c['chip_fabrication_models']['part.era1']['1981']['good_packaged_chip_cost_usd']==22.434
cp={x['id']:x for x in c['products']}
for ref,count in [('bundle.artemis_pro_512_server',64),('bundle.artemis_pro_1mb_server',128)]:
 parts={x['component_ref']:x['quantity'] for x in cp[ref]['snapshots']['1981']['bom_lines']}
 assert parts['bompart.part.aion_4164']==count
 assert 'bompart.part.dram_64kbit' not in parts
for row in i['quarterly_wafer_loading']:
 if row['chip_ref']=='part.aion_4164' and row['quarter']=='1980-Q1':assert row['cost_snapshot_year']==1979
for src in impact['sources']:assert hashlib.sha256((R/src['path']).read_bytes()).hexdigest()==src['sha256']
assert impact['investment']['included_process_capital_usd']==sum(x['usd'] for x in p['capital_schedule'] if x['quarter']<='1981-Q4')==2225000
assert impact['forward_budget_total_usd']==2880000
assert len(baseline['roi_central'])==32
roi=read('roi_1974_1980.json');central=next(x for x in roi['scenarios'] if x['id']=='central')
assert central['quarterly'][-1]['quarter']=='1981-Q4'
assert math.isclose(impact['cash_after_reserving_forward_budgets_usd'],central['quarterly'][-1]['cumulative_net_cash_usd']-2880000,abs_tol=.01)
assert any(x['month']=='1981-07' and x['stream']=='bpi_licenses' for x in roi['monthly_revenue_links'])
assert i['memory_manufacturing']['development_line']['production_output_credited']==0
print('PASS: RAM release gates, repair bounds, least-cost selection, frozen ERA1, PRO population, investment boundaries and report source hashes')
