"""December launch, open implementation, pricing gates and unaffected November sales."""
import json,hashlib,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/n).read_text())
c=read('logix_aion_technical_catalog_v2.json');s=read('logix_aion_story.json');p=read('pricing_results.json');f=read('sales_forecast.json')
r={x['id']:x for v in c.values() if isinstance(v,list) for x in v if isinstance(x,dict) and 'id' in x}
e=next(e for phase in s['phases'] for e in phase['events'] if e['id']=='event.plus_launch')
ids=['software.aurelia_compatibility_kit','service.aurelia_compatibility_support','service.aurelia_compatibility_certification']
for ref in ids:
 assert r[ref]['introduced']['event_start_date']==e['date']['start']=='1979-12-03'
 assert ref in e['product_refs']
 offer=next(x for x in p['products'] if x['id']==ref)
 assert offer['snapshots']['1979']['retail_price_usd'] is None
 assert offer['snapshots']['1980']['retail_price_usd']>0 and offer['channel']=='direct'
assert not set(read('pricing_baseline.json')['products']) & set(read('compatibility_pricing_baseline.json')['products'])
assert p['metadata']['compatibility_baseline_sha256']==hashlib.sha256((R/'compatibility_pricing_baseline.json').read_bytes()).hexdigest()
policy=r[ids[0]]['compatibility_policy']
assert 'without a bespoke partnership or mandatory certification' in policy['eligibility']
assert 'CP/M alone is insufficient' in policy['binary']
assert 'separate optional profiles' in policy['hardware']
assert 'No future processor' in policy['scope']
assert f['metadata']['forecast_end']<e['date']['start']
assert [x['launch_through_november_1979']['units'] for x in f['scenarios']]==[49737,66900,77800]
print('PASS: December compatibility kit, independent implementation, separate licences, snapshot gates and unchanged November forecast.')
