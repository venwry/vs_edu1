# Artemis configuration workbench

The Artemis page combines hardware and fitted peripherals in one grouped diagram.
Its right-hand inspector uses the existing structured specification renderer.
Select a complete system, chassis, upgrade kit, professional offering or explicitly
labelled expansion target, then choose the hardware revision and BOM evaluation.
All 24 currently recorded choices derive from the existing catalogue, memory
configurations and cost rows. The six expansion targets are not advertised as
qualified offers. PRO announcements retain the unknown-shipment warning.

This prototype applies only to `artemis.html`. Aurelia and Athena retain their
existing explorers. Artemis's software, memory, bundles and detailed legacy views
remain available in the expandable reference section below the new workbench.
Configuration, revision, evaluation and model selections are encoded in the URL.
The component inspector retains its selection when that component remains fitted.

## Authoritative data and scope

- `generated/catalogs/logix-aion-technical-catalog-v2.json`: computers, RAM bank
  population, cards, displays, software, offers, effective dates and readiness.
- `generated/catalogs/hardware-bom.json`: recursive assembly membership and
  structural quantities, including explicitly unresolved quantities.
- `generated/models/manufacturing-costs.json`: saved annual evaluations, component
  estimates, costs and their assumptions. No model is recalculated by this view.

Their canonical sources remain under `data/hardware/`, `data/commercial/`,
`data/software/`, `data/manufacturing/` and `data/business/` as defined in the manifest.
No technical facts, financial assumptions, schema versions or calculated outputs
change in this UI prototype.

The supplied drawing guides the grouping and connections. Actual catalogue facts
win: there is one dedicated primary video connector in addition to four general
expansion slots; the standard chassis has two internal floppy drives. PRO also has
its recorded 5 MB internal disk. The Budget Hard-Disk Office uses an external disk
subsystem and retains both floppies. NICs consume a general slot. Slot/port numbering
in the diagram is illustrative; no undocumented pinout or slot assignment is implied.
Memory banks contain matched module pairs. OS/application cartridge capacity is not
invented from the illustration. Chassis-only offers do not acquire an OS cartridge,
keyboard or monitor. Upgrade kits are not shown as complete computers. The CAD
reference configuration uses the two named displays/cards and documented 1 MiB host;
its base primary card is replaced rather than duplicated.

## Dated costs and BOM interpretation

Only dates explicitly present in the cost metadata and ending in June 15 appear.
Select the original revision to inspect the 1980 launch-system evaluation; select
the networking revision for its 1981 and 1982 evaluations. Introduction is a catalogue
offering boundary, not proof of shipment. The current annual series ends in 1982.
The November CAD offering and uncosted expansion targets therefore show no annual
costs; unknown values are not converted to zero or extrapolated into 1983.

Manufacturing and fulfillment is the saved recurring total less separately recorded
licence and service delivery costs. The complete recurring total and its original
uncertainty range are also shown. The BOM-material column is a subset, not an amount
to add again to manufacturing and fulfillment. Component unit estimates are the
saved extended amount divided by the saved model quantity.

Budget Office evaluations contain aggregate `budgetcost.*` rows, including packages
and HDD allowances. These are labelled complete recurring-cost components, not
physical-material unit prices. Their structural BOM is displayed separately, followed
by the saved decomposition; totals must not be summed across these overlapping views.
The dated catalogue assembly determines fitted hardware even when a legacy budget
snapshot still names its launch assembly. No saved snapshot is silently rewritten.

Structural BOM quantities can be unresolved while the existing model uses a planning
allowance. Those differences remain visible with source links and relevant quantity
assumptions. The UI does not turn planning estimates into released production BOMs.

## Verification

Run `node tests/artemis-configurator.test.cjs` with the project's jsdom dependency.
It checks all configuration/revision/date combinations, inclusion of every catalogue
offer and RAM target, the network/OS revision boundary, 4-bank population, inspector
selection, external HDDs, aggregate cost components and missing-cost cases.

The shared organisation test, structured-specification test, wire-routing test,
canonical data validation and BOM validation also apply. Only the Artemis entry in
`tests/page-content-reorganized.json` changes for this intentional UI update.
The older `tests/atlas.test.cjs` still expects `.site-nav` links on Timeline and fails
against the pre-existing shared header; it is not part of the current page CI suite.

A live browser screenshot could not be verified in the execution environment:
the cloud browser cannot reach the local HTTP server and disallows file URLs.
DOM interaction coverage does not replace a final desktop/mobile visual review.
