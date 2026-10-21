"""Prevent retroactive sales, accidental video requirements and date/source conflation."""
import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/n).read_text())
s=read('logix_aion_story.json');t=read('logix_aion_technical_catalog_v2.json');m=read('market_reactions.json');f=read('sales_forecast.json')
e={e['id']:e for p in s['phases'] for e in p['events']};r={x['id']:x for v in t.values() if isinstance(v,list) for x in v if isinstance(x,dict) and 'id'in x}
for x in m['events']:assert e[x['event_ref']]['date']['start']==x['date']
seq=['event.aurelia_launch','event.tandy_contact','event.tandy_agreement','event.tandy_design_review','event.tandy_port_review','event.tandy_announcement','event.tandy_ncc_demo','event.tandy_release']
assert [e[x]['date']['start'] for x in seq]==sorted(e[x]['date']['start'] for x in seq)
assert e['event.aionix_preliminary']['date']['start']<e['event.aurelia_launch']['date']['start']<e['event.aionix_agreement']['date']['start']
assert r['edition.abacus_1.model_ii']['platform_support']==[{'computer_ref':'computer.trs80_model_ii','available_from':'1979-10-15'}]
assert r['edition.abacus_1.model_ii']['dependency_refs']==['software.cpm_model_ii']
assert r['device.model_ii_flexibus']['specification']['video_requirement']=='None; native Tandy video retained.'
assert all('model_ii' not in x['id'] for x in read('manufacturing_costs.json')['products'])
assert all('model_ii' not in x['id'] for x in read('pricing_results.json')['products'])
assert f['metadata']['source_reactions_sha256']==hashlib.sha256((R/'market_reactions.json').read_bytes()).hexdigest()
assert f['metadata']['source_story_sha256']==hashlib.sha256((R/'logix_aion_story.json').read_bytes()).hexdigest()
assert f['metadata']['current_forecast_horizon']=='1982-12-31'
print('PASS: scenario dates, staged Tandy port, external boundaries, AIONix sequence and current forecast provenance.')
