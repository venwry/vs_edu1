"""Accepted programme timing, fair benchmarks, partner independence and disclosure."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/n).read_text())
c=read('comdex_1979_campaign.json');s=read('logix_aion_story.json');t=read('logix_aion_technical_catalog_v2.json')
e=next(e for p in s['phases'] for e in p['events'] if e['id']==c['metadata']['launch_event_ref'])
assert e['date']['start']==c['metadata']['launch_date']=='1979-12-03'
st=c['premiere']['stages'];assert sum(x['minutes'] for x in st)==c['premiere']['duration_minutes_before_questions']==45
ids=[x['id'] for x in st];assert ids.index('bpi')==ids.index('abacus_2')+1
assert 'head of independent BPI' in st[ids.index('bpi')]['description']
assert 'BPI leadership' in st[ids.index('partners')]['description']
assert 'actor.bpi' in [x['actor_ref'] for x in e['participants']]
d=c['speed_demonstration'];assert sum(d['segment_minutes'].values())==st[ids.index('aurelia_plus_speed')]['minutes']==6
assert d['measured_results'] is None
assert d['computer_refs']==['computer.aurelia','computer.aurelia_plus']
assert any('Same executable' in x for x in d['controls'])
assert any('no silent frame skipping' in x for x in d['controls'])
a=c['abacus_demonstration'];assert 'text-mode' in a['chart_scope']
r={x['id']:x for v in t.values() if isinstance(v,list) for x in v if isinstance(x,dict) and 'id'in x}
assert all(ref in r for ref in c['offering_refs'])
assert {x['computer_ref'] for x in r['edition.abacus_2.z80']['platform_support']}==set(d['computer_refs'])
assert c['disclosure']['architecture_reveal']==read('ncc_1979_campaign.json')['migration']['architecture_reveal']
f=read('sales_forecast.json');assert f['metadata']['november_forecast_end']<c['metadata']['launch_date']
assert [x['launch_through_november_1979']['units'] for x in f['scenarios']]==[49737,66900,77800]
print('PASS: COMDEX timing, matched workloads, no invented benchmark, Abacus/BPI order, compatibility and unchanged sales.')
