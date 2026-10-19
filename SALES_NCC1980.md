# Sales and Academy demand through NCC 1980

Cutoff: **May 18, 1980**, the day before NCC opens on May 19. The last row covers May 1–18, not a full month. This US scenario forecast includes no next-generation computer deliveries or architecture-dependent customer knowledge. Earlier periods retain their campaign boundaries; prices and dependent projections reflect the video-cost rebase.

## Computer sales

| Scenario | Dec–May 18 Aurelia | Dec–May 18 Aurelia+ | Incremental computers | Cumulative since June 1978 |
|---|---:|---:|---:|---:|
| Conservative | 6,180 | 15,378 | 21,558 | 71,302 |
| Central | 11,590 | 22,690 | 34,280 | 101,180 |
| Strong | 14,601 | 28,882 | 43,483 | 121,283 |

These are conditional cases, not confidence intervals. Central cumulative stock is approximately 78,471 Aurelias and 22,647 Aurelia+ systems before retirement, returns or resale adjustments. Central calendar-1979 deliveries total 63,181; January–May 18, 1980 adds 27,187.

| Central period | Aurelia | Aurelia+ | Total | New Academy requests | Delivered enrolments |
|---|---:|---:|---:|---:|---:|
| 1979-12 | 3,871 | 3,166 | 7,037 | 2,210 | 1,590 |
| 1980-01 | 2,600 | 3,507 | 6,107 | 2,043 | 1,710 |
| 1980-02 | 1,889 | 4,113 | 6,002 | 2,060 | 1,824 |
| 1980-03 | 1,447 | 4,453 | 5,900 | 2,079 | 1,932 |
| 1980-04 | 1,226 | 4,694 | 5,920 | 2,126 | 1,998 |
| 1980-05 (1–18) | 557 | 2,757 | 3,314 | 1,230 | 1,200 |

### Demand mechanics

November new demand anchors the extension. Monthly factors and explicit incremental rates represent COMDEX applications/speed messaging, compatibility confidence, competing products, emerging clone substitution and hesitation ahead of the next-generation announcement. The model assumes successful campaign execution without inventing a measured speed multiplier. No extra Academy conversion bonus or duplicate June price-cut uplift is added.

Customers initially prefer Aurelia+ increasingly, but the price premium reduces the Plus-intending cohort using each scenario's existing elasticity. The modelled average package is $2,049.81 for Aurelia versus $2,662.06 for Aurelia+, approximately 30% more. Feature/campaign gains and price response are separate. Buyers deterred by price are not silently reassigned to Aurelia or placed in a firm-order backlog. Actual willingness to pay remains an important sensitivity.

Separate Aurelia and Aurelia+ queues retain 75% of prior unmet requests and lapse 25%. December Plus exposure is 29/31, reflecting its December 3 launch. May demand and capacity are prorated 18/31. Monthly ceilings describe conditional customer-delivery capacity, not proven factory output. The old model is not abruptly withdrawn; unused capacity is not sold stock. Compatible competitors' units are never Logix deliveries.

### Price and revenue boundaries

Existing products keep their June 1979 price/cost snapshots through the cutoff. New COMDEX offers use their first available June 1980 snapshots as **provisional launch-period proxies**, because no December quotes exist. This does not establish a historical launch price or apply future reductions to old products. The 80% Office/20% colour mix is retained with one disk and 70% printer attachment. The retained Aurelia package still contains its existing application mix; unmodelled additional purchases by new Aurelia owners are not assumed.

Central computer-package receipts after dealer fees are approximately $63.12m for December–May 18; recurring contribution is $15.95m, before marketing, credits, support expansion, development, financing and tax. Separate full-licence purchases by the November installed cohort yield 7,521 Abacus 2 licences. New Aurelia+ systems attach 4,538 Pulse licences; Pulse is not assumed available on original Aurelia. These additional applications produce about $0.71m AION receipts, outside package receipts. Independent BPI receipts are about $1.32m and remain outside Logix/AION revenue.

No automatic upgrade discount, duplicate bundled Abacus licence, customer trade-in resale, kit-volume revenue, OEM royalty or market-share denominator is invented. Software bought by existing owners is not an extra computer. Financial estimates are provisional until launch prices are established.

## Logix Computer Academy

| Scenario | New requests, Dec–May 18 | Delivered enrolments, Dec–May 18 | Delivered enrolments, June 1979–May 18 | Unmet requests at cutoff |
|---|---:|---:|---:|---:|
| Conservative | 6,810 | 6,810 | 12,937 | 0 |
| Central | 11,748 | 10,254 | 18,162 | 834 |
| Strong | 16,765 | 12,318 | 21,852 | 2,630 |

These are course enrolments, **not unique students, graduates or extra computer sales**. New-system customers, existing owners, prospective buyers and manufacturer/integrator learners generate explicit requests. Students may attend more than one course. Central December begins with 1,539 unmet requests from the June–November extension; 2,191 requests lapse during December–May 18, leaving 827 unmet after 10,254 delivered places. Requested places do not equal completed training.

### Course mix and capacity

The original 2/5/6/5-day courses cover Fundamentals, Fundamentals with Abacus, Business Tools workflow and developer training. Use the existing planning allowances of three days for BPI and two for Pulse. Abacus 2 chart/document material and Pulse teaching begin after COMDEX. Manufacturer learners consume existing developer-course capacity; engineering subscriptions are not extra student enrolments.

Central delivered December–May places: 2,580 Fundamentals; 3,090 Fundamentals/Abacus; 1,014 business workflow; 1,014 developer; 1,542 BPI; and 1,014 Pulse. This is a teaching-capacity allocation, not evidence that those cohorts already exist.

Central capacity grows from 20 centres/52 rooms in November to 22/56 in December and **27 centres, 72 rooms and 90 instructors by NCC**. Assume eight seats with six occupied, 18 teaching days per room-month and 15 per instructor-month. Whole course blocks consume their respective durations; both rooms and staff constrain delivery. May available days are prorated. BPI/Pulse specialist staffing and local schedule fit must be qualified; totals are not signed leases or confirmed openings.

The first-year 10,000–13,000 enrolment roadmap remains a historical planning target. The new June-1979-onward model neither invents prior actual attendance nor adds a second set of first-year students. Existing Fundamentals credits and other voucher terms remain unchanged. Tuition and redemption expenses require a separate cohort cash-flow model; they are not included as profits here.

## Practical implications

Aurelia+ shifts the product mix, but its package premium moderates demand. Existing-owner Abacus upgrades provide another route to application adoption. In the central case, Academy delivery is more constrained than aggregate computer capacity: train specialist instructors and use qualified dealer-hosted sessions before committing to additional permanent leases. Do not count either training registrations or manufacturer kit evaluations as hardware sales.

Rebuild with `python tools/build_sales.py`. The sales page presents all scenarios, product queues, monthly Academy requests/places and course mix. The Academy page links directly to its demand section. `tests/validate_ncc80_forecast.py` checks period boundaries, queues, financial arithmetic, course durations, staffing/room constraints and Pulse platform compatibility.
