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
for sc in f['scenarios']:
 for row in sc['months']:
  assert row['units']==row['pre_reaction_units']-row['apple_displacement_units']-row['tandy_deferred_units']+row['compatibility_gain_units']
  if row['month']<'1979-05':assert row['tandy_deferred_units']==row['compatibility_gain_units']==0
 assert sum(x['pre_reaction_units'] for x in sc['months'])==sc['pre_reaction_units']
 assert sc['reaction_delta_units']==sc['launch_year']['units']-sc['pre_reaction_units']
assert f['reaction_policy']['tandy_computer_shipments_before_ncc']==f['reaction_policy']['tandy_abacus_customer_licenses_before_ncc']==f['reaction_policy']['ibm_pre_ncc_sales_effect']==0
print('PASS: scenario dates, staged Tandy port with native video, external commercial boundaries, AIONix sequence, source hashes and no retroactive Tandy/IBM sales.')
