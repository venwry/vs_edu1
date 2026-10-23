from data_paths import resolve_path
"""Check NCC cost populations, pricing policy, campaign arithmetic and launch dates."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
load=lambda n:json.loads((R/n).read_text())
campaign=load('generated/catalogs/ncc-1982-campaign.json');review=load('generated/models/manufacturing-costs.json')['reviews']['ncc-1982'];catalog=load('generated/catalogs/logix-aion-technical-catalog-v2.json');costs={x['id']:x for x in load('generated/models/manufacturing-costs.json')['products']};prices={x['id']:x for x in load('generated/models/pricing-results.json')['products']}
assert campaign['headline']=='Pointy ideas with a solid point.'
assert campaign['conference']['start']=='1982-06-07' and campaign['conference']['end']=='1982-06-10'
subtotal=sum(x['usd'] for x in campaign['budget_rows'])
assert subtotal==campaign['budget_subtotal_usd']
assert abs(campaign['budget_total_usd']-subtotal*1.15)<.001
for n,h in review['source_sha256'].items():
 source=(R/resolve_path(n)).read_bytes()
 if review.get('source_hash_scopes',{}).get(n)=='canonical_json_without_reviews':
  source=json.dumps({k:v for k,v in json.loads(source).items() if k!='reviews'},sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
 assert hashlib.sha256(source).hexdigest()==h,n
for id,n in [('device.artemis_video_card_64kb',8),('device.artemis_professional_video_128kb',16)]:
 row=costs[id];v={x['component_ref']:x['quantity'] for x in row['snapshots']['1982']['bom_lines']}
 assert v['bompart.part.aion_4164']==n
 assert row['snapshots']['1981']['total_usd'] is None
 assert prices[id]['snapshots']['1982']['pricing_balance']['status']=='no_proxy_cost_based'
v={x['component_ref']:x['quantity'] for x in costs['device.artemis_video_card_64kb']['snapshots']['1982']['bom_lines']}
assert v['bompart.part.aion_2114']==2
for pack in campaign['packages']:
 row=prices[pack['id']]['snapshots']['1982']
 assert abs(sum(costs[x]['snapshots']['1982']['total_usd'] for x in pack['components'])-row['manufacturing_cost_usd'])<.011
 assert abs(row['contribution_margin_on_net_revenue_pct']-25)<.02
team=prices['software.aion_development_team'];assert team['launch_snapshot']['date']=='1981-11-19'
assert team['launch_snapshot']['retail_price_usd']==team['snapshots']['1982']['retail_price_usd']==745.23
assert team['snapshots']['1981']['retail_price_usd'] is None
assert team['snapshots']['1982']['unit_profit_usd']==-279.46
assert 'software.autocad_1_artemis' not in prices
assert costs['software.autocad_1_artemis']['snapshots']['1982']['total_usd'] is None
mode=next(x for x in catalog['devices'] if x['id']=='device.artemis_professional_video_128kb')['specification']['bitmap_modes'][0]
assert mode['width']*mode['height']*mode['bits_per_pixel']//8==120000
assert mode['simultaneous_shades']==4 and mode['palette_grayscale_levels']==16
assert mode['bytes_per_framebuffer']+mode['remaining_video_ram_bytes']==131072
print('PASS: NCC campaign, itemized RAM, package single counting, June cutoff, Team launch subsidy and review provenance.')
