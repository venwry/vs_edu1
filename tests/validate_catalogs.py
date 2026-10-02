"""Run from any directory: python tests/validate_catalogs.py (requires jsonschema)."""
from pathlib import Path
import json, jsonschema
root=Path(__file__).resolve().parents[1]
def read(n):return json.loads((root/n).read_text())
story=read('logix_aion_story.json');tech=read('logix_aion_technical_catalog_v2.json');site=read('site_pages.json')
jsonschema.Draft202012Validator(read('logix_aion_story.schema.json')).validate(story)
records={x['id']:x for v in tech.values() if isinstance(v,list) for x in v if isinstance(x,dict) and 'id'in x}
import re
def check_refs(value):
 if isinstance(value,dict):
  for item in value.values():check_refs(item)
 elif isinstance(value,list):
  for item in value:check_refs(item)
 elif isinstance(value,str) and re.fullmatch(r'(?:computer|software|part|device|technology|service|bundle|edition)\.[a-z0-9_.]+',value):
  assert value in records, 'Unresolved catalog reference: '+value
check_refs(tech)
editions=tech['platform_editions']
edition_keys={'id','name','product_ref','execution_target','role','introduced','platform_support','minimum_resources','dependency_refs','delivery','support_status'}
for e in editions:
 assert set(e)==edition_keys,e['id']
 assert set(e['minimum_resources'])=={'installed_ram_kb','application_ram_bytes','rom_bytes','status'}
 assert e['execution_target'] in {'z80_cpm','era_aionix'}
 assert e['id'] in records[e['product_ref']]['edition_refs']
 assert len({p['computer_ref'] for p in e['platform_support']})==len(e['platform_support'])
 for support in e['platform_support']:
  assert set(support)=={'computer_ref','available_from'}
  assert support['available_from']>=records[support['computer_ref']]['introduced']['event_start_date']
for c in tech['computers']:
 expected={e['product_ref'] for e in editions if any(p['computer_ref']==c['id'] for p in e['platform_support'])}
 assert set(c['compatible_software'])==expected,c['id']
for id in ['computer.aurelia','computer.aurelia_plus']:
 assert {'software.abacus_1','software.abacus_2'}<=set(records[id]['compatible_software'])
assert records['software.aionix_server']['category']=='operating_system_edition'
assert records['device.network_card_aurelia']['sold_with']==['software.cpm_aurelia_networking']
assert 'used_in' not in records['part.artemis_ram_module_prototype']
accepted_designs=['technology.flexibus','technology.artemis_memory_model','technology.cpm80_virtual_peripheral_bridge','technology.aurelia_memory_model','software.bpi_client_server']
for id in accepted_designs:
 assert 'proposed_design' not in records[id]
 assert records[id]['specification']['implementation_design']['status'].startswith('Accepted design baseline')
profiles=records['technology.aurelia_memory_model']['specification']['implementation_design']['application_memory_profiles']
for p in profiles:
 assert int(p['bdos_entry'],16)==int(p['application_end_inclusive'],16)+1
 assert p['tpa_bytes']==int(p['bdos_entry'],16)-int(p['application_start'],16)
for c in tech['computers']:
 layout=c['video']['memory_layout'];text=layout['text_mode'];bitmap=layout['bitmap_mode']
 capacity=(c['memory'].get('video_ram_kb') or c['video']['video_ram_kb'])*1024
 assert text['allocated_bytes']==text['text_buffer_count']*(text['character_map_bytes_per_buffer']+text['attribute_map_bytes_per_buffer'])+text['font_bytes']
 assert text['allocated_bytes']<=capacity
 assert bitmap['framebuffer_count']*bitmap['bytes_per_framebuffer']+bitmap['remaining_vram_bytes']==capacity
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
explorer=tech['artemis_explorer']
assert set(explorer['computer_refs'])<=records.keys()
for layer,diagram in explorer['diagrams'].items():
 ids={n['id'] for n in diagram['nodes']}
 assert len(ids)==len(diagram['nodes']),layer
 for node in diagram['nodes']:
  if 'record_ref' in node:assert node['record_ref'] in records,node['record_ref']
 for edge in diagram['edges']:assert set(edge)<=ids,edge
for p in site['pages']:
 if p.get('explorer_family')=='artemis':assert 'src="artemis-explorer.js"' in (root/p['path']).read_text()
# Preserve event meanings and prevent an offer or future right becoming a completed transaction.
by={e['id']:e for e in events}
assert by['event.bpi_offer']['event_type']=='offer'
assert by['event.ibm_project']['event_type']=='plan'
assert by['event.apple_extensions']['date']['end']=='1979-06-07'
assert by['event.aionix_agreement']['agreement_terms'][4]['effective_date']['start']=='1982'
assert by['event.aurelia_launch']['date']['precision']=='month'
assert records['software.bpi_suite']['introduced']['event_start_date']=='1978-06-05'
assert records['technology.bpi_relational_database']['introduced']['event_start_date']=='1978-06-05'
assert records['software.microsoft_basic_aurelia']['introduced']['event_start_date']=='1979-06-04'
for product,edition in [('software.bpi_suite','edition.bpi_suite.z80'),('software.microsoft_basic_aurelia','edition.microsoft_basic_aurelia.z80')]:
 assert records[product]['introduced']==records[edition]['introduced']
assert 'event.bpi_launch' in {e['id'] for p in story['phases'] if p['id']=='phase.ncc78' for e in p['events']}
assert 'event.basic_launch' in {e['id'] for p in story['phases'] if p['id']=='phase.ncc79' for e in p['events']}
assert 'phase.comdex78' not in {p['id'] for p in story['phases']}
for data in [tech,story]:assert not re.search(r'COMDEX.{0,20}1978',json.dumps(data),re.I)
assert set(story)=={'assumptions','phases'}
print(f'Validated {len(events)} events, {len(actors)} actors, {len(site["pages"])} pages; schema and references pass.')
