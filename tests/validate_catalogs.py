"""Run from any directory: python tests/validate_catalogs.py (requires jsonschema)."""
from pathlib import Path
import json, jsonschema
root=Path(__file__).resolve().parents[1]
def read(n):return json.loads((root/n).read_text())
story=read('logix_aion_story.json');tech=read('logix_aion_technical_catalog_v2.json');site=read('site_pages.json')
jsonschema.Draft202012Validator(read('logix_aion_story.schema.json')).validate(story)
records={x['id']:x for v in tech.values() if isinstance(v,list) for x in v if isinstance(x,dict) and 'id'in x}
actors={x['id'] for x in story['assumptions']['entities']};events=[e for p in story['phases'] for e in p['events']];event_ids={e['id'] for e in events}
assert len(event_ids)==len(events);assert len(actors)==len(story['assumptions']['entities']);assert len({p['id'] for p in story['phases']})==len(story['phases'])
for e in events:
 assert e['actions'],e['id']
 assert set(e['product_refs'])<=records.keys(),e['id']
 assert set(e['related_event_refs'])<=event_ids,e['id']
 assert {p['actor_ref'] for p in e['participants']}<=actors,e['id']
 for item in e['actions']+e['agreement_terms']:assert set(item['actor_refs'])<=actors,e['id']
 for item in e['metrics']+e['agreement_terms']:
  if isinstance(item['value'],dict):assert item['value']['minimum']<=item['value']['maximum']
for p in story['assumptions']['principles']:assert set(p['actor_refs'])<=actors
page_ids={p['id'] for p in site['pages']};paths={p['path'] for p in site['pages']}
assert len(page_ids)==len(site['pages'])==len(paths)
assert set(site['navigation'])<=page_ids
lanes=site['timeline_view']['lanes']
assigned=[e for lane in lanes for e in lane['event_refs']]
assert len(assigned)==len(set(assigned))==len(events)
assert set(assigned)==event_ids
for lane in lanes:assert set(lane['actor_refs'])<=actors
for p in site['pages']:
 assert (root/p['path']).exists(),p['path'];assert set(p['record_refs'])<=records.keys(),p['id']
 assert '<script defer src="atlas.js">' in (root/p['path']).read_text()
# Preserve event meanings and prevent an offer or future right becoming a completed transaction.
by={e['id']:e for e in events}
assert by['event.bpi_offer']['event_type']=='offer'
assert by['event.ibm_project']['event_type']=='plan'
assert by['event.apple_extensions']['date']['end']=='1979-06-07'
assert by['event.aionix_agreement']['agreement_terms'][4]['effective_date']['start']=='1982'
assert by['event.aurelia_launch']['date']['precision']=='month'
assert set(story)=={'assumptions','phases'}
print(f'Validated {len(events)} events, {len(actors)} actors, {len(site["pages"])} pages; schema and references pass.')
