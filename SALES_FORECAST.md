# Aurelia sales under revised pricing

This is a scenario forecast, not recorded sales or a new canonical story outcome. The current horizon is May 18, 1980; see [SALES_NCC1980.md](SALES_NCC1980.md) for the COMDEX-to-NCC extension and Academy demand. Earlier sections retain their explicitly named historical forecast periods. View [Logix computer demand and sales](sales.html), the machine-readable [forecast](sales_forecast.json) and [retail pricing](pricing.html).

## Price policy

Retain 60% of each offer's baseline dollar contribution after its baseline channel fee and recurring cost. Apply to all 82 offers and 218 available annual snapshots, including course variants before promotional credit. The frozen original `pricing_baseline.json` and separate `compatibility_pricing_baseline.json` for the three new COMDEX offers prevent repeated reductions on rebuild. Profit here excludes marketing, development, capital, financing and taxes.

1978 examples:

| Offer | Previous | Revised |
|---|---:|---:|
| Aurelia grayscale system | $2,109 | $1,664.69 |
| Aurelia colour system | $2,329 | $1,851.65 |
| Office bundle | $2,199 | $1,732.51 |
| Office bundle + disk | $2,598 | $2,070.78 |
| Office bundle + disk + printer | $3,057 | $2,462.71 |
| Fundamentals tuition | $199 | $138.38 |
| Fundamentals purchase credit | $99.50 | $69.19 |

The complete package is approximately 19.44% cheaper. It does not receive a 40% price discount. The main system margins become roughly 39–40%; reducing profit dollars by 40% is not the earlier hypothetical 30% margin policy.

## Forecast and periods

Central forecast: **10,750 US customer computer purchases during calendar 1978**, and **29,400 during June 1978–May 1979**, a rounded proxy for sales by NCC on June 4, 1979. June 1–3 is omitted, not silently included in May. The earlier 22,000 launch-year baseline is a planning estimate, not observed demand. January–May 1978 sales are zero.

Demand = 22,000 × (new complete-package price / old price)^(-elasticity), rounded to 1,000 and capped by scenario delivery capacity. Conservative / central / strong elasticities are 0.8 / 1.5 / 2.0, yielding 26,000 / 30,000 / 34,000 before incremental named-event adjustments. The resulting forecasts are 23,945 / 29,400 / 34,000, roughly 24,000–34,000. These are judgement scenarios, not confidence intervals. The ramp is an operational planning allocation, not a claim about measured seasonality.

Calendar-1978 baseline market is assumed to be 180,000 US units; the launch-year baseline is 250,000. Neither number is presented as a verified historical count. Add new/accelerated Logix purchases and competitor halo purchases to the relevant denominator. Diverted purchases change shares without expanding the market. Do not compare calendar sales with a launch-year denominator.

Central case: 60% of Logix purchases are new or accelerated. Including Apple-transferred buyers preserves competitor halo of 1,150 in 1978 and 5,080 over the launch year. Expanded markets are 187,600 and 272,720; Logix shares are **5.73%** and **10.78%**, respectively. Launch-year expansion is **9.09%**. These denominators and buyer splits are assumptions, not measured historical outcomes.

## Revenue and operating capacity

Average purchase mix: 80% Office grayscale bundle; 20% colour system plus Business Tools and Abacus; one disk per computer and printers with 70% of purchases. All sales assume a 25% dealer fee; direct sales are not assigned extra profit. Customer spending, supplier receipts after channel fees and contribution are separate. Supplier receipts combine the Logix/AION offer without allocating legal-entity revenue. Academy tuition and independent BPI licence receipts are excluded from these totals. BPI first-purchase receipts appear in a separate section; no BPI corporate profit or Adam equity income is inferred.

Monthly central deliveries rise to 4,920 in May 1979. Production must additionally supply demonstration, service and inventory needs. Existing costs assume a 10,000-unit annual family scale; holding those costs fixed is a scenario convention, not proof of capacity or automatic economies of scale. TV material has no guaranteed airtime.

Academy central roadmap: five launch centres, 8–10 by December 1978, 14–18 by NCC 1979; 40–45 teaching rooms, 50–56 instructors, 10,000–13,000 first-year course enrolments. This requires early recruiting and eight-learner rooms, with dealer-hosted classes bridging geographic gaps. Expand against sustained occupancy/waiting lists. Enrolments can include repeat students; they are not additional computer sales. Locations and openings remain proposals.

## Rebuild and verification

Run costs, pricing, then `python tools/build_sales.py`. The forecast records the pricing-file hash. Validate with `python tests/validate_sales.py`; shared-navigation and scenario-rendering checks are in the interface test suites. Pricing baseline changes require explicit review.


## Named competitor and partner effects

`market_reactions.json` supplies incremental central adjustments: Apple −1,800; late-May Tandy deferral −150; compatibility confidence +150; stronger BPI execution +1,200. Total 29,400 versus the pre-reaction 30,000 and prior 28,200. Calendar 1978 rises from 10,350 to 10,750. BPI already existed in the baseline, so only improved promotion and implementation support create incremental demand. Central BPI gains by month, June–May: 0, 20, 40, 60, 80, 100, 100, 100, 120, 160, 200, 220. The effect is deliberately gradual and zero in the launch month.

Conservative BPI gain is 600. Strong demand gain is 1,800, but only 945 fits the 34,000-unit delivery cap; 855 is deferred beyond the cutoff. No capacity increase is silently assumed. All these effects are judgement scenarios, not measured conversions.

Confidential late-1978 talks do not move public demand immediately. Model II and Abacus customer release is October 1979; no such unit or OEM revenue appears before NCC. The June demonstration, later Apple product review and IBM’s post-cutoff confidential OS problems generate no earlier sales. See [COMPETITOR_REACTIONS.md](COMPETITOR_REACTIONS.md). Values are rough judgement assumptions, not measured effects; future partner-volume estimates remain open.


## Independent BPI purchases

First-purchase attachment is 15% / 20% / 25% across scenarios. Cohorts are mutually exclusive: 50% buy accounting only, 25% four trading modules and 25% the complete suite, rounded by month. The central case has 2,150 BPI customer installations in 1978 and 5,880 through May 1979. Those customers are already included in computer units. Across the full period: 8,820 individual module licences and 1,470 suite licences; a suite is one entitlement for five modules.

Central BPI customer spending is $1,504,427.40; BPI receipts after the assumed 25% channel fee are $1,128,320.55. These are independent BPI receipts, not Logix/AION or Adam income. Software development, specialist support, marketing, setup, taxes and upgrade redemptions are not estimated, so this is not a profit forecast. No additional post-purchase upgrade revenue is counted; upgrade credits require a separate cohort model if introduced later.

BPI courses consume part of the existing 10,000–13,000 Academy enrolment plan. Each launch centre needs access to a BPI specialist; dealer qualification and paid setup capacity constrain adoption. Course completion does not create an extra computer sale. Detailed commitments and deployment gates are in BPI_PARTNER_STRATEGY.md.


## NCC 1979 campaign boundary

The original May 31 forecast remains unchanged. A separate June–November extension now models the accepted campaign in `ncc_1979_campaign.json`. Confidential preparation and later milestones are not applied retroactively. The ten-year $100 outlook is not a price or retirement input.

## June–November 1979 extension

The canonical Aurelia+ premiere is **December 3, 1979**, not November. Projection stops November 30 and contains no Aurelia+ sales, Pulse or Abacus 2.0 sales. It does not give buyers advance knowledge of unannounced successor details.

| Scenario | New demand, June–November | Deliveries, June–November | Sales, January–November 1979 | Cumulative since launch | Unmet demand at November end |
|---|---:|---:|---:|---:|---:|
| Conservative | 25,792 | 25,792 | 40,701 | 49,737 | 0 |
| Central | 40,282 | 37,500 | 56,150 | 66,900 | 1,334 |
| Strong | 53,518 | 43,800 | 65,336 | 77,800 | 5,612 |

These are conditional scenarios, not confidence intervals. New demand excludes returning unmet demand. The strong case starts June with 855 previously deferred BPI-related purchase intentions. Of unmet demand, 75% retries next month and 25% lapses; central attrition totals 1,448 through November. No demand is counted twice as a new buyer or as a completed sale.

### June price change

The complete Office/disk/printer package falls from **$2,462.71 to $2,117.95 (14.00%)**. Office/disk falls from $2,070.78 to $1,725.57. This is the 1979 annual snapshot change, separate from the already modelled contribution-policy reduction. No second 40% reduction is applied.

The June 15 snapshots are used as proxies for a June 4 NCC price change, an explicit assumption because the annual pricing data does not establish an exact effective date. June blends three days at old prices and 27 at new prices for both demand response and receipts. July–November use 1979 prices. Ceteris paribus, the package cut increases full-month demand by about 12.8% / 25.4% / 35.2% under elasticities 0.8 / 1.5 / 2.0. Actual deliveries can remain capacity-limited.

### Demand and offering assessment

Each scenario starts from its May delivered run rate, preserving existing Abacus, BPI, dealer, Academy and advertising effects. Modest monthly maturation/autumn factors are explicit assumptions. Incremental campaign, BPI execution and ecosystem confidence gains are additive against price-adjusted demand. They are separate from additional Apple substitution, Tandy waiting/substitution and migration hesitation. Full input arrays and scenario scaling are in `post_ncc_policy` and `tools/extend_sales.py`.

NCC demonstrations and July roadshows build awareness and developer confidence. Independent BPI deployment support helps convert business buyers; existing BPI availability is not counted again. Third-party peripherals improve usefulness without becoming Logix product revenue. October's qualified Tandy release increases competitive substitution. Optional video and Apple native cards can strengthen competitors as well as the ecosystem. No unsigned OEM target is treated as a delivered machine. Future architecture details remain secret; the migration message promises C source support and a planned qualified Z80 legacy option, not native binary continuity.

### Delivery and financial implications

Central monthly deliveries are 5,400 / 5,700 / 6,000 / 6,400 / 6,800 / 7,200, June through November. The corresponding new demand is 6,103 / 6,200 / 6,449 / 6,895 / 7,174 / 7,461. Raising November capacity to 7,200 requires about 46% more customer deliveries than May, plus inventory and service stock. These ceilings require factory, disk/printer supply, working capital, dealer and support plans; they are not established manufacturing capacity. The cost snapshots are retained without speculative volume savings.

June–November central customer package spending is **$76.99m**, supplier receipts after channel fees **$57.74m**, and recurring contribution **$16.28m**. Contribution excludes campaign, support expansion, Academy, R&D, financing and tax; it is not net profit. Independent BPI adds 7,500 customer installations and **$1.44m** after-channel receipts, excluded from Logix/AION totals. The original attachment rates and mutually exclusive cohorts remain; June price blending also applies to BPI.

This remains a computer-led package forecast. Other vendors' compatible machines, standalone cards/software, third-party peripherals, OEM royalties and Academy revenue are not quantified. Extended-period market share is withheld because no new market denominator has been calibrated. The main central-case constraint is delivery capacity, so extra marketing demand does not automatically create more sales.

Rebuild with `python tools/build_sales.py`; validate period arithmetic, pricing transitions and demand conservation with `tests/validate_sales_extension.py`. The page shows monthly demand, capacity, sales, unmet demand and price/campaign/competition components for each scenario.

The December 3 manufacturer compatibility kit and clone-enablement policy occur after this forecast cutoff. They change neither November Aurelia demand nor shipments. The NCC 1980 extension now includes a clone-substitution sensitivity and application purchases; OEM volumes and kit/support revenue remain unquantified.
