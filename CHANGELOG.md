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
## [1.3.0-rc.1] — 2026-10-20

Additive testing candidate based on `v1.2.0-rc.2`; ROS package version is
1.3.0 and the private npm package/tag is 1.3.0-rc.1. Stable publication still
requires both interface owners.

### Added

- `AirborneHealth` and the reliable `/airborne/health` registry entry. It is a
  versioned host-measurement input from `airborne_health_node` to `health_node`;
  `health_node` remains the sole `/dashboard/system_health` publisher.
- CPU, configured thermal-zone temperature, signed chrony remaining correction,
  and storage available to the running user. Unavailable numerics stay NaN and
  warnings describe the current sample only.

### Compatibility

`SystemHealth` and existing camera wire layouts are unchanged. This candidate
intentionally retains the `v1.2.0-rc.2` camera metadata contract rather than
rebasing onto the older stable interface main. Airborne and core consumers must
pin this exact immutable tag; neither stable interface publication nor hardware
calibration/thermal qualification is implied.

---


## [1.1.0] — 2026-10-11

- Publish immutable stable `v1.1.0` from merged
  [PR #10](https://github.com/bagwis-research/bagwis-interfaces/pull/10),
  commit `1568e509b06118deff7fb25e3da6d65acede81b2`, the commit tagged
  `v1.1.0-rc.3`; the stable release is the tested prerelease, byte for byte.
  This documentation follow-up is not the tag target.
- Contents (see `[1.1.0-rc.1]` through `[1.1.0-rc.3]` below): additive F3.8
  contract (`SystemHealth.BACKEND_UNKNOWN`, the rosbridge client-monitoring
  topics, bridge/health subscription declarations) and the `image_stream` QoS
  class for the three camera frame topics, with `AI_DETECTIONS_RAW` kept in
  `sensor_data`. Nothing from `v1.0.0` is renamed or retyped.
- Core and web already pin this commit; their pins are named `v1.1.0` from
  now on. The `v1.1.0-rc.1`, `-rc.2` and `-rc.3` tags remain immutable.
- Publication was authorized by JoshuaHM-p4; no review by EarlClydeeee is
  recorded on the contract PRs (README step 4 asks for both owners). Field
  acceptance remains separate.
## [1.2.0-rc.2] — 2026-10-14

Registry-only successor to immutable `v1.2.0-rc.1`; ROS remains 1.2.0, private
npm package/tag is 1.2.0-rc.2. No message/service wire changes.

- Add `ndvi_computation_node` subscribers to native RGB compressed image and
  CameraInfo. Clarify that red radiometry uses original JPEG, not model input.
- Regenerate topic constants and coordinate airborne/isolated core testing pins.
  Protected core and web remain untouched. Stable publication still requires
  both interface owners' approvals.
- Generator freshness/TypeScript verification and Jazzy interface build passed.
  Actual camera/NDVI executables exercised mono16 plus all Bayer16 orientations:
  calibrated analytic results, exposure/gain changes, translated registration,
  class-0 mask union and unfiltered/unknown/missing NIR unavailable responses.
  This is software evidence, not physical sensor or calibration qualification.
## [1.2.0-rc.1] — 2026-10-14

Additive prerelease based on `v1.1.0`; stable publication still requires both
owners' approvals. ROS version 1.2.0; private npm version 1.2.0-rc.1.

### Added

- `CameraFrameMetadata`: capture header, per-stream sequence, explicit source
  and clock, original signed nanosecond timestamp/reference, encoding/native
  bit depth, spectral band, measured exposure/gain/levels and radiometric
  validity/provenance. Unknown controls are NaN, not invented zeroes.
- Lossless NIR compressed-frame, CameraInfo and metadata registry entries,
  plus RGB frame metadata. NIR PNG preserves native 10–16-bit sample values
  and explicit Bayer orientation; it is not the contrast/gamma-adjusted
  browser preview. Frame QoS remains best-effort depth 1; info/metadata use
  reliable depth 10.
- Generated C++, Python and TypeScript constants and metadata types.

### Fixed

- Export the canonical topic-header include directory through an interface
  target. Modern ament target consumers previously received only rosidl's
  nested generated-header path and could not include `topics.hpp`.

### Consumers and verification

`bagwis-airborne` pins this candidate for its C++ Jazzy file-replay camera
component. Existing RGB topics and wire types are unchanged. Neither the
protected `bagwis-core` checkout nor `bagwis-web` is changed; their scientific
NIR consumption is a later integration step.

Jazzy build, generated-output check and TypeScript typecheck passed. Real ROS
subscribers and the standard compressed-image decoder recovered all four
synthetic RAW10 Bayer frames exactly, with source stamps retained. Replay
does not prove physical NIR capture, calibration or NDVI.

---

## [1.1.0-rc.3] — 2026-10-10

Registry-only correction of `v1.1.0-rc.2`. No `msg/` or `srv/` file moves; the
wire format is identical. `v1.1.0-rc.2` stays immutable and is superseded by
`v1.1.0-rc.3`; stable `v1.1.0` carries both rc.2's `image_stream` class and
this change.

### Changed

- `AI_DETECTIONS_RAW` moves from `image_stream` (BEST_EFFORT, KEEP_LAST 1)
  back to `sensor_data` (BEST_EFFORT, KEEP_LAST 5). Only the three camera
  frame topics (`CAMERA_IMAGE_RAW`, `CAMERA_IMAGE_RAW_COMPRESSED`,
  `CAMERA_IMAGE_PROCESSED`) remain `image_stream`.
- Why: georeferencing counts every inferred capture stamp
  (`FinalMetrics.frames_inferred`) and the recorded bag must contain every
  one. With a depth-1 queue a set delivered in a burst (a stalled executor
  catching up, or the replay player) overwrites the previous one. On rc.2 the
  synthetic G3 replay lost exactly one of its 400 raw sets in several runs
  (399/400, `rejected_hover 99`), failing `check_g3` and bagwis-core CI. A
  stale frame is worth dropping; a counted inference result is not.
- The registry header now says `image_stream` is for camera frames only and
  lists per-frame inference output under `sensor_data`.

### Consumers

`bagwis-core` needs no mapping change (both classes already exist in
`qos.py`); its QoS test expectations for `AI_DETECTIONS_RAW` change from depth 1
to the `sensor_data` profile, and its submodule pin moves to
`v1.1.0-rc.3`. `bagwis-web` and `bagwis-airborne` are unaffected.

---

## [1.1.0-rc.2] — 2026-10-10

Registry-only change on top of 1.1.0-rc.1: the QoS class of four frame topics.
No `msg/` or `srv/` file moves, so the wire format is identical. It joins the
unreleased 1.1.0 line (main is already 1.1.0; a 1.0.1 would be lower than the
current version), so the next immutable testing tag is `v1.1.0-rc.2` and
stable `v1.1.0` carries both. Consumers must map the new class before
re-pinning (bagwis-core PR "feat(qos)").

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
pick it up; every core subscriber of these topics (sampling, georeferencing,
the bridge's MJPEG inputs, `health_node`, `mission_recorder`) reads the class
through `qos_for`. `bagwis-airborne` has no nodes yet; when `v4l2_camera_node`
and the `image_transport` publisher land, they read the class from here
(FR-IF-03). `bagwis-web` subscribes through rosbridge, which does not expose
DDS QoS, so no change there.

---

## [1.1.0-rc.1] — 2026-10-10

Additive F3.8 hosting contract (minor bump, FR-IF-05). ROS and npm package
versions are both **1.1.0**; `v1.1.0-rc.1` is the immutable coordinated
testing tag for the feature branches. Stable `v1.1.0` requires both owners'
approvals and the merged contract first (README step 4); stable consumers stay
on `v1.0.0` until then. No field, name, type or QoS of 1.0.0 changes.

### Added

- `SystemHealth.BACKEND_UNKNOWN=255`: the explicit "no trustworthy producer"
  value of `inference_backend`. `BACKEND_ONNX=0` is a real backend, not a
  default. Header comment now states the unavailable-measurement convention
  (NaN / unknown constant / `active_warnings`), which rosbridge carries to the
  dashboard as JSON `null`.
- `BRIDGE_CLIENT_COUNT` (`/client_count`, `std_msgs/msg/Int32`) and
  `BRIDGE_CONNECTED_CLIENTS` (`/connected_clients`,
  `rosbridge_msgs/msg/ConnectedClients`), transient-local, published by the
  upstream `rosbridge_server` ClientManager that `rosbridge_websocket_node`
  composes. Declared so graph conformance expects them; neither is
  browser-readable. As with every foreign type in the registry, this package
  does not depend on `rosbridge_msgs`; core declares it.
- `rosbridge_websocket_node` declared subscriber of
  `CAMERA_IMAGE_RAW_COMPRESSED`, `CAMERA_INFO` and `AI_DETECTIONS_RAW`: the
  native inputs of the `/video.mjpeg` compositor (T3.8.3). No new image topic.
- `health_node` declared subscriber of `CAMERA_IMAGE_RAW_COMPRESSED`
  (downlink_fps), `AI_DETECTIONS_RAW`, `AI_NDVI` (nir_available),
  `MAVROS_GLOBAL_POSITION` (link freshness) and `DASHBOARD_SAFETY_ALERTS`
  (lidar_available), in addition to its 1.0.0 inputs (T3.8.8).

### Consumers and release order

- bagwis-core (F3.8 branch): host, health, recorder and conformance consume
  the additions; pins `v1.1.0-rc.1` until stable.
- bagwis-web (F3.8 branch): transport treats `null` numerics as unavailable and
  compares `inference_backend` against `SystemHealth_BACKEND_UNKNOWN`; pins
  `v1.1.0-rc.1` until stable.
- bagwis-airborne: unaffected (no airborne field or topic changed).

---

## [1.0.0] — 2026-10-09

- Publish immutable stable `v1.0.0` from merged
  [PR #5](https://github.com/bagwis-research/bagwis-interfaces/pull/5),
  commit `15ed068136e5ab9d82c1b51e74a54fba103b84d6`.
- Wire contract and generated code are identical to tested `v1.0.0-rc.1`;
  generator verification and TypeScript typecheck passed on the merged commit.
- Core, web and airborne promote their submodule pins after the stable
  interfaces publication. The prerelease tag remains immutable.
- ROS and private TypeScript package versions remain 1.0.0; the package is
  consumed by Git tag, not published to npm. Field acceptance remains separate.

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
