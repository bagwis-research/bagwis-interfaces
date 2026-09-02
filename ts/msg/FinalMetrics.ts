// THIS FILE IS GENERATED. DO NOT EDIT.
//
// Source:    topics/registry.yaml and msg/*.msg
// Generator: scripts/generate.py
//
// Edit the source and re-run scripts/generate.py. CI fails if the committed
// output does not match what the generator produces (FR-IF-03, FR-IF-06).

import type { GeoPoint, Header } from "./_external";
import type { ObstructionCluster } from "./ObstructionCluster";

export interface FinalMetrics {
  header: Header;
  mission_id: string;
  /** "Tumana Bridge" | "Marikina Bridge" */
  segment_name: string;
  /** metric cards, one per choke-point */
  clusters: ObstructionCluster[];
  total_hyacinth_area_m2: number;
  total_waste_area_m2: number;
  total_volume_m3: number;
  total_truck_loads: number;
  total_wet_biomass_kg: number;
  max_rwor_pct: number;
  max_rwor_location: GeoPoint;
  /** flood early warning for MCDRRMO */
  rwor_alert_active: boolean;
  kde_lat: number[];
  kde_lon: number[];
  kde_weight: number[];
  segment_covered_m: number;
  frames_inferred: number;
}
