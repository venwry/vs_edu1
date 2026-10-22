"""Aurelia+ sourcing, shared programme, and demand-driven fab capacity."""
import json,math
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(f):return json.loads((R/f).read_text())
c=load('generated/catalogs/logix-aion-technical-catalog-v2.json');b=load('generated/catalogs/hardware-bom.json')
r={x['id']:x for a in c.values() if isinstance(a,list) for x in a if isinstance(x,dict) and 'id'in x}
h=r['computer.aurelia_plus'];p=h['memory']['physical_population']
assert p['chip_ref']=='part.aion_4164' and p['data_chip_count']==8 and p['data_ram_kb']==64
assert r['part.aion_4164']['introduced']['event_start_date']=='1979-12-03'
assert 'computer.aurelia_plus' not in r['part.dram_64kbit']['used_in']
a=next(x for x in b['assemblies'] if x['id']=='assembly.computer.aurelia_plus.base')
lines={l['ref']:l['quantity'] for l in a['lines']}
assert lines['bompart.part.aion_4164']==8 and 'bompart.part.dram_64kbit' not in lines
assert lines['bompart.part.aion_4116']==8 and lines['bompart.part.aion_2114']==2
m=load('generated/models/manufacturing-costs.json')['chip_fabrication_models']['part.aion_4164']
assert abs(m['1980']['good_packaged_chip_cost_usd']*8-115.2448)<.01
assert abs(m['1981']['good_packaged_chip_cost_usd']*8-91.8992)<.01
iv=load('generated/models/industrial-investment-1974-1981.json')
prog=[p for p in iv['engineering_programs'] if p['id']=='aion_64k_dram']
assert len(prog)==1 and prog[0]['person_months']==120 and prog[0]['end']=='1979-Q3'
assert any(x['quarter']=='1979-Q4' and x['chip_ref']=='part.aion_4164' and x['good_chips']>0 for x in iv['quarterly_wafer_loading'])
for stage in iv['fab_stages']:
 for t in stage['tools']:
  target=stage['packaging_input_per_month'] if t['id'] in ['dice','bond','package','test'] else stage['wafer_starts_per_month']
  assert t['effective_monthly_capacity_one_down']>=target,(stage['id'],t['id'],target)
for q in iv['quarterly_capacity']:
 assert q['installed_computer_capacity_month']>=math.ceil(q['peak_month_customer_demand']*1.05)
print('PASS: Aurelia+ AION RAM, dated chip costs, earlier shared qualification, 1979 fab loading and redundant tool/reserve capacity.')

