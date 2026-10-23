# Shared computer configuration lists

Aurelia, Artemis and Athena use the same full-width equal-column list/inspector
layout and shared specification/BOM renderer. Component rows have a normal-weight
label at left and a bold value at right, on one compact line. Long text truncates
in the row; the selected inspector retains the complete value and specification.
Empty banks, ports and sockets are omitted. Compatible options and architecture
references stay in their own expandable sublists. Athena's unknown socket counts
and peripheral bundles are not inferred, and its planned configurations remain
explicitly labelled as pending qualification.

There is one system configuration dropdown. Artemis manufacturing revisions are
separate dated choices (Original / Networking); no hardware-revision or evaluation
filter is rendered. Old configuration/revision query links still resolve. June 15
cost history remains available in the configuration detail pane; clicking a row
selects that saved assessment and its BOM. The initial assessment is the latest
recorded date for the selected configuration, or its availability date when none
exists. No new estimates are generated.

Aurelia includes its recorded chassis, catalogue bundles and networking upgrade
kit. Its six documented chassis/bundle plus compatible-networking-upgrade
combinations are clearly labelled as combinations, not newly priced offers. The
Enhanced CP/M networking software replaces the base CP/M selection. The source
host and upgrade BOMs remain separate: replacement media and packaging have not
been consolidated, so no combined physical roll-up or cost is asserted.

Athena and Athena Server use their recorded planned RAM populations (256 KiB and
1 MiB), graphics/network cards, internal ROM, and 5/20 MB disks. No June 15 estimate
is available for these 1983 configurations in the saved model. The generic family
adapter reads existing technical and manufacturing projections; no canonical
hardware, software, dates, quantities or financial assumptions are changed.

The shared header retains content-proportional table cells, with centered text
and no visible cell/outer borders. The builder omits duplicate supplementary
blocks for all three computer pages. The historical artemis-configurator.js/css
filenames and DOM IDs are retained for compatibility while serving all families.

Validation: computer-families.test.cjs exercises every configuration/revision,
component selection, available annual assessment, populated bank counts, legacy
revision URLs and Aurelia networking replacement semantics. The original pure
Artemis model assertions remain in artemis-configurator.test.cjs. Page snapshots
are intentionally updated for the three computer bodies only. Shared navigation,
BOM Navigator, schema/view and BOM validators remain required. Rendered-browser
visual review is not available in this environment.
