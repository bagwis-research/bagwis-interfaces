// THIS FILE IS GENERATED. DO NOT EDIT.
//
// Source:    topics/registry.yaml and msg/*.msg
// Generator: scripts/generate.py
//
// Edit the source and re-run scripts/generate.py. CI fails if the committed
// output does not match what the generator produces (FR-IF-03, FR-IF-06).

import type { GeoPoint, Time } from "../msg/_external";

export interface ExportBiomassSampleRequest {
  sample_id: string;
  capture_stamp: Time;
  location: GeoPoint;
  match_radius_m: number;
  actual_available: boolean;
  actual_kg_m2: number;
}

export interface ExportBiomassSampleResponse {
  success: boolean;
  message: string;
  csv_path: string;
}
