"""Check configuration-specific card, sourcing, offer and demand invariants."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(f):return json.loads((R/f).read_text())
c=read('generated/catalogs/logix-aion-technical-catalog-v2.json')
r={x['id']:x for a in c.values() if isinstance(a,list) for x in a if isinstance(x,dict) and 'id'in x}
b=read('generated/catalogs/hardware-bom.json');aa={x['id']:x for x in b['assemblies']}
def pop(id):
 out={}
 for x in aa[id]['lines']:
  sub=pop(x['ref']) if x['ref'] in aa else {x['ref']:1}
  for k,n in sub.items():out[k]=out.get(k,0)+n*(x['quantity'] or 1)
 return out
small=r['computer.artemis']['video']
assert small['video_ram_kb']==16 and small['display_memory']['bank_data_width_bits']==8
assert small['host_interface']['host_width_bits']==32
assert small['pixel_buffer']['total_bytes']==160
assert small['sprite_memory']['capacity_bytes']==1024
assert len(small['text_modes'])==2 and len(small['bitmap_modes'])==6
for m in small['text_modes']:
 assert 2*m['ram_bytes_per_page']+m['font_bytes']<=16384
for m in small['bitmap_modes']:
 assert m['bytes_per_framebuffer']<=16384
 assert m['double_buffering']==(2*m['bytes_per_framebuffer']<=16384)
for m in small['text_modes']+small['bitmap_modes']:
 assert m['sprites_available']==5 and 'raster_640_400' not in m['required_raster_ids']
lo=pop('assembly.computer.artemis.m32_128');hi=pop('assembly.computer.artemis.m128_256');pro=pop('assembly.computer.artemis_pro.base')
assert lo['bompart.part.aion_4116']==8 and lo['bompart.part.aion_2114']==2
assert lo['bompart.part.aurelia_video_chip']==1 and not lo.get('bompart.part.artemis_graphics_chip')
assert hi['bompart.part.aion_4116']==16 and hi['bompart.part.aion_2114']==2
assert hi['bompart.part.aion_4164']==32 and not hi.get('bompart.part.dram_64kbit')
assert hi['bompart.part.artemis_graphics_chip']==1 and not hi.get('bompart.part.aurelia_video_chip')
assert pop('assembly.computer.artemis_pro.m128_512')['bompart.part.aion_4164']==64
assert not pop('assembly.computer.artemis_pro.m128_512').get('bompart.part.dram_64kbit')
assert 'bundle.artemis_128_mono_pro' not in r and 'bundle.artemis_256_mono' not in r
for layer in ['hardware','memory']:
 nodes=c['artemis_explorer']['diagrams'][layer]['nodes']
 assert not {'display_dram','sprite_sram','pixel_fifo','display_refresh'}&{n['id'] for n in nodes}
 assert any(n.get('computer_path')=='video' for n in nodes)
mix=read('generated/catalogs/sales-model-inputs.json')['basket_components']['artemis']
assert abs(sum(x['quantity'] for x in mix if x['product_ref'].startswith('bundle.'))-1)<.000001
iv=read('generated/models/industrial-investment-1974-1981.json')
assert sum(p['person_months'] for p in iv['engineering_programs'] if p['id'] in ['aion_64k_dram','artemis_tier_hardware','artemis_economy_driver'])==156
print('PASS: Artemis tier BOMs, mode allocation, monitor constraints, selected-card diagrams, AION sourcing and sales reconciliation.')

