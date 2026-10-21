"""Explicit alternative-history demand policy; counts are forecasts, not observations."""
import math
from collections import defaultdict
POLICY = {
 'horizon':'1980-01 through 1982-12',
 'capacity_headroom':.05,
 '1980_incremental_reaction_factors':[.98,.94,.96,1.0],
 'quarter_run_rate_vs_december_1980':[1.03,1.10,1.08,1.14,1.16,1.17,1.19,1.28],
 'native_share':[.34,.40,.44,.49,.53,.57,.61,.65],
 'pro_share':[0,0,.018,.025,.030,.035,.040,.045],
 'quarter_reasons':[
  'Apple business bundles and Tandy CP/M alternatives modestly displace demand; IBM has no qualified disk OS.',
  'Artemis qualification and native application availability constrain adoption; C source portability is not binary compatibility.',
  'Peripheral adapters and developer ports support demand, offset by selective enterprise purchasing.',
  'Native applications mature; independent OEM agreements remain qualification prospects, not automatic orders.',
  'CP/M/TUI installed base and documented interfaces sustain demand; no CP/M-86 competitor exists.',
  'Network launch and BPI pilots increase interest; portable CP/M competitors limit workstation growth.',
  'Recession and cautious dealer inventory offset conditional PRO availability; storage and recovery gates constrain server uptake.',
  'Team Edition pilots and developer interest support a modest spike; four-seat teams and 5 MB storage limit initial scope.',
  'IBM independent disk-OS launch assumed March 1982; recession and buyer waiting constrain growth.',
  'IBM business-channel credibility offsets cheaper Logix RAM and platform maturity; 286 availability starts port feasibility only.',
  'DRI 68k prototype work and third-party drivers support confidence; no production 68k AIONix or x86 AIONix revenue assumed.',
  'Late-year recovery, qualified compatibility and developer references support a forecast demand spike; no unqualified process savings.'
 ],
 'bounds':{'conservative':.8,'central':1.,'strong':1.2},
 'method':'1980 factors are incremental to existing signed reaction/price effects. 1981–82 quarterly run rates are relative to reassessed December 1980, replacing 4% compounded monthly growth. Existing balanced prices are held; no second price-elasticity or marketing bonus. Bounds are judgement scenarios, not statistical intervals.',
 'premises':['CP/M-86 does not exist; DRI prioritizes CP/M-80/TUI and AIONix/PRO.', 'Adam owns 30% of independent DRI; IBM sees a strategic conflict with competitor Logix.', 'Paterson does not create QDOS; IBM commissions its own alternative disk OS, with qualification risk.', 'DRI non-ERA port rights activate in 1982; 68k requires suitable MMU/system design; 286 enables feasibility, not an immediate release.', 'ERAv1 remains 3 um. June 1982 repaired 3 um RAM costs remain the volume cost basis through year-end; 2 um pilot savings await repeatable-production approval.', 'Adam foresees demand peaks, not engineering success: reserve 5% commercial headroom, retain OEE, one-down redundancy and qualification gates.'],
 'team_licenses_1981':[0,0,0,0,0,0,0,0,0,0,12,24],
 'team_licenses_1982':[30,35,40,45,50,55,60,65,70,80,90,100],
 'team_scope':'Small four-developer teams and pilots; existing 5 MB server constrains repositories. No large-storage product or enterprise-scale deployment assumed. Client and server purchases are contained in computer totals, not added again.',
 'external_revenue_boundary':'No external OEM, 68k/x86 AIONix port or unpriced storage revenue; independent third-party sales are not Logix receipts.'
}
def quarter(m):return m[:4]+'-Q'+str((int(m[5:7])-1)//3+1)
def allocate(total,weights):
 raw={k:total*v/sum(weights.values()) for k,v in weights.items()};out={k:int(v) for k,v in raw.items()}
 for k in sorted(raw,key=lambda k:raw[k]-out[k],reverse=True)[:total-sum(out.values())]:out[k]+=1
 return out

def reassess(original, multiplier=1.):
 out={m:{'products':dict(r['products']),'basis':r['basis']} for m,r in original.items() if m<'1980-01'}
 for m,r in original.items():
  if not m.startswith('1980'):continue
  factor=POLICY['1980_incremental_reaction_factors'][(int(m[5:])-1)//3]*multiplier
  out[m]={'products':allocate(round(sum(r['products'].values())*factor),r['products']), 'basis':POLICY['quarter_reasons'][(int(m[5:])-1)//3]}
 base=sum(out['1980-12']['products'].values())
 for i,factor in enumerate(POLICY['quarter_run_rate_vs_december_1980']):
  year=1981+i//4;q=i%4+1
  for j,season in enumerate([.95,1,1.05] if q!=4 else [.90,1.03,1.07]):
   month=f'{year}-{(q-1)*3+j+1:02}';native=POLICY['native_share'][i];pro=POLICY['pro_share'][i];old=.025 if year==1981 else .01
   out[month]={'products':allocate(round(base*factor*season),{'aurelia':old,'aurelia_plus':1-native-old,'artemis':native-pro,'artemis_pro':pro}), 'basis':POLICY['quarter_reasons'][i+4]}
 return dict(sorted(out.items()))
def team_units(m):return POLICY.get('team_licenses_'+m[:4],[0]*12)[int(m[5:])-1]
def team_quarter_budget(q):
 # All accepted gross development provision allocated at original dates.
 total=0
 for year in [1980,1981]:
  for mm in range(1,13):
   m=f'{year}-{mm:02}'
   if quarter(m)!=q:continue
   if '1980-12'<=m<='1981-11':total+=80000
   if '1981-02'<=m<='1981-11':total+=18000
   if '1981-04'<=m<='1981-11':total+=7500
   if year==1981:total+=15000
 return total
