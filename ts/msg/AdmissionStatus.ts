// THIS FILE IS GENERATED. DO NOT EDIT.
//
// Source:    topics/registry.yaml and msg/*.msg
// Generator: scripts/generate.py
//
// Edit the source and re-run scripts/generate.py. CI fails if the committed
// output does not match what the generator produces (FR-IF-03, FR-IF-06).

import type { Header } from "./_external";

export interface AdmissionStatus {
  header: Header;
  /** FOV / ground speed; +inf while hovering */
  sampling_interval_s: number;
  /** along-track footprint at the current height above water */
  fov_footprint_m: number;
  admitted_frames: number;
  shed_frames: number;
  /** shed / (admitted + shed); 0 when both are 0 */
  shed_rate: number;
  /** FR-CN-08 */
  rejected_no_fix: number;
  /** FR-CN-08, including frames with no telemetry at all */
  rejected_stale_telemetry: number;
  /** FR-CN-05 */
  rejected_hover: number;
  /** footprint has not moved off the last admitted one */
  rejected_not_cleared: number;
  /** admitted frames /ai/ndvi never answered within the timeout */
  downstream_timeouts: number;
}
