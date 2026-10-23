from data_paths import read_document, document_bytes, document_text
"""December launch, open implementation, pricing gates and unaffected November sales."""
import json,hashlib,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(n):return read_document(n, root=R)
c=read('generated/catalogs/logix-aion-technical-catalog-v2.json');s=read('generated/catalogs/logix-aion-story.json');p=read('generated/models/pricing-results.json');f=read('generated/models/sales-forecast.json')
r={x['id']:x for v in c.values() if isinstance(v,list) for x in v if isinstance(x,dict) and 'id' in x}
e=next(e for phase in s['phases'] for e in phase['events'] if e['id']=='event.plus_launch')
ids=['software.aurelia_compatibility_kit','service.aurelia_compatibility_support','service.aurelia_compatibility_certification']
for ref in ids:
 assert r[ref]['introduced']['event_start_date']==e['date']['start']=='1979-12-03'
 assert ref in e['product_refs']
 offer=next(x for x in p['products'] if x['id']==ref)
 assert offer['snapshots']['1979']['retail_price_usd'] is None
 assert offer['snapshots']['1980']['retail_price_usd']>0 and offer['channel']=='direct'
assert not set(read('baselines/pricing-baseline.json')['products']) & set(read('baselines/compatibility-pricing-baseline.json')['products'])
assert p['metadata']['compatibility_baseline_sha256']==hashlib.sha256(document_bytes('baselines/compatibility-pricing-baseline.json', root=R)).hexdigest()
policy=r[ids[0]]['compatibility_policy']
assert 'without a bespoke partnership or mandatory certification' in policy['eligibility']
assert 'CP/M alone is insufficient' in policy['binary']
assert 'separate optional profiles' in policy['hardware']
assert 'No future processor' in policy['scope']
for scenario in read('generated/models/sales-forecast.json')['scenarios']:
 assert all(r['products']['aurelia_plus']==0 for r in scenario['monthly'] if r['month']<'1979-12')
print('PASS: product launch gates and compatibility boundaries.')
