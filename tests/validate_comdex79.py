from data_paths import read_document, document_bytes, document_text
"""Accepted programme timing, fair benchmarks, partner independence and disclosure."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(n):return read_document(n, root=R)
c=read('generated/catalogs/comdex-1979-campaign.json');s=read('generated/catalogs/logix-aion-story.json');t=read('generated/catalogs/logix-aion-technical-catalog-v2.json')
e=next(e for p in s['phases'] for e in p['events'] if e['id']==c['main_launch_event_ref'])
assert e['date']['start']==c['launch_date']=='1979-12-03'
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
assert {x['computer_ref'] for x in r['software.abacus_2']['platform_support']}==set(d['computer_refs'])
assert c['disclosure']['architecture_reveal']==read('generated/catalogs/ncc-1979-campaign.json')['migration']['architecture_reveal']
for scenario in read('generated/models/sales-forecast.json')['scenarios']:
 assert all(r['products']['aurelia_plus']==0 for r in scenario['monthly'] if r['month']<'1979-12')
print('PASS: product launch gates and compatibility boundaries.')
