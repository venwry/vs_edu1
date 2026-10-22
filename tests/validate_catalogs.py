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
 if 'text_modes' in c['video']:
  for mode in c['video']['text_modes']+c['video']['bitmap_modes']:
   for config in mode['configurations']:assert config['allocated_bytes']+config['remaining_video_ram_bytes']==c['memory']['video_ram_kb']*1024
  continue
 layout=c['video']['memory_layout'];text=layout['text_mode'];bitmap=layout['bitmap_mode']
 capacity=(c['memory'].get('video_ram_kb') or c['video']['video_ram_kb'])*1024
 assert text['allocated_bytes']==text['text_buffer_count']*(text['character_map_bytes_per_buffer']+text['attribute_map_bytes_per_buffer'])+text['font_bytes']
 assert text['allocated_bytes']<=capacity
 assert bitmap['framebuffer_count']*bitmap['bytes_per_framebuffer']+bitmap['remaining_video_ram_bytes']==capacity
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
 if p.get('kind') == 'report':
  assert '<script' in (root/p['path']).read_text()
 else:
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
assert by['event.apple_extensions']['date']['start']=='1979-06-04'
assert by['event.apple_extensions']['date']['end']=='1979-06-04'
assert by['event.aionix_agreement']['agreement_terms'][4]['effective_date']['start']=='1982'
assert all(set(e['date'])=={'start','end'} and e['date']['end']>=e['date']['start'] for e in events)
assert [e['id'] for e in events if e['date']['end']!=e['date']['start']]==['event.ncc78_sessions_media']
assert records['software.bpi_suite']['introduced']['event_start_date']=='1978-06-05'
assert records['technology.bpi_relational_database']['introduced']['event_start_date']=='1978-06-05'
assert records['software.microsoft_basic_aurelia']['introduced']['event_start_date']=='1979-06-04'
for product,edition in [('software.bpi_suite','edition.bpi_suite.z80'),('software.microsoft_basic_aurelia','edition.microsoft_basic_aurelia.z80')]:
 assert records[product]['introduced']==records[edition]['introduced']
assert 'event.bpi_launch' in {e['id'] for p in story['phases'] if p['id']=='phase.ncc78' for e in p['events']}
assert 'event.basic_launch' in {e['id'] for p in story['phases'] if p['id']=='phase.ncc79' for e in p['events']}
assert 'phase.comdex78' not in {p['id'] for p in story['phases']}
for data in [tech,story]:assert not re.search(r'COMDEX.{0,20}1978',json.dumps(data),re.I)
assert set(story)=={'assumptions','phases','processes'}
print(f'Validated {len(events)} events, {len(actors)} actors, {len(site["pages"])} pages; schema and references pass.')


# Calendar phases must cover the requested period without gaps or overlaps.
from datetime import date, timedelta
phases=story['phases']
assert len(phases)==9
assert phases[0]['period']['start']=='1972-01-01'
assert phases[-1]['period']['end']=='1983-12-31'
for i,phase in enumerate(phases):
 start=date.fromisoformat(phase['period']['start']);end=date.fromisoformat(phase['period']['end'])
 assert start<=end
 if i:assert date.fromisoformat(phases[i-1]['period']['end'])+timedelta(days=1)==start
phase_by_event={e['id']:p['id'] for p in phases for e in p['events']}
assert phase_by_event['event.companies']=='phase.prepare_aurelia'
assert phase_by_event['event.facility']=='phase.prepare_aurelia'
assert 'event.exchanges' not in phase_by_event
assert phase_by_event['event.plus_launch']=='phase.comdex79'
assert by['event.plus_launch']['date']['start']=='1979-12-03'
assert phase_by_event['event.cpm_bridge']=='phase.ncc79' # Development precedes launch.
assert phase_by_event['event.artemis_software']=='phase.ncc79'
assert phase_by_event['event.aionix_agreement']=='phase.ncc78'
assert all(target in {p['id'] for p in phases} for target in site['timeline_view']['phase_aliases'].values())
print('Validated nine consecutive phases, confirmed-date placement, processes and legacy phase aliases.')

assert len(events)==142
assert 'event.basic_develop' not in event_ids
processes=[p for parent in story['processes'] for p in [parent]+parent.get('subprocesses',[])];process_ids={p['id'] for p in processes}
assert len(process_ids)==len(processes)==17
for proc in processes:
 assert set(proc['phase_refs'])<={p['id'] for p in phases}
 assert set(proc['related_event_refs'])<=event_ids
 assert set(proc['product_refs'])<=records.keys()
 assert {p['actor_ref'] for p in proc['participants']}<=actors
 for action in proc['actions']:assert set(action['actor_refs'])<=actors
assert 'process.economics_studies' in process_ids and 'process.nyse_speculation' not in process_ids
assert 'process.international_investment' not in process_ids
for phase in phases:
 for e in phase['events']:
  if e['id']!='event.power':assert phase['period']['start']<=e['date']['start']<=phase['period']['end'],e['id']
assert by['event.power']['date']['start']=='2025-12-07'
assert records['service.bpi_training']['introduced']['event_start_date']=='1978-06-12'
assert records['service.academy_direct_sales']['introduced']['event_start_date']=='1978-03-25'
for id in ['computer.aurelia_plus','software.pulse_1','software.abacus_2']:
 assert records[id]['introduced']['event_start_date']=='1979-12-03'
assert '1979-11' not in json.dumps(tech)
assert all(target in process_ids|event_ids|{p['id'] for p in story['assumptions']['principles']}|{p['id'] for p in phases} for target in site['timeline_view']['item_aliases'].values())
print(f'Validated {len(events)} events, {len(story["processes"])} parent processes and synchronized catalog availability.')

# Each top-level process has one lane; nested processes inherit their parent lane.
assigned_processes=[x for lane in lanes for x in lane.get('process_refs',[])]
assert len(assigned_processes)==len(set(assigned_processes))==len(story['processes'])
assert set(assigned_processes)=={p['id'] for p in story['processes']}
assert 'timeline2' not in page_ids
study=next(p for p in story['processes'] if p['id']=='process.economics_studies')
assert len(study['subprocesses'])==4
for child in study['subprocesses']:
 assert study['period']['start']<=child['period']['start']<=child['period']['end']<=study['period']['end']
assert by['event.us_nyse_start']['date']['start']=='1972-03-01'
assert by['event.us_nyse_start']['related_event_refs']==['event.lottery']
for name in ['organization_buildout','market_monitoring','market_expansion']:
 assert 'process.'+name not in process_ids
 assert any(p['id']=='assumption.'+name for p in story['assumptions']['principles'])
print('Validated nested academic years, migrated assumptions and timeline navigation.')




