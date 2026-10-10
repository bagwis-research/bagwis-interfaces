# Changelog

All notable changes to `bagwis_interfaces`.

Versioning follows FR-IF-04 and FR-IF-05:

| Change | Bump | Also required |
|---|---|---|
| Field or message addition | **minor** | — |
| Field rename, removal, or type change | **major** | Name every affected consumer below |
| Comment, doc, or generator-only change | **patch** | — |

Consumers pin a tag, never a branch. CI fails when a file under `msg/` or `srv/`
changes without a `<version>` bump in `package.xml` (FR-IF-07).

---

## [Unreleased] — 1.0.1

Registry-only change: the QoS class of four topics. No `msg/` or `srv/` file
moves, so the wire format is identical and this is a patch under FR-IF-04/05.

### Changed

- New QoS class `image_stream` (BEST_EFFORT, KEEP_LAST 1) for
  `CAMERA_IMAGE_RAW`, `CAMERA_IMAGE_RAW_COMPRESSED`, `CAMERA_IMAGE_PROCESSED`
  and `AI_DETECTIONS_RAW`, which were `sensor_data` (KEEP_LAST 5). A frame or
  a per-frame inference result that is already stale is worth less than the
  next one, and a queue deeper than one turns packet loss on the radio link
  into latency (DD-AN-3). MAVROS telemetry stays `sensor_data`: its short
  history is what lets a GPS reading taken just before a capture stamp still
  pair with the frame.
- The registry header now documents the four QoS classes and the policy each
  maps to, so a class name is a contract rather than a label.

### Consumers

`bagwis-core` maps `image_stream` in `infrastructure/qos.py` and re-pins to
pick it up. `bagwis-airborne` has no nodes yet; when `v4l2_camera_node` and the
`image_transport` publisher land, they read the class from here (FR-IF-03).
`bagwis-web` subscribes through rosbridge, which does not expose DDS QoS, so no
change there.

---

## [1.0.0-rc.1] — 2026-10-08

Breaking F3.6 shared contract. ROS and npm package versions are both **1.0.0**;
the immutable coordinated testing tag is **`v1.0.0-rc.1`**, not stable release.
Dependency: [draft PR #5](https://github.com/bagwis-research/bagwis-interfaces/pull/5),
with both JoshuaHM-p4 and EarlClydeeee required as contract reviewers.

### Breaking changes

- `AI_DETECTIONS_RAW` and `AI_DETECTIONS` retain topic names/QoS but replace
  Detection2DArray with atomic `SegmentedDetectionArray`: full image dimensions,
  capture header, primitive class/confidence/box fields and canonical lossless
  row-major foreground `[start,length,...]` runs. Positive, sorted, disjoint,
  row-contained/coalesced runs are mandatory for every nonempty detection.
  Producers undo letterboxing on masks and boxes and select the best class.
  Valid empty frames remain valid; invalid/missing masks reject the frame.
  No old-message shim or separate mask topic is provided; old bags must be
  regenerated.
- Removed `NdviResult.mask_pixel_count`. Segmentation count comes only from run
  lengths; NDVI retains index-aligned values/availability. Absent NIR leaves
  NDVI NaN, not area/biomass unavailable when class-0 masks are measured.
- `FinalMetrics.kde_lat` and `kde_lon` change from float32 to float64 to retain
  WGS84 precision.

### Added and clarified

- Equal-length sorted per-class area arrays in FinalMetrics/ObstructionCluster.
  Areas are exact spatial mask unions, not box/hull areas or observation sums.
  Class 0 supplies hyacinth biomass/RWOR; classes 1–4 supply waste
  volume/fractional truck equivalents. Mixed clusters use relevant layers;
  unknown 255 remains visible but is excluded from those named buckets.
  `is_organic` denotes dominant class 0; wood gets no wet biomass.
  Applicable incomplete metrics are NaN, non-applicable metrics zero.
- AnalyticsAssumptions adds RWOR alert threshold, profile source/revision,
  corrected added launch offset and policy/provenance disclosures.
- GeoreferencingStatus adds `rejected_invalid_mask`.
- `ExportBiomassSample` and registered `BIOMASS_EXPORT` service:
  caller-supplied exact capture/harvest location/radius, optional actual kg/m²,
  explicit success/error/CSV response. Core persists idempotent paired records
  and separates predicted kg/m² from predicted total kg; no fabricated
  harvest measurements or calibration UI are implied.
- Registry now includes the raw-frame counting subscription of
  georeferencing_node, the biomass export server and both actual dashboard
  publishers. README documents canonical runs and all affected metric semantics.

### Consumers and release order

All affected consumers — **bagwis-core, bagwis-web, bagwis-airborne** — pin
`v1.0.0-rc.1`. Core migrates admission/NDVI/georeferencing and synthetic bag
production together. Web/airborne require pin/generated-type consistency;
this release does not add a dashboard calibration UI or perception producer.
Both owners must approve and merge the interfaces contract before publishing
stable `v1.0.0`, followed by coordinated consumer stable pin updates.
No automatic merge, stable tag or ownership/gate change is authorized.

### Exercised evidence

- Generator check passed for 21 outputs; npm generated-type verification passed.
- Actual Jazzy build and generated ROS interface inspection confirmed the new
  detection/metric/service shapes and removal of the NDVI count field.
- rc.1 consumer compilation: web dependency install/typecheck passed; web test
  command exited 1 (“No test files found”), with no existing behavioral suite.
  Separate airborne Jazzy build: six packages, 38 tests, zero errors/failures,
  two skipped. Core pinned-submodule build: two packages, 631 tests,
  zero errors/failures, six skipped.
- Atomic Jazzy golden replay, same-mission restart and independent mission passed:
  recorded metrics/latched assumptions, 400 raw/10 admitted/10 NDVI frames and
  deduplicated class totals. Real M1 export service and offline CLI agreed on
  40 kg/m², 36 m² and 1,440 kg, blank unavailable measurements, idempotency and
  conflict/far-location rejection. Host reports: `/tmp/bagwis_f3_6`.
- Software/wire evidence is not field accuracy or harvested biomass validation.

---


## [0.3.0] — 2026-10-06

Additions for `georeferencing_node` (bagwis-core F3.5). Minor bump under
FR-IF-04/05: nothing is renamed or removed.

### Added

- `CORE_GEO_DETECTIONS` = `/core/geo_detections`, `GeoDetection`, published by
  `georeferencing_node`, one message per admitted detection. `GeoDetection`
  was specified in SRS-00 §4.2 with no topic; publishing it makes "detections
  resolve to lat/lon" (G3) checkable from a recording.
- `msg/GeoreferencingStatus.msg` on `CORE_GEOREFERENCING_STATUS` =
  `/core/georeferencing_status`: frames and detections georeferenced, unmatched
  detection sets and NDVI results (FR-CN-28), telemetry rejections by reason,
  and the registry's cluster count. Read by `health_node`.

### Consumers

`bagwis-core` re-pins to `v0.3.0`. `bagwis-airborne` and `bagwis-web` need no
change.

---

## [0.2.0] — 2026-10-05

Field and message additions for `dynamic_sampling_node` (F3.1). Minor bump
under FR-IF-04/05: nothing is renamed or removed.

### Added

- `AI_DETECTIONS_RAW` = `/ai/detections_raw`, `vision_msgs/msg/Detection2DArray`,
  `yolo26n_inference_node` → `dynamic_sampling_node`. SRS-00 §3 listed this
  link as "(internal)" with no name, so the sampler had nothing to subscribe to.
- `msg/AdmissionStatus.msg` on `CORE_ADMISSION_STATUS` = `/core/admission_status`:
  admission interval, footprint, admitted and shed counts, shed rate, and one
  counter per rejection reason (FR-CN-07, FR-CN-08, FR-CN-09). Published by
  `dynamic_sampling_node`, read by `health_node`.
- `SystemHealth.admitted_frames` (`uint32`) and `SystemHealth.shed_rate`
  (`float32`), which FR-CN-07 and FR-CN-09 require on the operator display.
- Registry subscribers: `dynamic_sampling_node` on `MAVROS_GLOBAL_POSITION`
  (displacement and fix status) and on `AI_NDVI` (downstream acknowledgement
  for shedding).

### Consumers

`bagwis-core` re-pins to `v0.2.0` for the sampler. `bagwis-airborne` and
`bagwis-web` need no code change; `bagwis-web` gains the two `SystemHealth`
fields in its generated types when it re-pins.

---

## [0.1.1] — 2026-09-27

Target distro moves from ROS 2 Humble to ROS 2 Jazzy. No `msg/` or `srv/`
change: the wire format, field names and topic names are identical, so this is
a patch release under FR-IF-04/05.

### Changed

- CI builds and tests against `ros:jazzy-ros-base` (amd64) and `arm64v8/ros:jazzy`
  (arm64) instead of Humble. The codegen job runs Python 3.12, matching Ubuntu
  24.04.
- `scripts/generate.py` and the generated `python/topics.py` use single-quoted
  string literals. Jazzy's `ament_flake8` enforces flake8-quotes (Q000), which
  the Humble build did not; without this `colcon test` reports 459 lint
  failures under Jazzy. `topics.py` exports exactly the same names and values as 0.1.0;
  `topics.hpp` and the TypeScript output are unchanged.
- `scripts/generate.py` import order fixed (flake8 I100, Google style).
- `package.xml` dependency comment no longer names a specific distro.

### Consumers

`bagwis-airborne`, `bagwis-core` and `bagwis-web` keep building against the
`v0.1.0` tag until they re-pin. Re-pinning to `v0.1.1` needs no code change on
their side, but a consumer's own CI must move to Jazzy at the same time.

---

## [0.1.0] — 2026-09-02

First real release. Supersedes the `v0.1.0` tag that previously pointed at a
README-only commit; the tag was moved onto this commit and `bagwis-core`
re-pinned. No consumer had built against the stub.

### Added

- Eight messages, transcribed from SRS-00 §4: `NdviResult`, `GeoDetection`,
  `ObstructionCluster`, `FinalMetrics`, `SafetyAlert`, `AnalyticsAssumptions`,
  `SystemHealth`, `FlightParams`.
- Three services, from SRS-00 §4.9: `StartMission`, `StopMission`,
  `GetMissionState`.
- `topics/registry.yaml` — the canonical topic registry (FR-IF-03). Seventeen
  topics and three services, each with its message type, publisher, subscribers
  and QoS profile.
- `scripts/generate.py` — stdlib-only generator emitting `topics.hpp`,
  `topics.py`, `ts/topics.ts` and `ts/msg/*.ts` from that registry (FR-IF-03,
  FR-IF-06). Output is committed; CI verifies it with `--check`.

### Deviations from SRS-00 §4

Recorded here rather than silently applied, because SRS-00 §2 and §4 disagree
and consumers need to know which won.

1. **`AnalyticsAssumptions` gains `std_msgs/Header header`.** FR-IF-08 requires
   every message to carry a Header; §4.6 lists none. This message is published
   (latched) on its own topic, so FR-IF-08 applies and the field was added.

2. **`ObstructionCluster` has no Header**, against a literal reading of
   FR-IF-08. It is nested inside `FinalMetrics.clusters[]` and never published
   on a topic of its own; `first_seen` / `last_seen` already carry its time
   extent. Adding a Header would duplicate `FinalMetrics.header` on every
   element of an unbounded array.

3. **`FlightParams` has no Header**, for the same reason: it is nested inside
   `StartMission.srv` and never published.

   *Follow-up:* FR-IF-08 should be reworded to "every **published** message",
   which is what its stated rationale — measurement-time stamping for
   georeferencing accuracy — actually requires.

4. **`SystemHealth` gains named constants** `LINK_OK`/`LINK_DEGRADED`/`LINK_LOST`
   and `BACKEND_ONNX`/`BACKEND_RKNN`. §4.7 gave these enumerations as trailing
   comments on `link_state` and `inference_backend`; they are now `uint8`
   constants so consumers compare against a symbol instead of a bare integer.
   Purely additive — the field types and order are unchanged.

### Topic names added beyond SRS-00 §3

Both messages are specified in §4 but no topic is named for either. The names
below are used by the registry and need a corresponding row added to SRS-00 §3.

| Topic | Message | Justification |
|---|---|---|
| `/dashboard/system_health` | `SystemHealth` | FR-CN-67 (publish ≥ 1 Hz); SADD-04 `healthStore.ts` |
| `/dashboard/assumptions` | `AnalyticsAssumptions` | FR-CN-47, FR-WEB-21. Latched (`transient_local`). |

### Dependencies

`package.xml` declares `std_msgs`, `geographic_msgs` and `builtin_interfaces` —
the only packages whose types appear in a field.

`sensor_msgs`, `vision_msgs`, `geometry_msgs` and `mavros_msgs` appear in the
SRS-00 §3 topic table but in no field here, so they are **not** declared.
Depending on them would force `ros-humble-mavros-msgs` and
`ros-humble-vision-msgs` onto every machine that builds this package, the Pi
Zero 2 W included, to satisfy a dependency nothing uses. Their types are
recorded in `topics/registry.yaml`, and each consumer declares what it actually
subscribes to.
