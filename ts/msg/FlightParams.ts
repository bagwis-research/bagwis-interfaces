// THIS FILE IS GENERATED. DO NOT EDIT.
//
// Source:    topics/registry.yaml and msg/*.msg
// Generator: scripts/generate.py
//
// Edit the source and re-run scripts/generate.py. CI fails if the committed
// output does not match what the generator produces (FR-IF-03, FR-IF-06).

export interface FlightParams {
  /** 40..80, hard-capped at 120 (CAAP PCAR Part 11) */
  target_altitude_m: number;
  /** default 5.35 (Lanca et al., 2025) */
  target_speed_ms: number;
  launch_to_water_offset_m: number;
  segment_name: string;
}
