from data_paths import read_document, document_bytes, document_text
"""Check accepted card architecture, monitor safety, BOM uniqueness and forecast propagation."""
import json,math
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(f):return read_document(f, root=R)
c=read('generated/catalogs/logix-aion-technical-catalog-v2.json');r={x['id']:x for a in c.values() if isinstance(a,list) for x in a if isinstance(x,dict) and 'id'in x}
b=read('generated/catalogs/hardware-bom.json');assemblies={x['id']:x for x in b['assemblies']}
def population(id):
 out={}
 for x in assemblies[id]['lines']:
  sub=population(x['ref']) if x['ref'] in assemblies else {x['ref']:1}
  for k,v in sub.items():out[k]=out.get(k,0)+v*(x['quantity'] or 1)
 return out
v=r['computer.artemis_pro']['video'];assert v==r['computer.artemis']['video_variants'][1]['specification']
assert v['display_memory']['capacity_bytes']==16*16384//8==32768
assert v['sprite_memory']['capacity_bytes']==2*1024*4//8==1024
assert v['pixel_buffer']['pages']*v['pixel_buffer']['bytes_per_page']==640
assert v['character_row_cache']['total_bytes']==320
assert len(v['text_modes'])==4 and len(v['bitmap_modes'])==10
for m in v['text_modes']:
 assert m['character_map_bytes_per_buffer']>=m['columns']*m['rows']
 assert m['font_bytes']>=256*m['glyph_height']
 assert 2*m['ram_bytes_per_page']+m['font_bytes']<=32768
for m in v['bitmap_modes']:
 assert m['stride_bytes']*m['height']==m['width']*m['height']*m['bits_per_pixel']//8==m['bytes_per_framebuffer']
 assert m['double_buffering']==(2*m['bytes_per_framebuffer']<=32768)
for m in v['text_modes']+v['bitmap_modes']:
 assert m['sprites_available']==5
 if m['height']==400:assert m['required_raster_ids']==['raster_640_400']
 for a in m['configurations']:assert a['allocated_bytes']+a['remaining_video_ram_bytes']==32768
for host in ['computer.artemis_pro']:
 inv=population('assembly.'+host+'.base')
 assert inv['bompart.part.aion_4116']==16 and inv['bompart.part.aion_2114']==2
 assert inv['bompart.part.artemis_graphics_chip']==1
 assert r[host]['io_and_expansion']['expansion_slots']['count']==4
 assert r[host]['io_and_expansion']['dedicated_video_slot']['general_purpose_slots_consumed']==0
for d in c['devices']:
 if d['category']=='monitor':assert ('raster_640_400' in d['specification']['capabilities']['raster_ids'])==(d['id']=='device.mono_pro')
for bundle in c['offered_bundles']:
 if bundle['id'].endswith('_mono_pro'):
  assert bundle['included_devices']==['device.flexibus_keyboard','device.mono_pro']
  inv=population(bundle['bom_assembly_ref']);assert inv['bompart.part.brimar_m36_141w_crt']==1 and inv['bompart.part.artemis_graphics_chip']==1
policy=read('generated/catalogs/artemis-display-revision.json');s=read('generated/models/sales-forecast.json');inv=read('generated/models/industrial-investment-1974-1981.json');roi=read('generated/models/roi-1974-1980.json')
for q in inv['quarterly_capacity']:
 assert q['installed_computer_capacity_month']>=math.floor(q['peak_month_customer_demand']*1.05)
for q,amount in policy['incremental_marketing_usd'].items():assert sum(x['central_usd'] for x in roi['marketing']['items'] if x['quarter']==q and x['programme']=='Mono Pro incremental campaign')==amount
assert all(not r['products'].get('artemis_pro') for m,r in inv['monthly_demand'].items() if m<'1981-07')
assert sum(p['person_months'] for p in inv['engineering_programs'] if p['id'] in ['artemis_video_card_increment','mono_pro_receiver','mono_pro_card_board','artemis_display_drivers'])==150
assert '__DISPLAY_REVISION__' not in (R/'roi.html').read_text()
print('PASS: Artemis card modes, monitor compatibility, exclusive memory, bundle uniqueness, demand uplift, reserve capacity, NRE and marketing propagation.')

