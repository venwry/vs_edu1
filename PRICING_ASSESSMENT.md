# Active policy: proportional 40% contribution reduction

All 79 offers and 212 available 1978–1981 snapshots now retain 60% of their previous dollar contribution, with unchanged recurring cost and baseline fee. `pricing_baseline.json` pins the pre-change values from commit 3751194. New retail = (cost + 0.60 × previous contribution) / (1 − fee), rounded to cents. This is neither a 40% retail discount nor a fixed margin percentage. It is contribution before marketing, vouchers, R&D, capital and taxes, not net corporate profit.

The old competitor-discount target, price endings, minimum-margin floor and nonnegative stress guarantee below describe the baseline method, not current safeguards. Losses under stress are now shown explicitly. The displayed floor is cost break-even at the default channel fee. Course variants receive the same reduction before vouchers; the old $50 surcharge becomes $30 and Fundamentals retains its 50% tuition credit. Other course vouchers remain $150, even where full redemption produces a negative course-only contribution.

Rebuild in order: `python tools/build_cost_assessment.py`, `python tools/build_pricing.py`, `python tools/build_sales.py`. Do not overwrite the immutable baseline with revised results. Cost/channel changes require an explicit baseline review; the builder rejects silent drift.

See [Sales 1978](sales.html) and [SALES_FORECAST.md](SALES_FORECAST.md).

---

## Original baseline methodology (superseded where noted above)

# Retail pricing, June 15, 1978–1981

Open `pricing.html` through the same HTTP server as the Atlas. The navigation includes **Retail pricing**. The page reads `pricing_results.json`; regenerate it with `python tools/build_pricing.py`.

## Commercial scope

79 commercial purchase units across ten types: complete systems; application bundles; network installation bundles; peripherals and expansion; networking; software/developer tools; business applications; support; training; developer programs. There are 212 applicable annual snapshots.

Includes the original review list, seven Aurelia/Aurelia+ use-case bundles and seven Artemis/PRO packages. Existing hardware bundles are unchanged. The JSON is the consolidated pricing proposal; it does not rewrite historical price fields or technical compatibility contracts in the technical catalog.

No withdrawal date is established, so end dates are null (displayed as Open). Aurelia+ and Abacus/Pulse 2 introduced in December 1979 have no June 1979 price. Abacus/Pulse 3 introduced November 1980 have no June 1980 price. PRO server and office-network packages retain provisional prices, with announced/shipping-unconfirmed status; the Available products only filter excludes them.

## Pricing strategy

* Aim at 75% of the normalized competitor basket, where a defensible basket can be constructed.
* Keep at least 25% contribution on net revenue at ComputerLand's maximum 30% share. Floor = cost / (0.70 × 0.75) for dealer products.
* Use 25% ComputerLand share as the displayed baseline; 20% and 30% scenarios recalculate immediately. This interprets the catalog's 20–30% retailer margin as a share of retail price, not a markup on wholesale.
* Services are proposed as direct sales, fee zero; their floor is cost / 0.75. Developer registration includes its SDK.
* Round upward to retail endings and avoid annual increases unless the cost floor requires one. A composite bundle aims at a further 5% saving against separately offered constituents when component prices exist, subject to the floor.
* No matching quotation means no verified competitor-discount claim. Cost-based recommendations remain explicitly identified.

These floors approximately protect each **sold unit** against a simultaneous 10% markdown, 20% cost overrun and 30% channel fee. They do not protect unsold inventory, severe obsolescence or the entire high-cost envelope in the manufacturing model. The detail panel shows both the moderate stress case and markdown at the original high cost. The cost selector also exposes losses at unchanged retail prices.

## Evidence and limitations

Sources are original June 1978, 1979, 1980 and 1981 BYTE advertisements, plus a 1980 Apple prospectus (used only in the 1981 assessment) and older engineering-course listings. URLs, observation prices and PDF page numbers are in `competitor_evidence` and `sources`. June issue dates are contemporary evidence, not claims to know exact transactions on June 15.

Observed prices are separate from normalized baskets. Match limitations include display type, memory, drive count/capacity, OS, software licenses and dealer services. Mail-order discounts are considered; higher list prices are not automatically selected to manufacture an apparent advantage. No IBM PC or post-cutoff network prices are backdated.

1978/1979 spreadsheets have no verified shipping direct equivalent in this research. ERA workstations have no exact historical equivalent. SDKs, standalone keyboards, support, courses and networking have weak or absent matching price evidence. Their estimates are scenario judgments, not competitor quotations. The numerical discount against such a basket is indicative only. Historical research is a sample of period offerings, not an exhaustive market census.

Particularly difficult targets: custom monitors versus inexpensive commodity displays; large early DRAM banks; the dedicated-RAM CP/M module versus a SoftCard sharing host memory. Rows that miss 20% below their benchmark retain the cost-protecting price and a qualification.

## Cost and profit boundaries

Costs reference the existing manufacturing model, with SHA-256 provenance. Commodity and internal-chip BOM, workforce, energy, consumables, recurring overhead, yield/rework, instructions, packaging, freight, recurring royalties and modeled included support remain included. No cost-model input was changed to make a target price work.

Profit = retail − ComputerLand fee − recurring manufacturing/delivery cost. It is **unit contribution**, not corporate net profit: R&D, capital investment/depreciation, software development, marketing/promotion, financing and taxes remain excluded. Actual warranty-loss provisions beyond modeled support would need a separate operating budget.

Bundles sum their exact component cost records. OS, keyboard, monitor and first-year support already in base systems are counted once. The 1981 Artemis base-system cost already includes the NIC and Server edition; no second network upgrade is charged. Office productivity switches from native Abacus 2 to Abacus 3 after 1980-11-19. The network installation adds three explicit $15 cable allowances (range $10–25); installation, training and backup media are not included.

BPI five-application suite uses the consolidated suite media cost, not five individually packaged application costs. The new client entitlement conservatively uses the existing full client-edition delivery estimate rather than inventing a cheap media/license split. Proposed BPI entitlements are one server package plus separately licensed clients, with final legal terms still to define.

Services retain their cost-model workload assumptions. On-site support is priced as a capped eight-hour engagement, not unlimited annual cover. Customer-site training is one two-day class for up to eight people: the per-learner cost is multiplied by eight, with travel billed additionally at cost. BPI and Pulse training assume three and two days respectively. These scope limits need to accompany any actual sale.

The four regular Academy courses also show their before-you-buy variant: +$50 tuition. Standalone Fundamentals receives purchase credit equal to 50% of that tuition; the other three courses retain the existing $150 voucher. Fundamentals credit is valid six months toward one Aurelia, accepted by Academy centres and participating dealers reimbursed by Logix, without a purchase obligation. Maximum voucher exposure and fully reserved contribution are explicit. The voucher is promotional spend excluded from the main manufacturing-cost/profit columns, and must only be reserved once across the associated course and computer sale.

## Validation

```
python tests/validate_pricing.py
node tests/pricing.test.cjs
node tests/atlas.test.cjs
```

Checks cover full product coverage, date gating, source chronology, exact cost reconciliation, mathematical fee/profit identities, the margin floor, stress cases, edition changes, no duplicated NICs, training units, grouped matrix, scenario controls, availability filters and site links.



The three NCC 1979 cards are included in the pricing matrix. Their new retail values are cost-floor planning proposals without a matched historical competitor benchmark. They do not overwrite a quoted catalog price. Host computer, compatible monitor and separate FlexiBUS/video cards are not bundled implicitly. Costs use AION launch silicon; SMC sensitivity is separate.


External Tandy Model II hardware, its CP/M distribution and the Abacus partner edition have no agreed OEM prices or licensing volumes. They are represented in the technical catalog, but excluded from the 79 Logix/AION retail offers; the existing Abacus Aurelia price is not silently reused as a Tandy license price.
