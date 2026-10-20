# NCC 1979: open architecture and investment continuity

Accepted campaign: **Choose your computer. Keep your investment.** The goal is cross-vendor CP/M application compatibility and FlexiBUS peripheral adoption, with Logix video optional. The machine-readable programme is [ncc_1979_campaign.json](ncc_1979_campaign.json). This is an alternative-history plan, not evidence that independent manufacturers signed agreements or passed qualification.

## Three independent adoption choices

| Programme | Commitment | Boundary |
|---|---|---|
| CP/M application compatibility | Versioned core/extensions, documented APIs, named host editions and resource limits, document interchange | FlexiBUS/video optional; no universal binary or floppy-format guarantee |
| FlexiBUS peripherals | Published electrical/transport/class protocols, host drivers and diagnostics | CP/M/video optional; identification alone does not establish feature support |
| Logix display | Distinguish portable display API from optional controller, card, digital link and monitor qualification | Existing displays can implement the API; 80 columns needs a qualified 640-pixel monitor |

CP/M remains commercially licensed. Openness means non-exclusive implementation rights, own-brand products, reference drivers/tests, predictable licensing and equal access to qualified components. It does not imply free software or automatic open-source licensing. DRI leads the software programme; Logix contributes hardware specifications; independent suppliers participate in a working group. Final charter, voting, certification/dispute process, fees, code redistribution rights and maintenance duration require published agreements.

## Adam's honest migration commitment

The next generation will break native Z80 binary compatibility. The established C environment, APIs and file formats reduce source migration work; developers still recompile, adapt and test. Assembly, pointer/integer assumptions, banking and direct hardware access require review. The 1979 campaign teaches existing portable-C practices; it does not release the full new-target compiler/framework a year early.

A planned optional Z80 coprocessor provides a separate path for qualified legacy applications. Implementation details remain confidential. It is not a June 1979 shipping product, and compatibility is not promised for every future model.

Adam reveals neither the next processor's word size nor architecture before NCC 1980. The project technical catalog may contain those facts for the author; it must not be copied unfiltered into 1979 press material. The architecture reveal belongs to May 19, 1980.

The embargo applies throughout 1979, including COMDEX, Q&A, sales proposals, dealer training, partner/OEM briefings and developer clinics. Call the future offering only “next-generation computers”. Withhold future product/processor/OS names, word size, ISA, registers, memory organisation, execution design, performance, schematics and coprocessor integration. Demonstrate released 8-bit products only; distribute no future-target SDK, binaries, compiler output, benchmark, board photograph or linked specification from which the architecture could be inferred. Published current CP/M, FlexiBUS and optional video interfaces remain available.

Approved response to architecture questions: “We will discuss the new architecture at NCC 1980. Today we can describe our C migration approach and planned optional Z80 compatibility path.”

## Continuing eight-bit market

Eight-bit computers remain useful for business while declining prices broaden home, school and personal use. Maintain CP/M tools and applications alongside next-generation engineering; publish a funded support term before promising a specific service period. No fixed date forces all business users to migrate.

Adam expects next-generation computers to remain above roughly $100 for about a decade from 1979. This is a strategic forecast in nominal future US retail dollars before tax: a computer using an existing television and basic storage, excluding a complete disk/printer business system. Exact basic-storage inclusion remains open. It is not a forecast that Aurelia itself will cost $100, a guarantee of each model's production life, or a withdrawal trigger around 1989.

The existing professional digital-video interface cannot be assumed to drive a household television. A future consumer-TV output, hardware configuration and cost model are necessary before selling the forecast as an engineered product. The current pricing horizon ends in 1981; no invented 1989 prices are added.

## NCC presentation: 50 minutes before questions

| Segment | Minutes | Content |
|---|---:|---|
| Opening | 4 | Explain customer investment and independent choices for software, peripherals and displays. |
| Cross Vendor | 8 | Run supported application workflows on Aurelia and the Model II prototype. Use separately qualified host editions; preserve documents and supported semantics without promising identical binaries. |
| Applications | 10 | Demonstrate Abacus first, then independent BPI business records and summary export. BPI remains an independent licensor; no BPI Model II port is implied. |
| Flexibus | 7 | Operate a qualified peripheral sequentially on named hosts. Identification, driver support and application features are separately verified. Attach only at quiescent ports. |
| Apple Video | 6 | Show native Apple II drivers and optional display cards separately. No Apple CP/M/Z80 execution or automatic adaptation of existing Apple graphics is implied. |
| Partners | 7 | DRI, Tandy, Microsoft, BPI management and confirmed peripheral participants explain responsibilities and commercial access. No prospective OEM is presented as signed. SMC is a future qualified source, not June production supply. |
| Migration | 5 | Adam states that the next generation will break native Z80 binary compatibility. Existing C tools and documented APIs reduce source migration effort; recompilation, adaptation and testing remain necessary. A planned optional Z80 coprocessor offers qualified legacy execution. Architecture and word size remain secret until NCC 1980. Eight-bit systems retain business uses and broaden into homes and education as prices fall. |
| Availability | 3 | Separate shipping products, prototypes, future plans and adoption targets; provide documented configurations, licence terms, directory and developer-registration contacts. |

Use a tested Aurelia–Model II Abacus document round trip with separately supported host editions. Verify the actual transfer medium, file format and common feature subset. Tandy remains a prototype at NCC; customer release stays October 15. BPI follows Abacus and retains independent licensing/support; the Tandy agreement does not create a BPI port. Apple's native 6502 demonstrations do not claim CP/M execution. Mark prepared datasets and recordings. Validate quiescent attachment and all AV paths.

## Marketing sequence

| Scenario date | Activity |
|---|---|
| 1979-02-19 | Begin confidential briefings and engineering-kit evaluations. Prioritise North Star and Vector Graphic as prospects; approach Cromemco, Altos, Intertec and Heath selectively. Invitations are not signed agreements or qualified products. |
| 1979-05-05 | Alongside the existing DRI portable-extension release, publish separate CP/M application, FlexiBUS peripheral and optional Logix display compatibility profiles, reference-driver and test access, non-exclusive implementation principles and support-roadmap requirements. Exact fees and support duration remain to be settled. |
| 1979-05-21 | Invite computer, software and peripheral suppliers to test named configurations and document failures before public demonstrations. Supplier attendance and passing results must be verified; no announcement of an unsigned OEM. |
| 1979-06-04 | Present a 50-minute cross-vendor campaign before questions. Demonstrate applications/documents, then independent BPI, FlexiBUS, Apple native drivers and optional video. BPI management speaks with partners. State that the next generation breaks native Z80 binary compatibility; C source/API portability reduces migration work and a planned optional Z80 compatibility coprocessor supports qualified legacy software. Reveal neither processor word size nor architecture before NCC 1980. See ncc_1979_campaign.json. |
| 1979-07-16 | Run dealer demonstrations, joint trade-press activity and developer clinics. Teach documented APIs, file interchange, C portability boundaries and device-class drivers. Publish a directory distinguishing shipping, qualified and prototype configurations. |
| 1979-10-15 | Promote the separately recorded Tandy customer release and only individually qualified SMC or peripheral products. Update directory evidence; do not imply all licensed chips, every peripheral class or new independent OEM systems are shipping. |
| 1979-12-15 | Target Tandy shipping, one additional named OEM selling a supported CP/M-extension/FlexiBUS option, another OEM in qualification, dealer/integrator configurations and third-party devices in several categories. These are adoption targets, not recorded achievements or contracted orders. |
| 1980-01-14 | Publish verified customer examples, compatibility results and partner configurations. Target three to five non-Logix manufacturers with supported configurations by NCC 1980, counting Tandy once and excluding duplicate dealer builds. Do not disclose the new processor architecture early. |

The campaign emphasises OEM engineering, dealer roadshows, trade press, joint advertisements, developer clinics and an evidence-backed compatibility directory. The directory separates shipping, qualified, prototype and planned products and identifies responsible suppliers. Participation in a workshop does not confer certification or OEM endorsement. Partner/publicity rights and venue bookings remain execution gates.

## Manufacturers: recruitment priorities, not signed outcomes

| Prospect | CP/M extensions | FlexiBUS | Logix video hardware | Proposed approach |
|---|---|---|---|---|
| North Star | high | medium-high | medium, optional | First recruitment target with Lifeboat as a potential integration/distribution partner; official OEM support is separate from aftermarket compatibility. |
| Vector Graphic | high | medium-high | low-medium | Second priority; protect existing display investment and qualify software/interface options. |
| Cromemco | medium | medium | low | Selective compatibility programme; preserve its OS and graphics strategy. |
| Altos | medium-high | medium | low | Business-software and peripheral evaluation; no whole-platform redesign assumed. |
| Intertec | medium-high | medium, host-specific work | low | Late-1979 evaluation, potential 1980 qualification; later documentation does not establish June-1979 option availability. |
| Heath/Heathkit | medium | medium, host-specific accessory | low | Later feasibility programme, not a promised 1979 release. |

Tandy is the existing software/peripheral anchor; Apple is the native peripheral/display anchor. North Star/Lifeboat and Vector Graphic are recruitment priorities, not assumed signatories. Cromemco preserves its independent OS/graphics strategy. Altos, Intertec and Heath require host-specific feasibility work. Later manuals are architectural evidence only; they cannot prove that later options shipped in June 1979.

## Peripheral opportunities and constraints

Recruit independently branded wide-carriage/letter-quality/specialist printers, plotters, modems, larger floppy/backup systems, selected hard disks and specialist input/instruments. Publish a product-boundary policy so partners understand where Logix's reference products end; do not promise an unagreed perpetual exclusion from every market.

Plotter, modem and specialist profiles still need definition and drivers. Printer discovery does not specify fonts, forms or plotting commands. Storage requires geometry, media/error handling, durable flush and separate boot qualification. V1 supports one device per host port, not passive hubs or implicit daisy chains. The 500-kbit/s rate allows at most 50 KB/s before framing overhead, so fast native disk controllers remain legitimate. Architecture-tagged ROM code must not execute on an incompatible CPU.

## Targets and economics

By December 1979 target Tandy shipping, one additional supported OEM configuration and another OEM in qualification, several dealer/integrator configurations and devices in several third-party categories. By NCC 1980 target three to five distinct non-Logix manufacturers with officially supported configurations, counting Tandy once. Logix video is selective, not mandatory. None of these targets is recorded as an achieved shipment event.

Track independent compatible-computer sales, qualified applications, third-party peripheral shipments, interchange/support results and supply concentration. A fall in Aurelia share may accompany ecosystem success. No OEM volume or royalty is invented.

Campaign, ports, reference engineering, certification, support, directories and roadshows need operating budgets outside unit manufacturing costs. The pre-NCC forecast remains 10,396 Aurelias in 1978 and 28,400 through May 1979. Most activity occurs after its cutoff; confidential recruitment creates no immediate consumer sales. May communications receive no separately calibrated uplift beyond existing assumptions. The separate June–November extension in sales_forecast.json now models price response, campaign gains, substitution and monthly delivery limits; independent BPI receipts remain separate. Compatible OEM volumes and royalties remain unquantified.

## Evidence boundaries

- [December 1979 primary manual supports North Star CP/M integration precedent, not an actual alternate partnership.](https://deramp.com/downloads/north_star/software/manuals/Lifeboat%20CPM%2022.pdf)
- [May 1979 reproduced Vector price list supports existing CP/M and display investment.](https://vintagecomputer.com/vector-graphic-inc-pricelist-1979.html)
- [Period advertising supports Cromemco independent OS/compatibility positioning.](https://www.worldradiohistory.com/UK/Practical-Computing/70s/Practical-Computing-1979-09-S-OCR.pdf)
- [Later primary manual; architecture precedent only, not proof of June 1979 adapter availability.](https://www.bitsavers.org/pdf/intertec/Superbrain_Users_Manual_Sep80.pdf)

See [CONSISTENCY_REVIEW_1979.md](CONSISTENCY_REVIEW_1979.md) for corrections and unresolved decisions.
