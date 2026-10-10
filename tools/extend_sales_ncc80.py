"""Conditional COMDEX-to-NCC sales and Academy capacity forecasts, not actual orders."""
import calendar
import hashlib
import json
import math


def extend_ncc80(model, offers, root):
    def load(n): return json.loads((root/n).read_text())
    story=load('logix_aion_story.json')
    events={e['id']:e for p in story['phases'] for e in p['events']}
    assert events['event.artemis_launch']['date']['start']=='1980-05-19'
    model['metadata'].update(title='Logix computer sales and Academy demand through NCC 1980',forecast_end='1980-05-18',november_forecast_end='1979-11-30',ncc1980_date='1980-05-19',source_comdex_campaign_sha256=hashlib.sha256((root/'comdex_1979_campaign.json').read_bytes()).hexdigest())
    periods=['1979-12','1980-01','1980-02','1980-03','1980-04','1980-05']
    keys=['retail_price_usd','manufacturing_cost_usd','computerland_fee_usd','revenue_after_fee_usd','unit_profit_usd']
    financial={'customer_retail_spend_usd':'retail_price_usd','supplier_revenue_after_channel_usd':'revenue_after_fee_usd','recurring_cost_usd':'manufacturing_cost_usd','unit_contribution_total_usd':'unit_profit_usd'}
    def snap(ref,year): return offers[ref]['snapshots'][str(year)]
    def basket(parts): return {k:round(sum(snap(r,y)[k]*q for r,q,y in parts),2) for k in keys}
    oldparts=[(x['product_ref'],x['quantity_per_computer'],1979) for x in model['average_sale']['components']]
    plusparts=[('bundle.proposed_aurelia_plus_office',.8,1980),('bundle.aurelia_plus_color',.2,1980),('software.business_tools_aurelia',.2,1979),('software.abacus_2',.2,1980),('device.flexidisk',1,1979),('device.flexiprint40',.7,1979)]
    avg={'aurelia':basket(oldparts),'aurelia_plus':basket(plusparts)}
    policy={
      'period':'1979-12-01 to 1980-05-18 inclusive; May 1–18 only, before the NCC launch',
      'price_basis':'Hold existing products at June 1979 prices and costs. New COMDEX products use their first available June 1980 snapshots as provisional launch-period price/cost proxies, not proof of December quotes. Do not apply a June 1980 price cut to existing products before NCC. Financial estimates require sensitivity review once launch quotes exist.',
      'average_sale_by_computer':avg,'plus_components':[{'product_ref':r,'quantity':q,'snapshot_year':y} for r,q,y in plusparts],
      'baseline':'Use November new demand, already including the June price response and NCC campaign. Add only incremental COMDEX/product/workshop effects. No new universal price cut or quantified speed claim.',
      'run_rate_factors':[1.08,.95,1.0,1.05,1.10,1.12],
      'central_incremental_rates':{'comdex_applications_gain':[.06,.08,.09,.08,.07,.06],'independent_compatibility_confidence_gain':[0,.005,.01,.015,.02,.025],'competition_loss':[.015,.02,.025,.03,.035,.04],'clone_substitution_loss':[0,.005,.01,.015,.02,.03],'migration_waiting_loss':[.01,.015,.02,.025,.04,.06]},
      'plus_preference_share':[.60,.70,.78,.82,.85,.88],
      'plus_price_response':'Preference shares precede price response. Apply (Plus average package / retained Aurelia average package)^(-scenario elasticity) to the Plus-intending cohort; the premium deters some purchases rather than silently assuming willingness to pay. COMDEX application gains already represent feature benefits; no extra quality multiplier. Existing-price Aurelia intentions are unchanged.',
      'central_full_month_delivery_capacity':[7800,8200,8600,9000,9400,9800],
      'central_full_month_plus_capacity':[4200,5600,6600,7400,8000,8600],
      'scenario_capacity_scale':{'conservative':.75,'central':1,'strong':1.2},
      'capacity':'Assumed net customer-delivery ceilings and product-specific ramp, not proven factory capacity. No model is forced to retire. Do not move unfilled old-model requests into Plus without modelling a buyer decision. Unused capacity is not a sale.',
      'timing':'December Plus demand/capacity exposure is 29/31 because launch is December 3. May demand and capacity are 18/31 of a month. Monthly rows are approximations, not dated individual orders.',
      'backlog':'75% of each model’s opening unmet demand retries; 25% lapses. November backlog opens as Aurelia demand. Separate product queues; no automatic substitution. Fresh demand plus returning demand equals deliveries plus ending unmet demand.',
      'competition':'Independent ports/clones gain gradually after kit availability; this is a substitution sensitivity, not named OEM shipment evidence. Other manufacturers’ systems and royalties remain outside Logix computer totals. No next-generation details or post-NCC hardware sales enter the forecast.',
      'application_upgrades':'Existing November Aurelia cohort only: monthly Abacus 2 full-licence purchase assumptions 2/2.5/2.5/2/1.5/1.5% before scenario scaling and partial-month exposure. No unapproved upgrade discount. These licences are separate from new-machine bundle licences; Pulse attached to new Aurelia+ systems only is reported separately.',
      'scope':'All forecasts are US scenario sell-through. Academy attendance is a consequence/channel interaction already reflected in demand, not another additive computer-sales uplift. No new market-share denominator or corporate-profit claim.'}
    model['ncc1980_policy']=policy
    def amounts(n,a): return {k:round(n*a[v],2) for k,v in financial.items()}
    def total(rows): return {'units':sum(r['units'] for r in rows),**{k:round(sum(r[k] for r in rows),2) for k in financial}}
    for sc in model['scenarios']:
        scale=model['post_ncc_policy']['scenario_scaling'][sc['id']];capscale=policy['scenario_capacity_scale'][sc['id']]
        queues={'aurelia':sc['june_november_1979']['ending_unmet_units'],'aurelia_plus':0}
        cumulative=sc['launch_through_november_1979']['units'];rows=[];cohort=cumulative;upgraded=0
        for i,month in enumerate(periods):
            fraction=18/31 if i==5 else 1;plus_exposure=29/31 if i==0 else 1
            base=round(sc['post_ncc_months'][-1]['new_demand_units']*policy['run_rate_factors'][i]*fraction)
            effects={k:round(base*v[i]*scale['positive' if k.endswith('gain') else 'negative']) for k,v in policy['central_incremental_rates'].items()}
            fresh=max(0,base+sum(v if k.endswith('gain') else -v for k,v in effects.items()))
            plus_intent=round(fresh*policy['plus_preference_share'][i]*plus_exposure)
            plus=round(plus_intent*(avg['aurelia_plus']['retail_price_usd']/avg['aurelia']['retail_price_usd'])**(-sc['elasticity_assumption']))
            price_deferred=plus_intent-plus;new={'aurelia':fresh-plus_intent,'aurelia_plus':plus};fresh=sum(new.values())
            fullcap=round(policy['central_full_month_delivery_capacity'][i]*capscale*fraction)
            pluscap=round(policy['central_full_month_plus_capacity'][i]*capscale*fraction*plus_exposure)
            caps={'aurelia':fullcap-pluscap,'aurelia_plus':pluscap};products={}
            for kind in queues:
                opening=queues[kind];retry=round(opening*.75);available=new[kind]+retry;units=min(available,caps[kind]);queues[kind]=available-units
                products[kind]={'new_demand_units':new[kind],'opening_unmet_units':opening,'returning_demand_units':retry,'lapsed_demand_units':opening-retry,'delivery_capacity_units':caps[kind],'units':units,'unmet_demand_units':queues[kind],**amounts(units,avg[kind])}
            units=sum(x['units'] for x in products.values());cumulative+=units
            rate=[.02,.025,.025,.02,.015,.015][i]*scale['positive']*fraction*plus_exposure
            upgrades=min(cohort-upgraded,round(cohort*rate));upgraded+=upgrades
            pulse=round(products['aurelia_plus']['units']*{'conservative':.1,'central':.2,'strong':.3}[sc['id']])
            apps={k:round(upgrades*snap('software.abacus_2',1980)[v]+pulse*snap('software.pulse_1',1980)[v],2) for k,v in financial.items()}
            count=round(units*sc['bpi_attachment_rate']);four=round(count*.25);suite=round(count*.25);single=count-four-suite
            bpi_spend=round(single*snap('software.bpi_suite.bpi_general_accounting',1979)['retail_price_usd']+four*sum(snap('software.bpi_suite.'+x,1979)['retail_price_usd'] for x in ['bpi_general_accounting','bpi_accounts_receivable','bpi_accounts_payable','bpi_inventory_control'])+suite*snap('software.bpi_suite',1979)['retail_price_usd'],2)
            row={'month':month,'period_end':month+('-18' if i==5 else '-'+str(calendar.monthrange(int(month[:4]),int(month[5:]))[1])),'month_fraction':fraction,'baseline_demand_units':base,'incremental_effects':effects,'new_demand_units':fresh,'plus_price_deferred_units':price_deferred,'products':products,'units':units,'cumulative_units':cumulative,'delivery_capacity_units':fullcap,'unmet_demand_units':sum(queues.values()),'applications':{'existing_aurelia_abacus2_licenses':upgrades,'pulse_licenses_on_new_aurelia_plus':pulse,**apps},'bpi':{'customer_installations':count,'retail_spend_usd':bpi_spend,'bpi_receipts_after_channel_usd':round(bpi_spend*.75,2)}}
            row.update({k:round(sum(x[k] for x in products.values()),2) for k in financial});rows.append(row)
        sc['comdex_to_ncc1980_months']=rows
        a=total(rows);a.update({kind+'_units':sum(r['products'][kind]['units'] for r in rows) for kind in queues})
        a.update(new_demand_units=sum(r['new_demand_units'] for r in rows),opening_unmet_units=sc['june_november_1979']['ending_unmet_units'],lapsed_demand_units=sum(p['lapsed_demand_units'] for r in rows for p in r['products'].values()),ending_unmet_units=sum(queues.values()),additional_application_receipts_usd=round(sum(r['applications']['supplier_revenue_after_channel_usd'] for r in rows),2),bpi_receipts_usd=round(sum(r['bpi']['bpi_receipts_after_channel_usd'] for r in rows),2),abacus2_existing_owner_licenses=upgraded,pulse_licenses=sum(r['applications']['pulse_licenses_on_new_aurelia_plus'] for r in rows))
        sc['comdex_to_ncc1980']=a
        sc['launch_through_ncc1980']={'units':cumulative,'aurelia_units':sc['launch_through_november_1979']['units']+a['aurelia_units'],'aurelia_plus_units':a['aurelia_plus_units'],**{k:round(sc['launch_through_november_1979'][k]+a[k],2) for k in financial}}
        sc['calendar_1979']=total(sc['months'][7:]+sc['post_ncc_months']+rows[:1]);sc['calendar_1980_to_ncc']=total(rows[1:])
    academy(model)


def academy(model):
    policy={'period':'June 1979–May 18, 1980; prospective demand/capacity extension of the original first-year roadmap',
      'unit':'Course enrolments, not unique people, graduations or additional computer purchases. Repeat attendance across courses/months is allowed; no unique-student count is inferred.',
      'drivers':'New-system customers, owners of the installed base, prospective buyers who do not buy in that month, and manufacturer/integrator learners. These are enrolment requests; no extra hardware conversion bonus is added.',
      'course_days':{'fundamentals':2,'fundamentals_abacus':5,'business_workflow':6,'developer':5,'bpi':3,'pulse':2},
      'course_mapping':'Use the existing 2/5/6/5-day courses; charts/layouts enter Abacus teaching after December 3. BPI uses 3-day and Pulse 2-day planning allowances already in the cost model. Manufacturer learners consume developer capacity; optional engineering subscriptions are not course enrolments.',
      'shares_before_comdex':{'fundamentals':.35,'fundamentals_abacus':.25,'business_workflow':.15,'developer':.10,'bpi':.15,'pulse':0},
      'shares_after_comdex':{'fundamentals':.25,'fundamentals_abacus':.30,'business_workflow':.10,'developer':.10,'bpi':.15,'pulse':.10},
      'central_centres':[16,16,17,18,19,20,22,23,24,25,26,27],
      'central_rooms':[42,44,46,48,50,52,56,60,64,68,70,72],
      'class_size':8,'target_seat_occupancy':.75,'teaching_days_per_room_month':18,'teaching_days_per_instructor_month':15,
      'staffing':'Plan 1.25 instructors per room, including specialist capability; room-days are capped by both rooms and instructors. Cross-trained BPI/Pulse teachers and geographic fit remain hiring/scheduling gates. Counts are aggregate capacity targets, not signed leases or named openings.',
      'capacity':'Plan classes at six occupied seats (75% of eight). Reserve whole class blocks by course duration; demand is allocated proportionally, then capped by requested places. May uses 18/31 of room/instructor days; December Pulse classes begin only after launch. No course starting too late to finish by cutoff is assumed.',
      'backlog':'75% of unmet enrolment requests retry the following period; 25% lapse. Capacity is measured in teaching days, so a five-day course consumes more than Fundamentals.',
      'accounting':'Tuition, support costs and purchase-credit redemption are not quantified here. Existing 50% Fundamentals credit and six-month expiry remain; other eligible course vouchers retain their terms. Student attendance is not a second computer purchase.',
      'previous_period':'The original 10,000–13,000 first-year enrolment target is retained, not presented as actual attendance. No historical enrolments are fabricated to reconcile it.'}
    model['academy_demand_policy']=policy
    for sc in model['scenarios']:
        factor={'conservative':.8,'central':1,'strong':1.2}[sc['id']];attach={'conservative':.18,'central':.23,'strong':.28}[sc['id']]
        installed=sc['launch_year']['units'];waiting=0;rows=[]
        for i,sales in enumerate(sc['post_ncc_months']+sc['comdex_to_ncc1980_months']):
            fraction=sales.get('month_fraction',1);post=i>=6
            owner_rate=.003 if not post else .0045
            drivers={'new_system_customers':round(sales['units']*attach),'existing_owners':round(installed*owner_rate*fraction),'prospective_buyers':round((180 if not post else 260)*factor*fraction),'manufacturer_integrator_learners':round(([0,0,0,0,0,0,30,45,60,75,90,105][i])*factor*fraction)}
            fresh=sum(drivers.values());opening=waiting;retry=round(opening*.75);available=fresh+retry
            rooms=round(policy['central_rooms'][i]*factor);centres=round(policy['central_centres'][i]*factor);instructors=math.ceil(rooms*1.25)
            days=math.floor(min(rooms*18,instructors*15)*fraction)
            shares=policy['shares_after_comdex' if post else 'shares_before_comdex'];requested={k:math.floor(available*v) for k,v in shares.items()};requested['fundamentals']+=available-sum(requested.values())
            weighted=sum(shares[k]*policy['course_days'][k] for k in shares);nominal_seats=days*6/weighted
            courses={};used_days=0;enrolled=0
            for k in shares:
                allocated_days=math.floor(days*shares[k]*policy['course_days'][k]/weighted)
                classes=min(math.floor(allocated_days/policy['course_days'][k]),math.ceil(requested[k]/6))
                places=min(requested[k],classes*6);teaching=classes*policy['course_days'][k]
                courses[k]={'requested_enrolments':requested[k],'enrolments':places,'classes':classes,'teaching_days':teaching};enrolled+=places;used_days+=teaching
            waiting=available-enrolled
            rows.append({'month':sales['month'],'month_fraction':fraction,'drivers':drivers,'new_requests':fresh,'opening_unmet_requests':opening,'returning_requests':retry,'lapsed_requests':opening-retry,'enrolments':enrolled,'unmet_requests':waiting,'centres':centres,'rooms':rooms,'instructors':instructors,'available_teaching_days':days,'scheduled_teaching_days':used_days,'courses':courses,'planning_seat_capacity':math.floor(nominal_seats)})
            installed+=sales['units']
        sc['academy_months']=rows
        def total(rr):return {'new_requests':sum(x['new_requests'] for x in rr),'enrolments':sum(x['enrolments'] for x in rr),'opening_unmet_requests':rr[0]['opening_unmet_requests'],'lapsed_requests':sum(x['lapsed_requests'] for x in rr),'ending_unmet_requests':rr[-1]['unmet_requests'],'course_enrolments':{k:sum(x['courses'][k]['enrolments'] for x in rr) for k in policy['course_days']}}
        sc['academy_to_ncc1980']=total(rows);sc['academy_comdex_to_ncc1980']=total(rows[6:])
