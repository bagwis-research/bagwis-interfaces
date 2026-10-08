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
msg/                12 messages, including the atomic segmented-detection contract
srv/                4 services, including paired biomass export
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
3. Bump `<version>` in `package.xml` and keep the npm package/lockfile version
   aligned. Field addition is a minor bump; a rename, removal, or type change
   is a **major** bump that must name the affected consumers in `CHANGELOG.md`
   (FR-IF-05). CI fails without a bump (FR-IF-07).
4. Obtain both owners' approvals and merge the contract before a stable tag;
   then move each consumer's submodule pointer. Coordinated testing can use an
   immutable prerelease tag first; it is not a stable release.

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

## F3.6 breaking contract: 1.0.0 / v1.0.0-rc.1

ROS and npm package versions are **1.0.0**; coordinated core/web/airborne
consumers pin **`v1.0.0-rc.1`**. The contract is in
[draft PR #5](https://github.com/bagwis-research/bagwis-interfaces/pull/5),
requiring both Joshua (`JoshuaHM-p4`) and Earl Clyde (`EarlClydeeee`) to review.
Interfaces approval/merge and stable `v1.0.0` publication must precede consumer
stable pin updates. Neither this prerelease nor a consumer PR is approval to
merge, publish stable tags or mark field gates complete.

### Atomic segmented detections

`AI_DETECTIONS_RAW` and `AI_DETECTIONS` keep their topic names/QoS and now use
`bagwis_interfaces/msg/SegmentedDetectionArray`, replacing
`vision_msgs/msg/Detection2DArray` without an old-type shim:

```text
SegmentedDetectionArray:
  std_msgs/Header header       # capture stamp, undistorted full-resolution frame
  uint32 image_width_px
  uint32 image_height_px
  SegmentedDetection[] detections
SegmentedDetection:
  uint8 class_id               # 0..4, or 255 unknown; best hypothesis
  float32 confidence
  float64 center_u, center_v, width_px, height_px
  uint32[] mask_runs           # [start,length,...], row-major image indices
```

This summary groups the four scalar box fields for readability; the `.msg`
defines each separately. The foreground count is `sum(lengths)`, with no
redundant count field. Each foreground index denotes the cell
`[column,column+1] × [row,row+1]` in pixel-edge coordinates. Runs have positive
length, stay inside a single row/image, are sorted/non-overlapping, and are
coalesced within each row. A nonempty detection requires foreground pixels.
An empty detection array is a valid empty frame; absent/invalid masks in a
nonempty frame are rejected, never treated as measured zero.

Inference producers must undo letterboxing on boxes **and masks**, choose the
highest-score hypothesis (ties preserve producer order), and stamp the
original capture. Admission forwards the entire message unchanged. There is
no paired mask topic. Existing bags with old wire types must be regenerated.
`NdviResult.mask_pixel_count` is removed: NDVI owns only index-aligned NDVI
values/availability, not segmentation area. NIR-unavailable values are NaN,
while valid class-0 mask area can still yield finite area-derived biomass.

### Metric semantics

`ObstructionCluster` and `FinalMetrics` expose equal-length, sorted
`class_ids`/`class_area_m2` arrays. Areas are exact projected pixel-mask spatial
unions, preserving holes and disconnected components. Observation area is
foreground count × GSD²; box/hull geometry is display metadata, not measured
area. Same-class revisits and mission totals across clusters are deduplicated.
Cross-class overlap stays visible in each class layer; total area is the union
of all layers, not necessarily their sum.

| Layer | Applicable outputs |
|---|---|
| Class 0, hyacinth | Hyacinth area, wet biomass, RWOR |
| Classes 1–4 | Waste area, volume, fractional truck-load equivalents |
| Unknown 255 | Visible per-class area; excluded from the named buckets/derived metrics |

Mixed-cluster metrics use their relevant layers regardless of dominant label.
`is_organic` means dominant class 0; wood does not receive hyacinth density.
Non-applicable metrics are zero, applicable unmeasured metrics are NaN.
Legacy box-only clusters retain their IDs but are incomplete: partial later
masks do not make the historical survey measured. A new mission is required
for a complete survey. `FinalMetrics.kde_lat`/`kde_lon` are now float64 arrays;
weights remain float32 and represent actual Gaussian area-weighted density.

`AnalyticsAssumptions` adds RWOR alert threshold and river-profile
source/revision, corrects launch offset to **added** to relative altitude,
and discloses mask-union/static-target policy, fractional loads,
NIR-independent measured biomass, actual KDE grid spacing and uncalibrated
empirical constants. `GeoreferencingStatus.rejected_invalid_mask` distinguishes
invalid atomic frames. Core requires mission profile/bandwidth/threshold/
confidence/model inputs; synthetic profiles require explicit opt-in. Segment,
profile, calibration/area scale, confidence and model identity are frozen per
mission so persisted geometry cannot silently change meaning.

### Paired biomass service

`BIOMASS_EXPORT` names `/analytics/export_biomass_sample`, served by
`georeferencing_node`, with type `bagwis_interfaces/srv/ExportBiomassSample`:

```text
Request: sample_id, capture_stamp, location, match_radius_m,
         actual_available, actual_kg_m2
Response: success, message, csv_path
```

The caller supplies a real harvest coordinate and exact capture time.
Core selects the nearest positive-area class-0 observation inside the radius
(ties by detection index, then cluster ID), with no temporal extrapolation.
Missing match or invalid input is an explicit error. Predicted density is
kg/m²; wet mass is measured area × density in kg. Unavailable actual density
and NDVI are blank in the CSV, not zero. Same sample ID/same request is
idempotent; conflicting requests fail. This is dashboard-callable via
rosbridge; the F4 calibration UI and harvested-sample OLS validation are not
implemented or claimed by this contract.

Core's [README](https://github.com/bagwis-research/bagwis-core/blob/feat/f3-6/README.md)
documents required launch inputs, actual service/CLI usage, persistence and
separate post-mission ODM/GeoTIFF/static XYZ output. O-1 remains a static layer
artifact, not a fabricated FinalMetrics orthomosaic URL.

### Exercised contract evidence

The 21 generated outputs passed `generate.py --check` and npm verification.
Actual ROS Jazzy build/interface inspection confirmed SegmentedDetectionArray,
FinalMetrics, NdviResult and ExportBiomassSample, including the removed
`mask_pixel_count` field's absence. This is generated/wire contract evidence,
not field validation or final stable-release approval.

Consumer checks at `v1.0.0-rc.1`: web dependency installation/typecheck passed,
but its test command exited 1 (“No test files found”), not a behavioral-test
pass. Airborne's independent Jazzy workspace built six packages and reported
38 tests with zero errors/failures and two skipped. Core's pinned-submodule
workspace built two packages and reported 631 tests with zero errors/failures
and six skipped. Final replay proof is separate from these build/test results.
The actual atomic three-node golden replay, same-mission restart and independent
new mission all passed, including recorded FinalMetrics/latched assumptions,
400 raw/10 admitted/10 NDVI frames, deduplicated 52/34 m² totals and the real
ExportBiomassSample service/CLI pair. M1 exported 40 kg/m², 36 m² and 1,440 kg
without invented actual weight. Evidence: `/tmp/bagwis_f3_6/report.txt` and
`restart-service-report.json`; stable release and field acceptance remain separate.


