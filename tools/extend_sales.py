"""Explicit June–November 1979 scenario assumptions; preserves the earlier forecast."""
import hashlib
import json


def extend(model, offers, root):
    campaign = json.loads((root / 'ncc_1979_campaign.json').read_text())
    story = json.loads((root / 'logix_aion_story.json').read_text())
    launch = next(e for p in story['phases'] for e in p['events'] if e['id'] == 'event.plus_launch')['date']['start']
    model['metadata'].update(title='Logix computer demand and sales, 1978–November 1979', forecast_end='1979-11-30', aurelia_plus_launch=launch, source_campaign_sha256=hashlib.sha256((root / 'ncc_1979_campaign.json').read_bytes()).hexdigest())
    metrics = ['retail_price_usd', 'manufacturing_cost_usd', 'computerland_fee_usd', 'revenue_after_fee_usd', 'unit_profit_usd']
    mix = model['average_sale']['components']
    averages = {year: {key: round(sum(offers[x['product_ref']]['snapshots'][year][key] * x['quantity_per_computer'] for x in mix), 2) for key in metrics} for year in ['1978', '1979']}
    refs = model['pricing_comparison']['references']
    packages = {year: round(sum(offers[r]['snapshots'][year]['retail_price_usd'] for r in refs), 2) for year in ['1978', '1979']}
    policy = {
        'period': '1979-06-01 through 1979-11-30; no Aurelia+ deliveries before its canonical 1979-12-03 launch',
        'price_effective_date_assumption': '1979-06-04',
        'price_basis': 'Use June 15 annual pricing snapshots as proxies for NCC June 4 prices. June has 3/30 old-price and 27/30 new-price exposure, assuming uniform daily purchases. Later months use 1979 prices. This is an explicit timing assumption, not a new catalog price announcement.',
        'complete_package_1978_usd': packages['1978'], 'complete_package_1979_usd': packages['1979'],
        'complete_package_reduction_pct': round((1-packages['1979']/packages['1978'])*100, 2),
        'average_sale_by_price_year': averages,
        'baseline': 'Each scenario starts from its May delivered run rate, which already includes established Abacus, BPI, Academy, advertising and existing competition. Monthly factors model channel maturation and autumn buying. They are judgement inputs, not observed seasonality or a second launch-year price uplift.',
        'monthly_run_rate_factors': [1.02, 1.00, 1.02, 1.08, 1.14, 1.18],
        'central_effect_rates': {
            'campaign_gain': [.025, .035, .05, .06, .07, .08],
            'bpi_execution_gain': [.005, .01, .015, .02, .025, .03],
            'ecosystem_confidence_gain': [.005, .01, .015, .02, .03, .04],
            'apple_substitution': [.01, .015, .02, .025, .04, .05],
            'tandy_substitution_or_waiting': [.015, .02, .025, .03, .06, .07],
            'migration_uncertainty': [.02, .015, .01, .01, .005, .005]},
        'effect_boundaries': 'Rates are additive increments against price-adjusted demand, not measured conversions. Campaign covers NCC and July roadshows; BPI covers additional independent sales/support execution; ecosystem confidence covers interoperability and third-party peripheral availability. Existing benefits remain in the May base. Tandy waiting starts with its public demonstration; the October customer release increases substitution. Apple native cards may help competitors. No unsigned OEM contract, partner computer shipment, BPI Tandy port, IBM-delay windfall or future architecture detail is assumed.',
        'successor': 'No unannounced Aurelia+ specification, price or launch-date knowledge is assigned to 1979 buyers. Generic migration uncertainty is modelled; successor-announcement deferral would require a dated public event. November Aurelia+ sales are zero.',
        'backlog': 'Only explicitly tracked BPI capacity-deferred demand opens June. Each month 75% of prior unmet demand retries; 25% lapses. New demand plus retries is capped by delivery capacity; unmet demand is neither a sale nor a firm order. Other untracked pre-June lost demand is not invented.',
        'capacity_by_scenario': {'conservative': [4400, 4600, 4800, 5000, 5200, 5400], 'central': [5400, 5700, 6000, 6400, 6800, 7200], 'strong': [6200, 6600, 7000, 7500, 8000, 8500]},
        'capacity_status': 'Assumed net customer delivery ceilings, not funded production commitments. Central November capacity of 7,200 is 46% above May deliveries; factory, disks, printers, working capital, service stock and dealer readiness must support it. No automatic cost savings are taken.',
        'scenario_scaling': {'conservative': {'positive': .5, 'negative': 1.4}, 'central': {'positive': 1, 'negative': 1}, 'strong': {'positive': 1.4, 'negative': .7}},
        'market_scope': 'Forecast Logix Aurelia customer purchases only. Competing compatible computers and third-party peripherals are not Logix sales. OEM royalties, expansion-card sales to other installed bases, standalone software and Academy receipts remain unquantified; no extended-period market share is asserted without a new denominator.',
        'campaign_ref': 'ncc_1979_campaign.json', 'architecture_reveal': campaign['migration']['architecture_reveal']}
    model['post_ncc_policy'] = policy
    financial = {'customer_retail_spend_usd': 'retail_price_usd', 'supplier_revenue_after_channel_usd': 'revenue_after_fee_usd', 'recurring_cost_usd': 'manufacturing_cost_usd', 'unit_contribution_total_usd': 'unit_profit_usd'}
    def total(rows):
        result = {'units': sum(x['units'] for x in rows)}
        result.update({k: round(sum(x[k] for x in rows), 2) for k in financial})
        result['bpi'] = {k: round(sum(x['bpi'][k] for x in rows), 2) for k in rows[0]['bpi']}
        return result
    for sc in model['scenarios']:
        rows = []; cumulative = sc['launch_year']['units']; backlog = sc['reaction_components']['bpi_capacity_deferred']
        scale = policy['scenario_scaling'][sc['id']]
        for i, month in enumerate(['1979-06', '1979-07', '1979-08', '1979-09', '1979-10', '1979-11']):
            old_weight = .1 if i == 0 else 0
            price_factor = old_weight + (1-old_weight)*(packages['1979']/packages['1978'])**(-sc['elasticity_assumption'])
            base = round(sc['months'][-1]['units'] * policy['monthly_run_rate_factors'][i])
            priced = round(base*price_factor)
            effects = {k: round(priced*v[i]*scale['positive' if k.endswith('gain') else 'negative']) for k, v in policy['central_effect_rates'].items()}
            fresh = max(0, priced + sum(v if k.endswith('gain') else -v for k,v in effects.items()))
            opening = backlog; retry = round(opening*.75); lapsed = opening-retry
            available = fresh+retry; cap = policy['capacity_by_scenario'][sc['id']][i]; delivered = min(available, cap); backlog = available-delivered; cumulative += delivered
            average = {k: round(old_weight*averages['1978'][k]+(1-old_weight)*averages['1979'][k], 2) for k in metrics}
            row = {'month': month, 'baseline_demand_units': base, 'price_gain_units': priced-base, 'effects': effects, 'new_demand_units': fresh, 'opening_unmet_units': opening, 'returning_demand_units': retry, 'lapsed_demand_units': lapsed, 'demand_including_returning_units': available, 'delivery_capacity_units': cap, 'units': delivered, 'unmet_demand_units': backlog, 'cumulative_units': cumulative, 'aurelia_plus_units': 0, 'old_price_fraction': old_weight, 'average_sale': average}
            row.update({k: round(delivered*average[v], 2) for k,v in financial.items()})
            count = round(delivered*sc['bpi_attachment_rate']); four=round(count*.25); suite=round(count*.25); single=count-four-suite
            def price(ref):
                return old_weight*offers[ref]['snapshots']['1978']['retail_price_usd']+(1-old_weight)*offers[ref]['snapshots']['1979']['retail_price_usd']
            four_price = sum(price('software.bpi_suite.'+x) for x in ['bpi_general_accounting','bpi_accounts_receivable','bpi_accounts_payable','bpi_inventory_control'])
            spend=round(single*price('software.bpi_suite.bpi_general_accounting')+four*four_price+suite*price('software.bpi_suite'),2)
            row['bpi']={'customer_installations':count,'single_accounting_licenses':single,'four_module_customers':four,'complete_suite_licenses':suite,'individual_module_licenses':single+4*four,'retail_spend_usd':spend,'bpi_receipts_after_channel_usd':round(spend*.75,2)}
            rows.append(row)
        sc['post_ncc_months']=rows
        sc['june_november_1979']=total(rows)
        sc['june_november_1979'].update(new_demand_units=sum(x['new_demand_units'] for x in rows),opening_unmet_units=rows[0]['opening_unmet_units'],lapsed_demand_units=sum(x['lapsed_demand_units'] for x in rows),ending_unmet_units=rows[-1]['unmet_demand_units'])
        sc['calendar_1979_through_november']=total(sc['months'][7:]+rows)
        sc['launch_through_november_1979']=total(sc['months']+rows)
