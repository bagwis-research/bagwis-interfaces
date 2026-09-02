// THIS FILE IS GENERATED. DO NOT EDIT.
//
// Source:    topics/registry.yaml and msg/*.msg
// Generator: scripts/generate.py
//
// Edit the source and re-run scripts/generate.py. CI fails if the committed
// output does not match what the generator produces (FR-IF-03, FR-IF-06).

import type { Header } from "./_external";

export interface AnalyticsAssumptions {
  header: Header;
  /** D_avg,      default 0.15 */
  mat_depth_m: number;
  /** V_truck,    default 6.0 */
  truck_capacity_m3: number;
  /** W_density,  default 40.0 */
  hyacinth_density_kg_m2: number;
  confidence_threshold: number;
  kde_bandwidth_m: number;
  vegetation_ndvi_threshold: number;
  /** subtracted from barometric relative altitude */
  launch_to_water_offset_m: number;
  /** artifact bundle tag */
  model_version: string;
  citation_note: string;
}
