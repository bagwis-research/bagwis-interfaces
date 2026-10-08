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
  /** sorted observed IDs, including 255; aligned with class_area_m2 */
  class_ids: number[];
  /** per-class spatial union area, NaN if unmeasured */
  class_area_m2: number[];
  centroid: GeoPoint;
  hull: GeoPoint[];
  /** O-3: union across all class layers, not their sum */
  area_m2: number;
  /** O-4: classes 1-4 union area x mat depth */
  volume_m3: number;
  /** O-5: waste volume / truck capacity; fractional equivalents */
  truck_loads: number;
  /** O-6: class-0 union area x hyacinth density, even without NIR */
  wet_biomass_kg: number;
  /** O-7: class-0 obstruction only */
  rwor_pct: number;
  /** RWOR denominator, for auditability */
  river_width_m: number;
  /** dominant_class_id == 0; does not determine mixed-layer metrics */
  is_organic: boolean;
  first_seen: Time;
  last_seen: Time;
}
