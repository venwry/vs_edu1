# Sales and Academy demand through NCC 1980

Cutoff: **May 18, 1980**, the day before NCC opens on May 19. The last row covers May 1–18, not a full month. This US scenario forecast includes no next-generation computer deliveries or architecture-dependent customer knowledge. Original projections through November 1979 are unchanged.

## Computer sales

| Scenario | Dec–May 18 Aurelia | Dec–May 18 Aurelia+ | Incremental computers | Cumulative since June 1978 |
|---|---:|---:|---:|---:|
| Conservative | 6,180 | 15,369 | 21,549 | 71,286 |
| Central | 11,571 | 22,647 | 34,218 | 101,118 |
| Strong | 14,601 | 28,816 | 43,417 | 121,217 |

These are conditional cases, not confidence intervals. Central cumulative stock is approximately 78,471 Aurelias and 22,647 Aurelia+ systems before retirement, returns or resale adjustments. Central calendar-1979 deliveries total 63,181; January–May 18, 1980 adds 27,187.

| Central period | Aurelia | Aurelia+ | Total | New Academy requests | Delivered enrolments |
|---|---:|---:|---:|---:|---:|
| December 1979 | 3,871 | 3,160 | 7,031 | 2,208 | 1,590 |
| January 1980 | 2,600 | 3,500 | 6,100 | 2,041 | 1,710 |
| February | 1,874 | 4,105 | 5,979 | 2,055 | 1,824 |
| March | 1,445 | 4,445 | 5,890 | 2,077 | 1,932 |
| April | 1,225 | 4,685 | 5,910 | 2,123 | 1,998 |
| May 1–18 | 556 | 2,752 | 3,308 | 1,229 | 1,200 |

### Demand mechanics

November new demand anchors the extension. Monthly factors and explicit incremental rates represent COMDEX applications/speed messaging, compatibility confidence, competing products, emerging clone substitution and hesitation ahead of the next-generation announcement. The model assumes successful campaign execution without inventing a measured speed multiplier. No extra Academy conversion bonus or duplicate June price-cut uplift is added.

Customers initially prefer Aurelia+ increasingly, but the price premium reduces the Plus-intending cohort using each scenario's existing elasticity. The modelled average package is $2,047.99 for Aurelia versus $2,661.41 for Aurelia+, approximately 30% more. Feature/campaign gains and price response are separate. Buyers deterred by price are not silently reassigned to Aurelia or placed in a firm-order backlog. Actual willingness to pay remains an important sensitivity.

Separate Aurelia and Aurelia+ queues retain 75% of prior unmet requests and lapse 25%. December Plus exposure is 29/31, reflecting its December 3 launch. May demand and capacity are prorated 18/31. Monthly ceilings describe conditional customer-delivery capacity, not proven factory output. The old model is not abruptly withdrawn; unused capacity is not sold stock. Compatible competitors' units are never Logix deliveries.

### Price and revenue boundaries

Existing products keep their June 1979 price/cost snapshots through the cutoff. New COMDEX offers use their first available June 1980 snapshots as **provisional launch-period proxies**, because no December quotes exist. This does not establish a historical launch price or apply future reductions to old products. The 80% Office/20% colour mix is retained with one disk and 70% printer attachment. The retained Aurelia package still contains its existing application mix; unmodelled additional purchases by new Aurelia owners are not assumed.

Central computer-package receipts after dealer fees are approximately $62.98m for December–May 18; recurring contribution is $15.95m, before marketing, credits, support expansion, development, financing and tax. Separate full-licence purchases by the November installed cohort yield 7,521 Abacus 2 licences. New Aurelia+ systems attach 4,529 Pulse licences; Pulse is not assumed available on original Aurelia. These additional applications produce about $0.71m AION receipts, outside package receipts. Independent BPI receipts are about $1.32m and remain outside Logix/AION revenue.

No automatic upgrade discount, duplicate bundled Abacus licence, customer trade-in resale, kit-volume revenue, OEM royalty or market-share denominator is invented. Software bought by existing owners is not an extra computer. Financial estimates are provisional until launch prices are established.

## Logix Computer Academy

| Scenario | New requests, Dec–May 18 | Delivered enrolments, Dec–May 18 | Delivered enrolments, June 1979–May 18 | Unmet requests at cutoff |
|---|---:|---:|---:|---:|
| Conservative | 6,808 | 6,808 | 12,934 | 0 |
| Central | 11,733 | 10,254 | 18,162 | 827 |
| Strong | 16,745 | 12,318 | 21,852 | 2,619 |

These are course enrolments, **not unique students, graduates or extra computer sales**. New-system customers, existing owners, prospective buyers and manufacturer/integrator learners generate explicit requests. Students may attend more than one course. Central December begins with 1,539 unmet requests from the June–November extension; 2,191 requests lapse during December–May 18, leaving 827 unmet after 10,254 delivered places. Requested places do not equal completed training.

### Course mix and capacity

The original 2/5/6/5-day courses cover Fundamentals, Fundamentals with Abacus, Business Tools workflow and developer training. Use the existing planning allowances of three days for BPI and two for Pulse. Abacus 2 chart/document material and Pulse teaching begin after COMDEX. Manufacturer learners consume existing developer-course capacity; engineering subscriptions are not extra student enrolments.

Central delivered December–May places: 2,580 Fundamentals; 3,090 Fundamentals/Abacus; 1,014 business workflow; 1,014 developer; 1,542 BPI; and 1,014 Pulse. This is a teaching-capacity allocation, not evidence that those cohorts already exist.

Central capacity grows from 20 centres/52 rooms in November to 22/56 in December and **27 centres, 72 rooms and 90 instructors by NCC**. Assume eight seats with six occupied, 18 teaching days per room-month and 15 per instructor-month. Whole course blocks consume their respective durations; both rooms and staff constrain delivery. May available days are prorated. BPI/Pulse specialist staffing and local schedule fit must be qualified; totals are not signed leases or confirmed openings.

The first-year 10,000–13,000 enrolment roadmap remains a historical planning target. The new June-1979-onward model neither invents prior actual attendance nor adds a second set of first-year students. Existing Fundamentals credits and other voucher terms remain unchanged. Tuition and redemption expenses require a separate cohort cash-flow model; they are not included as profits here.

## Practical implications

Aurelia+ shifts the product mix, but its package premium moderates demand. Existing-owner Abacus upgrades provide another route to application adoption. In the central case, Academy delivery is more constrained than aggregate computer capacity: train specialist instructors and use qualified dealer-hosted sessions before committing to additional permanent leases. Do not count either training registrations or manufacturer kit evaluations as hardware sales.

Rebuild with `python tools/build_sales.py`. The sales page presents all scenarios, product queues, monthly Academy requests/places and course mix. The Academy page links directly to its demand section. `tests/validate_ncc80_forecast.py` checks period boundaries, queues, financial arithmetic, course durations, staffing/room constraints and Pulse platform compatibility.
