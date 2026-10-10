# NCC 1979 consistency review

Scope: the narrative, event/phase/lane assignments, technical catalog and editions, 1978 and 1979 campaigns, competitor plans, manufacturing and pricing models, sales attribution, site data and validation suites. This is a cross-file scenario audit, not proof of engineering feasibility or a new exhaustive historical-source audit. All inconsistencies and material open decisions found in this review are listed below; unknown technical details are not presented as contradictions.

## Corrected inconsistencies and missing boundaries

| ID | Finding | Resolution |
|---|---|---|
| C01 | No consolidated NCC 1979 campaign expressed the accepted interoperability, migration and eight-bit commitments. | Added NCC_1979_CAMPAIGN.md, ncc_1979_campaign.json and eight dated timeline milestones. |
| C02 | A June coprocessor promise could conflict with the July event labelled “module developed”. | June is a planned legacy option; July 1 begins detailed implementation; the product remains introduced May 19, 1980. |
| C03 | “Executes Aurelia applications natively” could imply that the new host CPU executes Z80 instructions. | Catalog explicitly assigns execution to the Z80 guest and requires OS, memory and peripheral bridging. |
| C04 | The full portability framework is dated 1980, while the accepted campaign refers to an established C environment in 1979. | Existing Z80 C/API/file-format discipline is distinguished from the complete new-target framework introduced in 1980. |
| C05 | The author-facing catalog exposes architecture details that must remain secret publicly in 1979. | Explicit press-material disclosure boundary; public architecture/word-size reveal assigned to NCC 1980. Internal specifications remain intact. |
| C06 | A single “compatible” label could overstate binary, media, peripheral or video interchange. | Three independent profiles with ISA/resource, file/media, driver/class and monitor qualification requirements. |
| C07 | The technical catalog review scope still deferred pricing, sales and memory-bus work already assessed elsewhere; README also called pricing deferred. | Replaced stale deferrals with current assessment/qualification distinctions. |
| C08 | Manufacturing documentation listed 116 rows, 199 inputs and 148 quantity assumptions, omitting later cards. | Corrected to 119 rows, 221 component-cost entries and 166 quantity assumptions; annual priced counts 48/55/92/117. Costs themselves unchanged. |
| C09 | A ten-year $100 claim had no explicit configuration, money basis or lifecycle meaning. | Recorded as Adam's nominal-dollar forecast for a future TV/basic-storage computer; not a complete business system, guaranteed date or withdrawal instruction. |
| C10 | Manufacturer rankings and adoption goals could be mistaken for signed agreements or completed shipments. | Prospects remain assessments; end-1979 and NCC-1980 quantities are targets with distinct-OEM counting. No fictitious signed North Star/Vector products added. |
| C11 | New campaign exposure could be counted again in the existing pre-NCC sales forecast. | Explicit cutoff and overlap policy; June/October/1980 effects are excluded, May activity has no separately calibrated additional uplift. |
| C12 | Event-count documentation and validation assertions needed updating after new milestones. | Updated to 70 events; canonical event inventory and website lanes agree. Historical date-review tables are explicitly a review subset. |

## Remaining engineering, commercial and modelling decisions

| ID | Open item | Impact / required resolution |
|---|---|---|
| R01 | Governance and licensing | COMDEX now defines standard kit terms, royalty-free reference-runtime redistribution, optional AION certification and bounded support. Working-group governance, dispute/appeal procedure and final launch/extra-work fees remain open; no OEM contract is asserted. |
| R02 | Long-term CP/M support | No funded duration, staffing or end-of-support policy. “Years of future” cannot become a ten-year contractual support guarantee without these decisions. |
| R03 | Campaign and porting budget | OEM kits, reference engineering, workshops, venue/AV, roadshows, directory, joint media and migration clinics are unbudgeted. Unit-cost and contribution tables exclude them. |
| R04 | Public demonstration qualification | TPA/RAM budgets, large Abacus workloads, BPI export/import, cross-host document round trip and exact physical transfer route need measured acceptance. CP/M does not guarantee a common disk format or identical program binaries. |
| R05 | FlexiBUS electrical release | Connector/power sequencing, final controller integration, buffering, timing and fault tests remain incomplete. V1 is point-to-point and bounded in throughput, not a universal hot-plug/hub system. |
| R06 | Peripheral class protocols | Modem, plotter and specialist classes, richer printer features and their drivers are not fully specified. Device identification cannot substitute for them. |
| R07 | Storage and boot | Baseline card operation loads drivers from an existing boot disk. FlexiBUS boot needs qualified ROM; hard disks need flush/error semantics and throughput tests. Fast native controllers remain valid. |
| R08 | Display availability | Controller 80-column capability does not give existing 320-pixel monitors 80 columns. A qualified 640-pixel monitor, correct timings/readability and a named available configuration are required for any such demo. |
| R09 | Future home-TV configuration | Current professional digital-video output does not establish household-TV compatibility. The $100 forecast needs a later consumer output design, exact basic-storage inclusion and costed system definition. |
| R10 | Legacy module engineering | Guest ROM/banking, 64 KB local memory budget, mailbox/bridge, drivers and conformance remain to be implemented/qualified. Artemis PRO and every future model are not automatically covered. |
| R11 | Component sourcing | June cards use AION supply. October SMC availability is per qualified part; all chips/VRAM cannot be assumed released together. Supply allocations, warranty, yields and volumes remain gates. |
| R12 | OEM and peripheral adoption | Except existing named story agreements, prospects remain unsigned and peripheral products unnamed/unqualified. Targets require agreements and actual evidence before being converted to shipment events or forecast revenue. |
| R13 | Capacity versus demand | The sales model caps demand but does not establish a factory/staffing/working-capital plan. Recurring costs use 10,000 units per family while central first-year sales reach 29,400. This is an explicit modelling assumption, not proven scale economics. |
| R14 | Post-NCC sales model | June–November 1979 now has a separate price/campaign/substitution and capacity model. Compatible-machine volumes, OEM royalties and a new market-share denominator remain unquantified. Programme targets are not added to Aurelia sales. |
| R15 | Long-horizon economics | The pricing model ends in 1981. There is no cost/demand model through approximately 1989 or a household product roadmap, so the roughly decade-long $100 forecast remains a strategic judgement. |
| R16 | BPI commercial and delivery details | Final investment cap table/closing, specialist support costs, pilot results, database limits, payroll jurisdictions and update terms remain unresolved. Operational independence is established in the story; unrelated ownership is not asserted. |
| R17 | Tandy economics | OEM royalties, minimum purchases, port/support budgets and Model II configuration prices remain unspecified. No Tandy BPI port is part of the Abacus agreement. |
| R18 | Academy implementation | Exact cities/openings, occupancy, qualified instructors and specialist availability are still operating decisions. BPI enrolments consume existing capacity rather than adding free capacity. |
| R19 | Other retained engineering gates | BOM quantity/part/routing gaps, fabrication masks/process/yields, paired-RAM electrical design, MMU/interrupt timing and later network/database recovery acceptance remain open in their respective design/BOM records. This campaign does not certify them. |
| R20 | Historical market estimates | Market denominators, elasticities and response adjustments are scenario assumptions. Additional source research is required before treating them as historical measurements. Later supplier manuals establish architecture precedent, not June-1979 shipping dates. |

## Checked distinctions that are not contradictions

- The 1978 premiere remains 44 minutes; the 1979 presentation is a separate 50-minute programme.
- Apple native peripheral/display support does not imply CP/M or Z80 execution. Tandy retains its native video and qualified host-specific Abacus edition.
- Independent BPI branding/management is compatible with Adam's proposed investment. A future ownership separation around 1985 is not the beginning of operational independence.
- Optional open interfaces do not require Logix to fund every OEM port or DRI to promise an x86 OS on IBM's schedule.
- Aurelia's installed base is not the whole compatible ecosystem. Competitors may gain hardware sales while the standard grows.
- No withdrawn-product dates are invented. The $100 milestone neither retires all 8-bit systems nor guarantees every model remains in production for ten years.
- The 40% contribution-reduction policy explicitly supersedes the old margin safeguard. Existing stress losses (94 priced snapshots under the model's combined stress case) are intentional disclosed consequences, not arithmetic errors to repair by silently raising prices.
- Unqualified BOMs and numerical cost scenarios coexist because costs are conditional planning estimates. Likewise, announced introduction dates do not prove measured hardware/software readiness.
- Existing 1978 advertising/celebrity arrangements and conference venue/broadcast rights remain proposed agreements, not established contracts.

## Validation

Run all tests/validate_*.py and tests/*.test.cjs after rebuilding costs, pricing and sales. The added validate_ncc79.py checks stage order/duration, profile separation, timeline references, prospective OEM status, disclosure/product dates, targets and unchanged pre-NCC unit forecasts. Source hashes and deterministic rebuilds retain provenance; passing structural tests does not close R01–R20.

## COMDEX compatibility-kit follow-up

The December 3 kit, optional support and certification are now catalogued, costed and included in annual pricing. Named Abacus platforms are supported configurations rather than an exclusive permission list. The Aurelia+ focus permits independently designed Aurelia-class clones and maintains installed-base support without inventing a withdrawal date. The original 79-offer pricing baseline is unchanged; three additions use their own frozen baseline. November demand/sales values remain unchanged. Specialist staffing, certification throughput, December launch quotations, actual OEM adoption and post-launch substitution remain planning decisions. Public materials preserve the NCC 1980 architecture embargo.

## COMDEX campaign follow-up

The accepted campaign preserves catalogued text-mode bar charts rather than claiming additional graphical chart types. The shaded cube is a separate benchmark utility. Identical executable/workload/display settings and correct completion are required; no measured speedup is invented from the 4/6 MHz clocks. Payslips use precalculated fictitious values; field mapping, rounding, pagination, batch completeness and BPI reconciliation remain qualification gates. BPI stays independent and follows Abacus in the presentation. Abacus 2.0 supports both existing Aurelia and Aurelia+; the 45-minute programme is separate from the NCC programmes. Confidential preparation causes no new pre-November sales uplift. Marketing budget, actual benchmark results, demonstration readiness and signed supplier/media participation remain open. Next-generation disclosure remains embargoed until NCC 1980.
