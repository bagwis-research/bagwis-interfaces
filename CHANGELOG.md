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
