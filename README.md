# bagwis-interfaces

The contract between BAGWIS repositories. Message and service definitions plus
the canonical topic registry. **No logic.**

Specified by [`SRS-00-interfaces.md`](https://github.com/bagwis-research/bagwis-docs/blob/main/DP1/planning/software/SRS-00-interfaces.md).

| | |
|---|---|
| **ROS package** | `bagwis_interfaces` (ament_cmake, `rosidl`) |
| **Owners** | Joshua + Earl Clyde — changes need both approvals |
| **Consumers** | `bagwis-airborne`, `bagwis-core`, `bagwis-web` |
| **Consumed as** | git submodule pinned to a **tag**, never a branch (FR-IF-04) |

## Why this repository exists

Three topics that cross a node boundary have no official ROS type:
`/ai/ndvi`, `/dashboard/final_metrics`, `/dashboard/safety_alerts`. Each is
produced by one repository and consumed by another. If their definitions lived
inside either side, a field rename would silently break the other, and it would
surface as an `undefined` on screen during an LGU evaluation session.

## Layout

```
msg/                8 messages          SRS-00 §4.1–4.8
srv/                3 services          SRS-00 §4.9
topics/registry.yaml    <-- the single source of truth for every topic name
scripts/generate.py     <-- reads it, writes the three languages below
include/bagwis_interfaces/topics.hpp    generated, committed
python/topics.py                        generated, committed
ts/topics.ts, ts/msg/*.ts, ts/srv/*.ts  generated, committed
```

## Using the constants

No repository types a topic name. Ever. That is what FR-IF-03 is for, and it is
the first of three guards against C-13 — a transposed name (the two middle
letters of NDVI swapped) fails *silently*, because the subscriber simply
receives nothing and it presents as a dead sensor.

```cpp
#include <bagwis_interfaces/topics.hpp>
create_publisher<bagwis_interfaces::msg::NdviResult>(bagwis::topics::AI_NDVI, 10);
```

```python
from bagwis_interfaces.topics import AI_NDVI
from bagwis_interfaces.msg import NdviResult
self.create_publisher(NdviResult, AI_NDVI, 10)
```

```ts
import { AI_NDVI, type NdviResult } from "@bagwis/interfaces";
ros.subscribe<NdviResult>(AI_NDVI, (m) => setNdvi(m.mean_ndvi));
```

## Changing a message

1. Edit the `.msg`, or `topics/registry.yaml` for a name.
2. `python3 scripts/generate.py` — **required**; the generated files are
   committed and CI compares them.
3. Bump `<version>` in `package.xml`. Field addition is a minor bump; a rename,
   removal, or type change is a **major** bump that must name the affected
   consumers in `CHANGELOG.md` (FR-IF-05). CI fails without a bump (FR-IF-07).
4. Tag the release, then move each consumer's submodule pointer.

Generated files carry a `THIS FILE IS GENERATED` banner. Editing one by hand
gets reverted by the next `generate.py` run and caught by CI before that.

## Build

```bash
colcon build --packages-select bagwis_interfaces
ros2 interface show bagwis_interfaces/msg/FinalMetrics
```

The build **verifies** the committed generator output and fails if it is stale.
It never writes into the source tree.

TypeScript, which needs no ROS toolchain:

```bash
npm install && npm run verify     # generate.py --check && tsc --noEmit
```

## Dependencies

Declared: `std_msgs`, `geographic_msgs`, `builtin_interfaces` — the only
packages whose types appear in a field.

Not declared: `sensor_msgs`, `vision_msgs`, `geometry_msgs`, `mavros_msgs`.
They appear in the SRS-00 §3 topic table but in no field here, so depending on
them would force those apt packages onto every machine that builds this one,
the Pi Zero 2 W included, for a dependency nothing uses. Their types are
recorded in `topics/registry.yaml`; each consumer declares what it subscribes to.
