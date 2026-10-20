"""Cross-file campaign dates, presentation order and variable-credit accounting."""
import json,math
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/n).read_text())
c=read('aurelia_1978_campaign.json');s=read('logix_aion_story.json');t=read('logix_aion_technical_catalog_v2.json');p=read('pricing_results.json')
e={e['id']:e for phase in s['phases'] for e in phase['events']}
r={x['id']:x for v in t.values() if isinstance(v,list) for x in v if isinstance(x,dict) and 'id'in x}
assert e['event.academy']['date']['start']==c['academy']['established_date']=='1978-03-25'
assert e['event.aurelia_launch']['date']['start']==c['academy']['public_announcement_date']=='1978-06-05'
assert c['academy']['launch_city_count']==r['service.academy_before_you_buy']['launch_program']['launch_city_count']==5
assert c['academy']['city_names'] is None and c['academy']['tuition_usd'] is None
assert c['academy']['credit']==r['service.academy_before_you_buy']['completion']['fundamentals_purchase_credit']
assert all(x['event_ref'] in e for x in c['schedule'])
a=c['premiere']['stages'];ids=[x['id'] for x in a]
assert ids.index('partners')+1==ids.index('academy') and ids.index('academy')+1==ids.index('packages')
assert sum(x['minutes'] for x in a)==c['premiere']['duration_minutes_before_questions']==44
assert len(c['technical_sessions'])==2 and c['broadcast_program']['broadcast_fee_usd']==0
assert e['event.ncc78_sessions_media']['date']=={'start':'1978-06-05','end':'1978-06-08'}
assert r['service.bpi_training']['introduced']['event_start_date']==c['academy']['bpi_training_start']=='1978-06-12'
for offer in p['products']:
 if not offer['id'].startswith('service.academy_regular_courses.course_'):continue
 for year,snapshot in offer['snapshots'].items():
  v=snapshot['before_you_buy_variant'];fundamentals=offer['id'].endswith('.course_1')
  expected=float(Decimal(str(v['retail_price_usd']*c['academy']['credit']['tuition_fraction'])).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)) if fundamentals else 150
  assert v['voucher_face_value_usd']==v['maximum_incremental_promotion_cost_usd']==expected
  assert math.isclose(v['contribution_after_full_voucher_usd'],v['retail_price_usd']-snapshot['manufacturing_cost_usd']-expected,abs_tol=.011)
assert c['cost_boundary']['campaign_budget_usd'] is None
print('PASS: Academy establishment versus announcement, five-city scope, presentation order, conference interval, free broadcast supply and 50% credit accounting across every annual snapshot.')
