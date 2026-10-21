"""Campaign separation, migration timing and no retroactive forecasts."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/n).read_text())
c=read('ncc_1979_campaign.json');s=read('logix_aion_story.json');t=read('logix_aion_technical_catalog_v2.json');f=read('sales_forecast.json')
e={x['id']:x for p in s['phases'] for x in p['events']}
r={x['id']:x for v in t.values() if isinstance(v,list) for x in v if isinstance(x,dict) and 'id' in x}
assert len(e)==90
assert sum(x['minutes'] for x in c['premiere']['stages'])==c['premiere']['duration_minutes_before_questions']==50
assert read('aurelia_1978_campaign.json')['premiere']['duration_minutes_before_questions']==44
ids=[x['id'] for x in c['premiere']['stages']]
assert ids.index('partners')<ids.index('migration')<ids.index('availability')
assert 'Abacus first, then independent BPI' in next(x['description'] for x in c['premiere']['stages'] if x['id']=='applications')
assert {x['id'] for x in c['profiles']}=={'cpm_application','flexibus_peripheral','logix_display'}
for item in c['schedule']:assert e[item['event_ref']]['date']['start']==item['date']
m=c['migration'];assert m['native_binary_compatibility'] is False
assert m['public_announcement']<e['event.cpm_bridge']['date']['start']<r['device.artemis_cpm80_module']['introduced']['event_start_date']==m['architecture_reveal']=='1980-05-19'
assert r['device.artemis_cpm80_module']['sold_separately'] is True
assert r['device.artemis_cpm80_module']['compatible_with']==['computer.artemis']
assert r['technology.aion_c_portability_framework']['introduced']['event_start_date']=='1980-05-19'
assert all('unsigned prospect' in x['status'] for x in c['manufacturer_assessment'])
assert c['targets']['ncc1980']['supported_non_logix_manufacturers_range']==[3,5]
assert c['targets']['end_1979']['status'].startswith('Target')
assert c['eight_bit_outlook']['threshold_usd']==100 and c['eight_bit_outlook']['reference_year']==1979
assert c['economics']['budget_usd'] is None
sc=next(x for x in f['scenarios'] if x['id']=='central')
assert all(row['month']<'1979-06' for row in sc['months'])
assert sum(row['units'] for row in sc['months'])==sc['launch_year']['units']
assert 'No Apple CP/M' in next(x['description'] for x in c['premiere']['stages'] if x['id']=='apple_video')
print('PASS: separate 1978/1979 campaigns, optional profiles, migration disclosure and dates, prospective OEM targets and preserved pre-NCC forecast boundary.')

# 1979 timeline must not expose future technical names or direct spec links.
import re
for item in e.values():
 if item["date"]["start"].startswith("1979"):
  visible={k:v for k,v in item.items() if k != "id"}
  assert not re.search(r"artemis|\bera1?\b|aionix",json.dumps(visible),re.I), item["id"]
assert c["disclosure_policy"]["embargo_until"]==m["architecture_reveal"]
assert "internal_product_ref" not in m
assert not re.search(r"artemis|\bera1?\b|aionix",json.dumps(c),re.I)
process=next(x for x in s["processes"] if x["id"]=="process.artemis_engineering")
assert not process["product_refs"]
print("PASS: 1979 next-generation entries and campaign withhold future technical names and specification links.")

