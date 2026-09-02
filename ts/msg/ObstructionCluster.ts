// THIS FILE IS GENERATED. DO NOT EDIT.
//
// Source:    topics/registry.yaml and msg/*.msg
// Generator: scripts/generate.py
//
// Edit the source and re-run scripts/generate.py. CI fails if the committed
// output does not match what the generator produces (FR-IF-03, FR-IF-06).

import type { GeoPoint, Time } from "./_external";

export interface ObstructionCluster {
  cluster_id: string;
  dominant_class_id: number;
  observation_count: number;
  centroid: GeoPoint;
  hull: GeoPoint[];
  /** O-3 */
  area_m2: number;
  /** O-4  = area_m2 x 0.15 */
  volume_m3: number;
  /** O-5  = volume_m3 / 6.0 */
  truck_loads: number;
  /** O-6  = area_m2 x 40.0, hyacinth only; 0.0 otherwise */
  wet_biomass_kg: number;
  /** O-7 */
  rwor_pct: number;
  /** RWOR denominator, for auditability */
  river_width_m: number;
  /** true -> O-6/O-7 apply; false -> O-3/O-4/O-5 apply */
  is_organic: boolean;
  first_seen: Time;
  last_seen: Time;
}
