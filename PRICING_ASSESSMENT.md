# Retail pricing: balanced contribution and proxy discount

The active policy covers all 82 offers and 218 available annual snapshots for 1978–1981. Let P be retail price, C recurring cost, f the dealer fee and B the normalized competitor proxy. Match contribution margin on net receipts, 1 − C/[P(1 − f)], to proxy discount, 1 − P/B. Therefore **P = sqrt(C × B / (1 − f))**, rounded to cents. These percentages describe unit contribution before corporate overhead, development, marketing, capital, tax and finance; they are not corporate net profit.

170 snapshots match to within 0.02 percentage points before display rounding. For 46 snapshots without a proxy, use a disclosed 25% contribution margin on net receipts; no competitor discount is claimed. Two second-generation monochrome-monitor snapshots (1980 and 1981) cannot match while avoiding a unit loss: use rounded-up break-even prices and disclose the premium above the proxy. Stress losses remain visible. Fees and manufacturing assumptions are unchanged.

Course promotions balance contribution after reserving the entire voucher. Composite bundles use their own normalized proxies and exact component costs; matching may make a bundle dearer than buying components separately, which is disclosed rather than hidden by an incompatible discount cap.

This policy supersedes the earlier 40% dollar-contribution reduction. Both immutable baseline files remain unchanged for audit and demand comparisons. The price ratio feeds the existing sales elasticity model; no uncalibrated feature or marketing uplift is added. Manufacturing capacity supplies modeled full demand plus 10% reserve; ROI uses the resulting staffing, inventory, capex and marketing requirements. The Sales page retains its dated delivery caps, so its totals differ from the full-supply investment/ROI scenario and its end-1980 extension.

The main Retail pricing table can be resized in both dimensions using its bottom-right corner, with internal scrolling and sticky headings. Filters preserve the chosen dimensions. Print layout expands the table normally.

Rebuild in order: `python tools/build_pricing.py`, `python tools/build_sales.py`, `python tools/build_investment_model.py`, `python tools/build_roi.py`. Rebuild manufacturing costs first only if their inputs change. Preserve frozen baselines. Pricing results contain source hashes, cost bridges and per-snapshot balance status.

## Evidence and limitations

Sources are original June 1978, 1979, 1980 and 1981 BYTE advertisements, plus a 1980 Apple prospectus (used only in the 1981 assessment) and older engineering-course listings. URLs, observation prices and PDF page numbers are in `competitor_evidence` and `sources`. June issue dates are contemporary evidence, not claims to know exact transactions on June 15.

Observed prices are separate from normalized baskets. Match limitations include display type, memory, drive count/capacity, OS, software licenses and dealer services. Mail-order discounts are considered; higher list prices are not automatically selected to manufacture an apparent advantage. No IBM PC or post-cutoff network prices are backdated.

1978/1979 spreadsheets have no verified shipping direct equivalent in this research. ERA workstations have no exact historical equivalent. SDKs, standalone keyboards, support, courses and networking have weak or absent matching price evidence. Their estimates are scenario judgments, not competitor quotations. The numerical discount against such a basket is indicative only. Historical research is a sample of period offerings, not an exhaustive market census.

Particularly difficult targets: custom monitors versus inexpensive commodity displays; large early DRAM banks; the dedicated-RAM CP/M module versus a SoftCard sharing host memory. Two monitor snapshots require break-even prices above their proxies; these exceptions are disclosed.

## Cost and profit boundaries

Costs reference the existing manufacturing model, with SHA-256 provenance. Commodity and internal-chip BOM, workforce, energy, consumables, recurring overhead, yield/rework, instructions, packaging, freight, recurring royalties and modeled included support remain included. No cost-model input was changed to make a target price work.

Profit = retail − ComputerLand fee − recurring manufacturing/delivery cost. It is **unit contribution**, not corporate net profit: R&D, capital investment/depreciation, software development, marketing/promotion, financing and taxes remain excluded. Actual warranty-loss provisions beyond modeled support would need a separate operating budget.

Bundles sum their exact component cost records. OS, keyboard, monitor and first-year support already in base systems are counted once. The 1981 Artemis base-system cost already includes the NIC and Server edition; no second network upgrade is charged. Office productivity switches from native Abacus 2 to Abacus 3 after 1980-11-19. The network installation adds three explicit $15 cable allowances (range $10–25); installation, training and backup media are not included.

BPI five-application suite uses the consolidated suite media cost, not five individually packaged application costs. The new client entitlement conservatively uses the existing full client-edition delivery estimate rather than inventing a cheap media/license split. Proposed BPI entitlements are one server package plus separately licensed clients, with final legal terms still to define.

Services retain their cost-model workload assumptions. On-site support is priced as a capped eight-hour engagement, not unlimited annual cover. Customer-site training is one two-day class for up to eight people: the per-learner cost is multiplied by eight, with travel billed additionally at cost. BPI and Pulse training assume three and two days respectively. These scope limits need to accompany any actual sale.

The four before-you-buy Academy variants are repriced separately against the same course proxy, balancing contribution after full voucher redemption. Fundamentals retains a credit of half tuition; other courses retain a $150 credit. This replaces a fixed tuition surcharge. Credits are reserved once in marketing, not also in manufacturing. The detail panel shows the full exposure.

## Validation

```
python tests/validate_pricing.py
node tests/pricing.test.cjs
node tests/atlas.test.cjs
```

Checks cover full product coverage, date gating, source chronology, exact cost reconciliation, mathematical fee/profit identities, the margin floor, stress cases, edition changes, no duplicated NICs, training units, grouped matrix, scenario controls, availability filters and site links.



The three NCC 1979 cards are included in the pricing matrix. Their new retail values are cost-floor planning proposals without a matched historical competitor benchmark. They do not overwrite a quoted catalog price. Host computer, compatible monitor and separate FlexiBUS/video cards are not bundled implicitly. Costs use AION launch silicon; SMC sensitivity is separate.


External Tandy Model II hardware, its CP/M distribution and the Abacus partner edition have no agreed OEM prices or licensing volumes. They are represented in the technical catalog, but excluded from the 82 Logix/AION retail offers; the existing Abacus Aurelia price is not silently reused as a Tandy license price.
