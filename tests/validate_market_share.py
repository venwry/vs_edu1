import json
from pathlib import Path
R=Path(__file__).resolve().parents[1];read=lambda n:json.loads((R/n).read_text());m=read('quarterly_market_share.json');sales=read('sales_forecast.json');eco=read('ecosystem_forecast.json')
for s in m['scenarios']:
 assert len(s['quarterly'])==12
 forecasts=next(x for x in sales['scenarios'] if x['id']==s['id']);contracts=next(x for x in sales['contract_scenarios'] if x['id']==s['id'])['quarterly']
 for r in s['quarterly']:
  assert sum(v['units'] for v in r['manufacturers'].values())==r['total_market_units']
  assert abs(sum(v['share_pct'] for v in r['manufacturers'].values())-100)<1e-9
  assert all(v['units']>=0 for v in r['manufacturers'].values())
  assert r['manufacturers']['logix']['units']==next(q['computer_units'] for q in forecasts['quarterly'] if q['quarter']==r['quarter'])
  assert r['platform_units']==r['total_market_units']-r['manufacturers']['other_manufacturers']['units']
  assert r['aion_tech_uk_subset']<=r['manufacturers']['logix']['units']
  eq=next(q for q in next(c for c in eco['scenarios'] if c['id']==s['id'])['quarterly'] if q['quarter']==r['quarter'])
  assert sum(eq['logix_new_units'].values())==r['manufacturers']['logix']['units']
  for c in [c for c in contracts if c['quarter']==r['quarter']]:
   assert c['computer_units']==r['manufacturers'][c['manufacturer_id']]['units']
   assert len([o for o in eq['external_oems'] if o['manufacturer']==c['manufacturer']])==1
  if r['quarter']<'1982-Q1':assert r['platform_units']==r['manufacturers']['logix']['units']
assert 'market-share' in read('site_pages.json')['navigation']
print('PASS: market denominators, 100% shares, Logix/clone reconciliation, UK subset and no duplicated contracted OEMs.')
