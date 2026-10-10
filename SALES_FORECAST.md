# Aurelia sales under revised pricing

This is a scenario forecast, not recorded sales or a new canonical story outcome. View [Sales 1978](sales.html), the machine-readable [forecast](sales_forecast.json) and [retail pricing](pricing.html).

## Price policy

Retain 60% of each offer's baseline dollar contribution after its baseline channel fee and recurring cost. Apply to all 79 offers and 212 available annual snapshots, including course variants before promotional credit. The frozen `pricing_baseline.json` prevents repeated reductions on rebuild. Profit here excludes marketing, development, capital, financing and taxes.

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

Central forecast: **10,600 US customer computer purchases during calendar 1978**, and **30,000 during June 1978–May 1979**, a rounded proxy for sales by NCC on June 4, 1979. June 1–3 is omitted, not silently included in May. The earlier 22,000 launch-year baseline is a planning estimate, not observed demand. January–May 1978 sales are zero.

Demand = 22,000 × (new complete-package price / old price)^(-elasticity), rounded to 1,000 and capped by scenario delivery capacity. Conservative / central / strong elasticities are 0.8 / 1.5 / 2.0, yielding 26,000 / 30,000 / 34,000 delivered systems under the selected capacity caps. These are judgement scenarios, not confidence intervals. The ramp is an operational planning allocation, not a claim about measured seasonality.

Calendar-1978 baseline market is assumed to be 180,000 US units; the launch-year baseline is 250,000. Neither number is presented as a verified historical count. Add new/accelerated Logix purchases and competitor halo purchases to the relevant denominator. Diverted purchases change shares without expanding the market. Do not compare calendar sales with a launch-year denominator.

Central case: 60% of Logix purchases are new or accelerated, with 1,000 competitor halo purchases in 1978 and 4,000 over the launch year. This gives about **5.66% calendar-1978 share** and **11.03% launch-year share**, with **8.8% launch-year market expansion**. Pulling later purchases forward is not permanent market creation.

## Revenue and operating capacity

Average purchase mix: 80% Office grayscale bundle; 20% colour system plus Business Tools and Abacus; one disk per computer and printers with 70% of purchases. All sales assume a 25% dealer fee; direct sales are not assigned extra profit. Customer spending, supplier receipts after channel fees and contribution are separate. Supplier receipts combine the Logix/AION offer without allocating legal-entity revenue. Academy tuition is excluded from these totals.

Monthly central deliveries rise to 5,200 in May 1979. Production must additionally supply demonstration, service and inventory needs. Existing costs assume a 10,000-unit annual family scale; holding those costs fixed is a scenario convention, not proof of capacity or automatic economies of scale. TV material has no guaranteed airtime.

Academy central roadmap: five launch centres, 8–10 by December 1978, 14–18 by NCC 1979; 40–45 teaching rooms, 50–56 instructors, 10,000–13,000 first-year course enrolments. This requires early recruiting and eight-learner rooms, with dealer-hosted classes bridging geographic gaps. Expand against sustained occupancy/waiting lists. Enrolments can include repeat students; they are not additional computer sales. Locations and openings remain proposals.

## Rebuild and verification

Run costs, pricing, then `python tools/build_sales.py`. The forecast records the pricing-file hash. Validate with `python tests/validate_sales.py`; shared-navigation and scenario-rendering checks are in the interface test suites. Pricing baseline changes require explicit review.
