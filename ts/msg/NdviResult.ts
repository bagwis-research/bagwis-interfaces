// THIS FILE IS GENERATED. DO NOT EDIT.
//
// Source:    topics/registry.yaml and msg/*.msg
// Generator: scripts/generate.py
//
// Edit the source and re-run scripts/generate.py. CI fails if the committed
// output does not match what the generator produces (FR-IF-03, FR-IF-06).

import type { Header } from "./_external";

export interface NdviResult {
  header: Header;
  /** over the vegetation mask */
  mean_ndvi: number;
  /** threshold applied, for auditability */
  vegetation_threshold: number;
  /** Px for the hyacinth mask */
  vegetation_pixel_count: number;
  /** per-instance mean NDVI, index-aligned to detections */
  mask_ndvi: number[];
  /** per-instance Px, index-aligned to detections */
  mask_pixel_count: number[];
  /** false -> all NDVI fields are meaningless */
  nir_available: boolean;
  /** homography state: ok | degraded | unavailable */
  registration_status: string;
}
