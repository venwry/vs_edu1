"""Explicit post-launch scenario assumptions; no empirical conversion claim."""
import json, hashlib

def extend_comdex80(m, offers, root):
    fields={'customer_retail_spend_usd':'retail_price_usd','supplier_revenue_after_channel_usd':'revenue_after_fee_usd','recurring_cost_usd':'manufacturing_cost_usd','unit_contribution_total_usd':'unit_profit_usd'}
    def snap(r,y):return offers[r]['snapshots'][str(y)]
    parts={'aurelia':[(x['product_ref'],x['quantity_per_computer']) for x in m['average_sale']['components']], 'aurelia_plus':[(x['product_ref'],x['quantity']) for x in m['ncc1980_policy']['plus_components']], 'artemis':[('bundle.proposed_artemis_office',.70),('bundle.proposed_artemis_developer',.15),('bundle.proposed_artemis_migration',.15),('device.flexidisk',1),('device.flexiprint40',.7)]}
    revision=json.loads((root/'artemis_display_revision.json').read_text())
    mix=revision['mono_pro_artemis_bundle_share']
    parts['artemis']=[(r,q*(1-mix)) for r,q in parts['artemis'] if r.startswith('bundle.')] + [(r+'_mono_pro',q*mix) for r,q in parts['artemis'] if r.startswith('bundle.')] + [(r,q) for r,q in parts['artemis'] if not r.startswith('bundle.')]
    def basket(kind,year):
        return {f:round(sum(snap(r,year)[f]*q for r,q in parts[kind]),2) for f in fields.values()}
    averages={str(y):{k:basket(k,y) for k in parts if y==1980 or k=='aurelia'} for y in [1979,1980]}
    old=m['ncc1980_policy']['average_sale_by_computer']
    m['metadata'].update(title='Logix computer sales through COMDEX 1980',ncc1980_forecast_end='1980-05-18',forecast_end='1980-11-18',comdex1980_date='1980-11-19',source_ncc1980_campaign_sha256=hashlib.sha256((root/'ncc_1980_campaign.json').read_bytes()).hexdigest())
    policy={'period':'May 19–November 18, 1980 inclusive. May has 13/31 exposure; November 18/30. Earlier campaign boundaries are preserved; revised source costs/prices propagate on rebuild. COMDEX launch-day Abacus 3/Pulse 3 revenue is excluded.', 'baseline':'April 1980 pre-price-response demand, from the prior model, is the full-month anchor. Apply run-rate growth and net campaign/competition effect once; then divide one buyer pool between all three computers. Artemis substitution is not added again as extra demand.', 'run_rate_factors':[1.05,1.08,1.10,1.12,1.16,1.20,1.22], 'net_campaign_rate':{'conservative':.01,'central':.07,'strong':.12}, 'net_effect':'Judgement net uplift for launch/dealer confidence after competition and migration hesitation; not measured conversion. No separate speed, Academy or year-2000 bonus.', 'artemis_preference_shares':[.12,.18,.23,.28,.33,.37,.40], 'aurelia_preference_shares':[.10,.09,.08,.07,.06,.05,.04], 'price_response':'Remaining intentions select Aurelia+. Each cohort responds to its package price relative to the prior Plus basket (old Aurelia uses its own basket). Premium-deterrence leaves the market; no automatic substitution. Existing products keep prior prices in May, then use June 1980 snapshots. Artemis May price is explicitly a provisional June-snapshot proxy. Price declines increase intentions according to the scenario elasticity, not by an additional marketing factor.', 'components':{k:[{'product_ref':r,'quantity':q} for r,q in v] for k,v in parts.items()},'average_sale_1980':averages['1980'], 'central_full_month_capacity':{'aurelia':[900,800,700,600,500,400,300],'aurelia_plus':[8500,8800,9000,9200,9400,9600,9800],'artemis':[600,1100,1800,2600,3500,4500,5500]},'capacity_scale':{'conservative':.75,'central':1,'strong':1.2},'capacity':'Assumed deliveries, not proven production capacity. Separate Artemis ramp and model queues; 75% retry and 25% lapse at each reporting-period transition, including the split May transition. No reallocation between models.', 'accounting':'Computer package receipts combine Logix/AION after channel fees; contribution excludes overhead, campaign, compatibility maintenance, R&D, tax and financing. BPI is independent and excluded. Migration bundle already contains the compatibility card: never attach it again. Native Abacus 2 is included in Office/Migration bundles. Standalone upgrades, extra Pulse licences, SDK subscriptions and Academy tuition are excluded from this extension rather than treated as zero-demand products.', 'limits':'US planning scenarios, not orders or market-share estimates. Academy numerical horizon remains May 18; post-launch training is a campaign activity without a new enrolment projection. No COMDEX 1980 launch-day software receipts.'}
    policy['display_revision_summary']=revision['demand_basis']+' Incremental campaign budget: $435,000 in 1980; conservative/central/strong intent uplift 6%/12%/18%. Higher prices can offset greater interest. Historical delivery ramp and expanded-capacity ROI case remain separate.'
    policy['display_revision']=revision
    policy['display_revision_sha256']=hashlib.sha256((root/'artemis_display_revision.json').read_bytes()).hexdigest()
    m['comdex1980_policy']=policy
    def total(rows):return {'units':sum(r['units'] for r in rows),**{k:round(sum(r[k] for r in rows),2) for k in fields}}
    for s in m['scenarios']:
        queues={k:(s['comdex_to_ncc1980_months'][-1]['products'][k]['unmet_demand_units'] if k!='artemis' else 0) for k in parts}
        cumulative=s['launch_through_ncc1980']['units'];rows=[]
        anchor=s['comdex_to_ncc1980_months'][-2];anchor_demand=anchor['new_demand_units']+anchor['plus_price_deferred_units']
        for i in range(7):
            month=f'1980-{i+5:02}';fraction=13/31 if i==0 else 18/30 if i==6 else 1
            base=round(anchor_demand*policy['run_rate_factors'][i]*fraction);uplift=round(base*policy['net_campaign_rate'][s['id']]);pool=base+uplift
            intents={'aurelia':round(pool*policy['aurelia_preference_shares'][i]),'artemis':round(pool*policy['artemis_preference_shares'][i])};intents['aurelia_plus']=pool-sum(intents.values())
            display_increment=round(intents['artemis']*revision['demand_uplift'][s['id']])
            intents['artemis']+=display_increment;pool+=display_increment
            products={}
            for k in parts:
                avg=old[k] if i==0 and k!='artemis' else averages['1980'][k]
                reference=old['aurelia' if k=='aurelia' else 'aurelia_plus']['retail_price_usd']
                fresh=round(intents[k]*(avg['retail_price_usd']/reference)**(-s['elasticity_assumption']))
                opening=queues[k];retry=round(opening*.75);cap=round(policy['central_full_month_capacity'][k][i]*policy['capacity_scale'][s['id']]*fraction);n=min(fresh+retry,cap);queues[k]=fresh+retry-n
                products[k]={'intending_buyers':intents[k],'price_response_delta_units':fresh-intents[k],'new_demand_units':fresh,'opening_unmet_units':opening,'returning_demand_units':retry,'lapsed_demand_units':opening-retry,'delivery_capacity_units':cap,'units':n,'unmet_demand_units':queues[k],**{f:round(n*avg[v],2) for f,v in fields.items()}}
            n=sum(x['units'] for x in products.values());cumulative+=n
            installs=round(n*s['bpi_attachment_rate']);four=round(installs*.25);suite=round(installs*.25);single=installs-four-suite;y=1979 if i==0 else 1980
            spend=round(single*snap('software.bpi_suite.bpi_general_accounting',y)['retail_price_usd']+four*sum(snap('software.bpi_suite.'+a,y)['retail_price_usd'] for a in ['bpi_general_accounting','bpi_accounts_receivable','bpi_accounts_payable','bpi_inventory_control'])+suite*snap('software.bpi_suite',y)['retail_price_usd'],2)
            rows.append({'month':month,'period_start':month+('-19' if i==0 else '-01'),'period_end':month+('-18' if i==6 else '-30' if i in [1,4] else '-31'),'month_fraction':fraction,'baseline_demand_units':base,'net_campaign_demand_units':uplift,'display_revision_intent_increment':display_increment,'buyer_pool_before_price_response':pool,'products':products,'new_demand_units':sum(x['new_demand_units'] for x in products.values()),'units':n,'cumulative_units':cumulative,'unmet_demand_units':sum(queues.values()),'bpi':{'customer_installations':installs,'retail_spend_usd':spend,'bpi_receipts_after_channel_usd':round(spend*.75,2)},**{f:round(sum(x[f] for x in products.values()),2) for f in fields}})
        s['ncc_to_comdex1980_months']=rows
        a=total(rows);a.update({k+'_units':sum(r['products'][k]['units'] for r in rows) for k in parts});a.update(ending_unmet_units=sum(queues.values()),new_demand_units=sum(r['new_demand_units'] for r in rows),bpi_receipts_usd=round(sum(r['bpi']['bpi_receipts_after_channel_usd'] for r in rows),2))
        s['ncc_to_comdex1980']=a
        prior=s['launch_through_ncc1980'];s['launch_through_comdex1980']={'units':cumulative,**{k+'_units':prior.get(k+'_units',0)+a[k+'_units'] for k in parts},**{f:round(prior[f]+a[f],2) for f in fields}}
        s['calendar_1980_to_comdex']={k:round(s['calendar_1980_to_ncc'][k]+a[k],2) for k in ['units',*fields]}
