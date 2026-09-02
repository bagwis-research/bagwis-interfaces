// THIS FILE IS GENERATED. DO NOT EDIT.
//
// Source:    topics/registry.yaml and msg/*.msg
// Generator: scripts/generate.py
//
// Edit the source and re-run scripts/generate.py. CI fails if the committed
// output does not match what the generator produces (FR-IF-03, FR-IF-06).

import type { GeoPoint, Header } from "./_external";

export interface GeoDetection {
  header: Header;
  cluster_id: string;
  /** Table 4 detection map, 0..4 */
  class_id: number;
  class_name: string;
  confidence: number;
  /** WGS84 */
  centroid: GeoPoint;
  /** footprint projected to WGS84 */
  polygon: GeoPoint[];
  /** Px, for Area = Px x GSD^2 */
  pixel_count: number;
  gsd_m_px: number;
  /** O-3 */
  area_m2: number;
  max_length_m: number;
  /** NaN when nir_available is false */
  mean_ndvi: number;
  /** FOV length for this sampling interval */
  fov_footprint_m: number;
}
