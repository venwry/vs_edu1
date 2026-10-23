# BOM vendor and first-use metadata

This change implements the approved story sourcing choices using existing
`manufacturer`, `manufacturer_part_number`, `vendor`, `requirements` and
`introduced` fields. It preserves every component, assembly, offer and functional
set identity and every BOM quantity. Combined elements remain combined; Logix is
the assembler/vendor, not a claim that Logix fabricates every constituent.

## Authoritative records and decisions

- `data/manufacturing/sourcing/bompart.*.json`: custom ROM chips are AION Labs;
  boards, enclosures, connectors, cables, assembled electronics, media selections,
  passive kits and packout sets are Logix. Known physical suppliers on linked
  catalogue records populate the existing manufacturer field. Fifteen entries
  remain unknown: unselected commodity DRAM/display OEMs and discrete mechanical,
  switch, diode, amplifier, ribbon and deflection parts. The existing Ball Brothers
  candidate for the 17-inch core is not promoted to qualified manufacturer.
- `data/hardware/components/part.*.json`: combined RAM modules use Logix as vendor;
  their AION chips and technology references remain unchanged. `part.hdd_5mb`
  selects Seagate ST506, also recorded in `bompart.part.hdd_5mb`.
- `data/software/products/software.product.aionix.json` and
  `software.product.cpm.json`: fill parent vendors as AION Software and Digital
  Research. Existing explicit edition attributions remain intact.
- `data/manufacturing/boms/programs/document.athena_1983_program.json` and
  `data/hardware/computers/computer.athena*.json`: keep functional sets intact;
  attribute the combined mainboard/power/chassis and ROM-bank sets to Logix and the
  EEPROM BIOS to AION Labs. Add the storage candidates below using the existing
  attribution and requirements vocabulary. These are the programme's planned
  1983 offering dates, not evidence of historical shipments.

## Drive selections

| Existing element | Supplier/model | Conditions |
| --- | --- | --- |
| Aurelia internal FDD; FlexiDisk | Shugart Associates SA400 | 35-track single-sided FM; format geometry must be frozen |
| FlexiDisk II | Shugart Associates SA400-derived OEM mechanism | Logix dual-format electronics; stock electronics do not establish Apple II GCR compatibility |
| Aurelia+, Artemis, Artemis PRO internal FDDs | Shugart Associates SA450 | DS/DD MFM; controller and formatted geometry unqualified |
| `part.hdd_5mb`; Athena 5 MB functional HDD | Seagate Technology ST506 | 5.0 MB formatted, 6.38 MB raw; 5 Mbit/s MFM; 34-pin control / 20-pin data; +12 V 4.5 A startup, +5 V 1 A maximum |
| Athena / Athena Server functional FDD | Shugart Associates SA450 | DS/DD; no invented formatted capacity |
| Athena Server 20 MB functional HDD | Rodime RO202E | 20.97 MB formatted, marketed as 20 MB; existing nominal `capacity_mb: 20` retained |

Model selection does not resolve procurement, interface, mounting, power or incoming
test qualification. No mechanisms or complete functional sets were split.

## PSU sourcing proposals

All complete PSU elements remain Logix assemblies. Candidate Power-One modules
are recorded in their existing requirements arrays, not as new BOM constituents.

| Existing PSU | Candidate modules |
| --- | --- |
| Aurelia | HC5-6/OVP + HC12-3.4 and qualified -5 V DRAM bias |
| Aurelia+ | HC5-6/OVP + HN12-5.1; auxiliary rails must be qualified |
| Artemis | D5-12 with overvoltage protection + HN12-5.1 |
| Artemis PRO | D5-12 with overvoltage protection + HE12-10.2; include HDD startup |
| FlexiDisk / FlexiDisk II | HB5-3/OVP + HC12-3.4 |
| 4 / 8 / 16-port network hub | HB5-3/OVP / HC5-6/OVP / D5-12 with overvoltage protection |
| FlexiPrint 40 | HB5-3/OVP logic; HC24-2.4 only if actuator voltage/pulse current matches |

These families are documented before June 1978. They are candidate building
blocks, not released power designs: rail budgets, peak loads, cooling, footprint,
mains variants and protection remain unresolved. Athena's combined system set
stays Logix with PSU sizing open pending a complete rail budget. Monitor PSU notes
retain OEM delivery boundaries to avoid double counting; Mono Pro needs a custom
HV/deflection design matched to its tube and yoke, not a generic low-voltage PSU.

## Dates and schema

Only previously missing navigator dates are populated. First use is the earliest
reachable offering date through forward BOM relationships, bounded by assembly,
linked-component and manufacturing-variant effective dates. Standalone part
catalogue dates are not roots; proposed bundles are not released offers. Existing
catalogue dates, including prototype dates, are preserved.

| First offering use | Standalone BOM elements |
| --- | ---: |
| 1978-06-05 | 59 |
| 1979-06-04 | 38 |
| 1979-12-03 | 22 |
| 1980-05-19 | 47 |
| 1981-05-04 | 46 |
| 1982-06 | 29 |
| no release | 5 |

The five unused `bompart.part.artemis_ram_module_32kb_x16.*` elements and seven
`bundle.proposed_*` records use:

```json
"introduced": {
  "event_name": "no release",
  "event_start_date": null
}
```

BOM Navigator displays and filters these as **no release**, while a genuinely
missing date still means Unknown. Proposal `earliest_offer_date` remains planning
metadata. Month precision remains month precision. No parallel release/status
field is added.

The v2 BOM record and legacy projection schemas add the existing `introduced`
structure, with a date string or the explicit no-release/null pair. The BOM record
schema also permits strings in its existing `manufacturer_part_number`, matching
the legacy schema. These are additive v2 changes. Example released structure:

```json
"introduced": {
  "event_name": "NCC 1980 — Logix Artemis launch",
  "event_start_date": "1980-05-19"
}
```

## Historical evidence

These documents establish historical models/specifications, not fictional Logix
contracts or qualification results:

- [Shugart SA400 OEM manual (1977)](https://nfggames.com/X68000/Documentation/Floppy%20Drives/Shugart/SA400%20Minifloppy%20OEM%20Manual.pdf): SA400 mechanism and interface requirements.
- [Shugart SA400/8080/1771 application note (November 1977)](https://deramp.com/downloads/mfe_archive/020-Disk%20Drives/Shugart/SA400/39003_SA400_8080_1771_App_Note_Nov77.pdf): period SA400/SA450 family and density options.
- [Seagate ST506 preliminary OEM manual (April 1981)](https://www.minuszerodegrees.net/manuals/Seagate/Seagate%20ST506%20-%20OEM%20Manual%20-%20Preliminary%20-%20Apr81.pdf): capacity, interface and power requirements.
- [Rodime RO200E product specification (1982)](https://bitsavers.trailing-edge.com/pdf/rodime/Rodime_RO200/PRO-0033r3_RO_200E_Series_Disk_Drive_Product_Specifcation_1982.pdf): RO202E availability and formatted capacity.
- [Electronics, 25 May 1978, Power-One advertisement](https://www.worldradiohistory.com/Archive-Electronics/70s/78/Electronics-1978-05-25.pdf): period module family/model table. Physical and electrical integration remain Logix engineering work.

## Build and validation

`python tools/data_catalog.py` rebuilds three affected compatibility views:
`hardware-bom.json`, `logix-aion-technical-catalog-v2.json`, and
`athena-1983-program.json`. No financial models, prices, historical hashes or frozen
baselines are rebuilt. The reviewed page-content fixture changes only for the
intended vendor, release-date, drive-name and specification text.

`tests/validate_bom_metadata.py` independently checks dates against forward BOM
reachability and variant dates. Navigator tests cover vendor inheritance, explicit
no release versus unknown, first use, month precision and filtering. Validation
results are recorded in the pull request.

Validation outcome: schema/structure, taxonomy, catalogue references, hardware
BOM, software/RAM migration, Athena, cost consolidation, COMDEX82 costs and the
new first-use audit pass. Protected-value comparison confirms unchanged IDs,
references, quantities, capacities, unit costs and all 114 assembly records.

The ecosystem forecast source-hash check passes on the base commit but now flags
the changed technical catalogue as stale. This is an intentional provenance
invalidation from metadata edits; no saved forecast hash was rewritten to disguise
it. The existing atlas Node test also fails on the base commit (missing retired
`pricing.html` navigation). Those failures are not removed or suppressed.
