// THIS FILE IS GENERATED. DO NOT EDIT.
//
// Source:    topics/registry.yaml and msg/*.msg
// Generator: scripts/generate.py
//
// Edit the source and re-run scripts/generate.py. CI fails if the committed
// output does not match what the generator produces (FR-IF-03, FR-IF-06).

import type { Header } from "./_external";

export interface GeoreferencingStatus {
  header: Header;
  /** paired frames that produced GeoDetections */
  frames_georeferenced: number;
  detections_georeferenced: number;
  /** admitted sets /ai/ndvi never answered */
  unmatched_detections: number;
  /** NDVI results with no detection set */
  unmatched_ndvi: number;
  rejected_no_fix: number;
  /** including frames with no telemetry at all */
  rejected_stale_telemetry: number;
  /** obstruction clusters in the mission registry */
  clusters: number;
}
