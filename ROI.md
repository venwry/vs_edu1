# Quarterly ROI and marketing, 1974–1980

Open [Quarterly ROI](roi.html) in the shared Atlas navigation or home cards. It contains charts of revenue, operating costs, capex, marketing, quarterly/cumulative returns and cash recovery, plus a 28-quarter table and CSV export. Select a year or a low/central/high marketing budget.

## Files and regeneration

- `roi_1974_1980.json`: complete financial bridge, assumptions and source hashes.
- `marketing_budget_1974_1980.json`: itemized quarterly commercial, conference and marketing budget by company.
- `tools/build_roi.py`: calculation and static HTML generator.
- `tools/roi_template.html`: presentation, charts, filters and CSV export.

```sh
python tools/build_investment_model.py
python tools/build_roi.py
python tests/validate_investment.py
python tests/validate_roi.py
node tests/roi.test.cjs
node tests/atlas.test.cjs
```

The first two generators use Python 3.9+ standard library. The ROI execution smoke test uses Node standard library; the complete Atlas DOM suite requires its existing `jsdom` dependency. Regenerate the industrial report first when its sources or navigation change; regenerate ROI afterward. Do not hand-edit generated data or HTML.

## Interpretation

This is a pre-tax, unlevered **five-entity project ecosystem**, not a shareholder or legal consolidated return. Separate company ROI would require missing revenue-sharing, transfer-price, ownership and tax terms. Marketing costs still retain company attribution.

Revenue uses the **same full-demand quantities as the industrial investment plan**, with historical realized basket prices taken from the corresponding sales-forecast periods. The original capacity-limited forecasts are shown separately, not combined with expanded-demand costs. November 19–December 31, 1980 sales remain an explicit extrapolation. No extra Abacus 3/Pulse 3 sales or campaign-driven uplift is invented.

- Quarterly ROI: EBIT divided by average opening/closing operating assets (modeled net fixed assets including work in progress, plus inventory). This is a nonannualized, pre-tax ROIC proxy.
- Cumulative accounting ROI: cumulative EBIT divided by cumulative capex plus ending inventory. This is a custom since-inception measure, not an annual rate.
- Free cash flow: net revenue less cash operating costs, capex and inventory increase. Depreciation reduces EBIT only.
- Cumulative cash return: cumulative free cash flow divided by the peak external funding requirement to date. Startup operating losses are included; no terminal asset sale is assumed.

The source campaign budgets were unspecified. The new budget covers TV/print buying; commercial production and proposed talent rights; media agency work; conference venue/booth/staging/AV/filming/editing/travel/freight; station-copy dispatch; PR/mail/roadshows/dealer co-op; partner promotion; and expected Academy/BPI credits. All amounts are explicit planning allowances, not historical invoices or contracts. The proposed celebrity casting remains unconfirmed.

The financial bridge **replaces** the industrial model's generic campaign/dealer allowance with these items. It does not rewrite that baseline silently. Existing staff, engineering, Academy assets/teaching and product manuals remain funded once. Channel commissions are deducted before supplier revenue. Promotional credits reduce revenue once; internal DRI royalties/reimbursements are eliminated from ecosystem resource totals. Free station footage generates no licence revenue or guaranteed exposure.

Inventory follows the committed one-quarter-ahead funding plan: the 1980 year-end includes 1981 Q1 prebuild. This is a continuing-business view, not liquidation at December 31. There is no AR/AP schedule, debt/interest, income tax or terminal asset value. Fab depreciation begins after commissioning; other fixed-asset lives are disclosed scenario assumptions.

Marketing sensitivity changes only spending and expected credit redemptions (0.65× / 1× / 1.75×). It is not a causal marketing ROI calculation and does not substitute for demand, yield or BOM sensitivity.


## Artemis replaceable video and Mono Pro

See [ARTEMIS_VIDEO_CARD.md](ARTEMIS_VIDEO_CARD.md) for the 32 KiB card, dedicated 1 KiB sprite SRAM, four pixel-buffer pages, 640×400 Mono Pro, new complete offers and qualification limits. Costs, balanced pricing, demand, engineering, marketing, capacity and ROI are rebuilt together; [ROI](roi.html) includes the current before/after comparison.
