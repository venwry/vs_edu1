# LogixLAN 1981 negotiated rates

Catalog 2.8 replaces the fixed 100 kbit/s link with one shared rate selected from 100, 250, 500 and 1,000 kbit/s. The stable `technology.logix_lan100_link` reference is retained. All rates are raw bit rates; application throughput remains a measurement gate.

| Host | Advertised platform rates (kbit/s) | Ceiling |
|---|---|---:|
| Aurelia | 100, 250 | 250 kbit/s |
| Aurelia+ | 100, 250, 500 | 500 kbit/s |
| Artemis / Artemis PRO | 100, 250, 500, 1,000 | 1 Mbit/s |

Firmware advertises the intersection of hardware capability, host ceiling and configured cable/reliability limits. The hub selects the highest common qualified rate. Any Aurelia limits a mixed network to at most 250 kbit/s; without Aurelia, an Aurelia+ limits it to 500. Artemis-only networks can reach 1 Mbit/s if every link and the hub qualify. Any 100-only participant limits the network to 100.

Start and coordinate at 100 kbit/s. Collect capabilities, announce and acknowledge a switch epoch, drain traffic, change the distributed clock, and qualify every link with test frames. Resume normal grants only after all links pass. Persistent errors cause coordinated step-down; clock/control loss invokes independent watchdog recovery to 100. Periodic 100 kbit/s discovery windows admit new stations and can lower the common rate. Their overhead reduces usable bandwidth.

The 4/8/16-port hubs remain streaming repeaters with one active transmitter, not independent per-port links or rate-converting switches. A 10 MHz divider reference can generate all four clocks with divisors 100/40/20/10. Maximum shared raw capacity is 125 kB/s at 1 Mbit/s, before protocol, polling and discovery overhead.

Adapters require hardware framing/CRC, destination filtering, complete-frame buffering, packet interrupts and receiver credits. Use a 4 KiB local packet-RAM design target, additional to host RAM. Frame length, IP MTU, buffer partitions, actual RAM parts and chip counts remain release gates. Reserve destination credit before unicast; broadcasts require credit from every intended receiver. Flow control handles temporary receiver pressure; a configured lower ceiling can address a persistently slow host.

Validate service latency and sustained TCP/IP throughput on each platform. Aurelia has 128 CPU clocks per raw byte at 250 kbit/s; Aurelia+ has 96 at 500 kbit/s. These are clocks, not instructions or guaranteed payload throughput. Cable limits, timing, error thresholds, discovery intervals and watchdog/ack timeouts require electrical and protocol qualification.

Both Aurelia and Aurelia+ now specify three independent point-to-point FlexiBUS ports, allowing keyboard, external disk and printer connections together. This does not change FlexiBUS signaling rates or general-purpose expansion-slot counts. Controller die quantity, per-port electronics, power and simultaneous-service testing remain manufacturing gates.

Run the existing catalog, BOM, video and UI validation documented in ATLAS_README.md. Specification consistency does not establish physical qualification.
