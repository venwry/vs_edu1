"""Rebuild the embedded NCC review from canonical costs and prices."""
from pathlib import Path
import json, hashlib
R=Path(__file__).resolve().parents[1]
def load(n):return json.loads((R/n).read_text())
def save(n,d):(R/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
p=load('generated/models/pricing-results.json');rows={x['id']:x for x in p['products']};campaign=load('generated/catalogs/ncc-1982-campaign.json');team=load('generated/catalogs/team-development-program.json')
ids=[x for x in campaign['offering_refs'] if x.startswith(('device.','software.'))]+[x['id'] for x in campaign['packages']]
review={'as_of':'1982-06-15','headline':campaign['headline'],'basis':'Engineering recurring-cost estimates, not supplier quotations or measured production yields. Nominal USD before tax.','pricing_method':p['policy']['formula'],'comparator_limitation':'No verified like-for-like June 1982 comparator for these new products; apply existing 25% contribution/net-revenue fallback. This is not a claim of equal market-discount percentages.','products':[{'id':i,'name':rows[i]['name'],**rows[i]['snapshots']['1982']} for i in ids],'team_launch_price':rows['software.aion_development_team']['launch_snapshot'],'team_1982_price':rows['software.aion_development_team']['snapshots']['1982'],'campaign_budget_usd':campaign['budget_total_usd'],'integration_status':'Unit economics and staged campaign plan are authoritative. The 1981–1983 sales/ROI reassessment now includes explicit paid upgrade cohorts, Team subsidy and the $253000 NCC provision. Capacity and programme costs remain planning allowances; see generated/catalogs/sales-reassessment-inputs.json.','source_sha256':{n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in ['generated/models/manufacturing-costs.json','generated/models/pricing-results.json','generated/catalogs/ncc-1982-inputs.json','generated/catalogs/ncc-1982-campaign.json','generated/catalogs/team-development-program.json']}}
# Exclude embedded reviews from the cost-input digest to avoid a self-reference.
review['source_sha256']['generated/models/manufacturing-costs.json']=hashlib.sha256(json.dumps({k:v for k,v in load('generated/models/manufacturing-costs.json').items() if k!='reviews'},sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
review['source_hash_scopes']={'generated/models/manufacturing-costs.json':'canonical_json_without_reviews'}
cost_model=load('generated/models/manufacturing-costs.json');cost_model.setdefault('reviews',{})['ncc-1982']=review;save('generated/models/manufacturing-costs.json',cost_model)
# The timeline and Navigator consume the campaign and merged review data.
print('Updated embedded NCC review.')
