"""Apply the accepted Aurelia+ AION system-memory sourcing revision once."""
import json,copy
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(f):return json.loads((R/f).read_text())
def save(f,v):(R/f).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def edit(f,a,b):
 p=R/f;s=p.read_text();assert a in s,(f,a);p.write_text(s.replace(a,b))
if (R/'aurelia_plus_aion_memory.json').exists():raise SystemExit(0)
c=load('logix_aion_technical_catalog_v2.json');b=load('hardware_bom.json')
r={x['id']:x for a in c.values() if isinstance(a,list) for x in a if isinstance(x,dict) and 'id'in x}
host=r['computer.aurelia_plus'];chip=r['part.aion_4164'];old=r['part.dram_64kbit']
host['memory']['physical_population']['chip_ref']=chip['id']
host['memory']['physical_population']['status']='Accepted AION-manufactured eight-chip baseline; 64K×1 process, speed, power, decode and independent refresh qualification required before December 1979.'
host['manufacturing_requirements'][0]='Qualify eight AION-manufactured 64K×1 DRAMs (64 KiB total, one 8-bit bank) before December 1979. Confirm package/pinout, supply rails, retention, refresh deadlines and 6 MHz host timing.'
chip['used_in']=list(dict.fromkeys(chip['used_in']+[host['id']]))
chip['introduced']=copy.deepcopy(host['introduced'])
chip['manufacturing_requirements']=['Qualify AION 64K×1 silicon, process, speed/retention bins, refresh, package and power rails for Aurelia+ before December 1979; reuse qualified silicon in Artemis from May 1980. Purchased DRAM maturity is not evidence of AION production yield.']
chip['specification']['qualification_status']='AION-owned part; released package, speed grade, rails, refresh and production yield require qualification before December 1979.'
old['used_in']=[x for x in old['used_in'] if x!=host['id']]
old['manufacturing_requirements']=['Qualify purchased 64K×1 DRAMs for remaining external-source high-density modules and kits; Aurelia+ and Artemis AION configurations have separate make-part references.']
for a in b['assemblies']:
 if a['id']=='assembly.computer.aurelia_plus.base':
  for l in a['lines']:
   if l['ref']=='bompart.part.dram_64kbit':
    assert l['quantity']==8;l['ref']='bompart.part.aion_4164';l['role']='64 KiB system RAM: eight AION 64K×1 DRAMs'
  a['requirements']=host['manufacturing_requirements']
 if a['id']=='assembly.part.aion_4164':a['requirements']=chip['manufacturing_requirements']
 if a['id']=='assembly.part.dram_64kbit':a['requirements']=old['manufacturing_requirements']
for x in b['components']:
 if x['id']=='bompart.part.aion_4164':x['requirements']=chip['manufacturing_requirements']
 if x['id']=='bompart.part.dram_64kbit':x['requirements']=old['manufacturing_requirements']
for x in b['products']:
 if x['catalog_ref']==host['id']:x['requirements']=host['manufacturing_requirements']
save('logix_aion_technical_catalog_v2.json',c);save('hardware_bom.json',b)
# Advance the same 120 PM programme; do not charge development twice.
edit('tools/build_investment_model.py',"'aion_64k_dram','AION Labs','1977-Q3','1980-Q1',120","'aion_64k_dram','AION Labs','1977-Q3','1979-Q3',120")
edit('tools/build_investment_model.py','64K cell/array, sense amps, refresh/retention, bias/power, process integration, masks, probe, speed bins and respin; additional to the existing 16K programme','64K cell/array, sense amps, refresh/retention, bias/power, process integration, masks, probe, speed bins and respin; finish silicon qualification by Q3 1979 for Q4 Aurelia+ ramp, reuse in Artemis. Existing 120 PM moved earlier, not duplicated.')
edit('tools/build_investment_model.py','RAM mapping, PCB derivatives, power, firmware and qualification','RAM mapping, AION 64K system DRAM board/power/refresh qualification, PCB derivatives and firmware; production ramp by December 1979 within the existing 108 PM')
edit('tools/build_investment_model.py','Buy bare PCBs, system DRAM/CPUs, displays','Buy bare PCBs, remaining externally sourced system DRAM/CPUs, displays')
edit('tools/build_investment_model.py','AION 4116 display-memory chips, populate/test boards','AION 4116 display-memory chips and AION 64K system DRAM for Aurelia+ / Artemis, populate/test boards')
# Freeze immediate predecessor for the before/after ROI comparison.
roi=load('roi_1974_1980.json');iv=load('industrial_investment_1974_1981.json');sales=load('sales_forecast.json')
last=next(x for x in roi['scenarios'] if x['id']=='central')['quarterly'][-1]
year=next(x for x in iv['summary_annual'] if x['year']==1980)
sc=next(x for x in sales['scenarios'] if x['id']=='central')
metrics={'aurelia_plus_deliveries_to_nov18':sc['ncc_to_comdex1980']['aurelia_plus_units'],'artemis_deliveries_to_nov18':sc['ncc_to_comdex1980']['artemis_units'],'full_demand_1980':year['computer_demand'],'end_1980_headcount':year['year_end_headcount'],**{k:last[k] for k in ['cumulative_accounting_roi_pct','cumulative_net_cash_usd','peak_external_funding_usd','cumulative_net_revenue_usd']}}
save('artemis_display_baseline.json',{'source_commit':'7263e35dd2ed035b1a4880b3f3efc428f6486fad','status':'Pre-Aurelia+ AION-memory scenario; immediately preceding committed model, not historical accounts.','metrics':metrics})
edit('tools/build_roi.py',"current_display={'artemis_deliveries_to_nov18':","current_display={'aurelia_plus_deliveries_to_nov18':next(x for x in sales_display['scenarios'] if x['id']=='central')['ncc_to_comdex1980']['aurelia_plus_units'],'artemis_deliveries_to_nov18':")
edit('tools/build_roi.py','Artemis video card and Mono Pro revision','Aurelia+ AION memory revision')
edit('tools/build_roi.py','Central Artemis display-related interest increases 4.8% before elasticity, but higher prices can offset it.','Aurelia+ now uses eight AION 64K DRAMs. Revised manufacturing costs flow through balanced prices and existing price elasticity; no additional marketing or demand bonus is invented. Shared chip development is advanced for December 1979, not duplicated.')
edit('tools/build_roi.py','Incremental 1980 campaign: $435,000. Engineering increment: 306 person-months (150 display plus 156 memory/economy-card).','Previously budgeted display campaign: $435,000. Previously budgeted display/memory engineering: 306 person-months; the shared 120 PM 64K DRAM programme now completes in Q3 1979. Existing Aurelia+ board qualification covers integration.')
edit('tools/build_roi.py','href="artemis.html">Hardware, modes and qualification','href="aurelia-plus.html">Aurelia+ hardware and qualification')
# Keep historical Artemis scenario documentation, explicitly identify its comparison boundary.
p=R/'ARTEMIS_TIERS.md';s=p.read_text().replace('AION is replacing purchased chips only in Artemis high-density configurations; PRO sourcing remains unchanged.','AION supplies Artemis high-density configurations and, in the subsequent Aurelia+ sourcing revision, eight chips per Aurelia+; PRO sourcing remains unchanged.')
s=s.replace('the comparison baseline is the preceding main commit a19af421','the original tier comparison baseline was a19af421; the current ROI comparison tracks the subsequent Aurelia+ sourcing revision')
p.write_text(s)
p=R/'RAM_BOM_DESIGN.md';s=p.read_text().replace('| Aurelia+ | 64 KiB | 64K × 1 |','| Aurelia+ | 64 KiB | AION 64K × 1 |');p.write_text(s)
policy={'status':'Accepted planning scenario; production qualification remains required','source_commit':'7263e35dd2ed035b1a4880b3f3efc428f6486fad','effective_from':'1979-12-03','computer_ref':'computer.aurelia_plus','system_ram_chip_ref':'part.aion_4164','chip_count':8,'system_ram_kib':64,'die_area_mm2':45,'maturity_multiplier':.85,'development':'Existing 120 PM shared programme completed by 1979-Q3; existing 108 PM Aurelia+ integration programme includes qualification. No duplicate NRE.','demand':'Existing balanced-price rule and elasticity only; marketing and appeal assumptions unchanged.','capacity':'Rebuild wafer loading, tool counts, factory investment, staffing and logistics for modeled demand plus 10% installed good-output reserve; existing additional 5% fab engineering allowance and one-down redundancy retained.'}
save('aurelia_plus_aion_memory.json',policy)
(R/'AURELIA_PLUS_AION_MEMORY.md').write_text('''# Aurelia+ AION system memory

Aurelia+ uses eight AION 64K×1 DRAMs: 64 KiB system RAM in one 8-bit bank. Its 16 KiB display DRAM (eight AION 4116 chips), 1 KiB exclusive sprite SRAM, video modes and system DMA/bank/refresh controller remain as specified.

The selected shared AION 64 Kbit model retains its 45 mm² die and 0.85 maturity multiplier. Recurring packaged/tested chip cost is about $15.13 in 1980 and $14.45 in 1981: eight chips cost about $121.04 / $115.62 before motherboard integration. Year-specific wafer costs and defect densities apply. These are planning yields, not qualified results.

Aurelia+ launches on December 3, 1979. The existing 120 person-month AION DRAM programme is moved to finish in Q3 1979, allowing Q4 production ramp; the existing 108 person-month Aurelia+ hardware programme includes board/power/refresh qualification. Development is shared with Artemis and not charged twice. Released pinout, power rails, speed/retention bins, refresh timing and 6 MHz system integration remain qualification gates.

All descendants of the Aurelia+ base BOM inherit the replacement. Purchased 64 Kbit memory remains in the separately specified PRO/expansion configurations.

Manufacturing costs feed balanced retail prices and the existing price-sensitive sales model. No additional marketing or appeal uplift is added. The industrial plan recomputes component orders, wafer starts, tool counts, fab space, staffing, logistics and capital from full modeled demand plus 10% installed output reserve; the existing 5% fab engineering allowance and one-down equipment redundancy are separate.

The [ROI report](roi.html) compares this revision with commit 7263e35dd2ed035b1a4880b3f3efc428f6486fad. The sales page retains its constrained delivery forecast; ROI and factory sizing use the disclosed full-demand capacity scenario. See [costs](manufacturing-costs.html), [pricing](pricing.html), [sales](sales.html) and [factory investment](industrial_investment_1974_1981.html) for regenerated dated results.
'''.replace('7263e35dd2ed035b1a4880b3f3efc428f6486fad','7263e35dd2ed035b1a4880b3f3efc428f6486fad'))
print('Applied Aurelia+ AION system-memory sourcing; rebuild dependent models.')
