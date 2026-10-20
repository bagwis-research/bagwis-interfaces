// THIS FILE IS GENERATED. DO NOT EDIT.
//
// Source:    topics/registry.yaml and msg/*.msg
// Generator: scripts/generate.py
//
// Edit the source and re-run scripts/generate.py. CI fails if the committed
// output does not match what the generator produces (FR-IF-03, FR-IF-06).

import type { Header } from "./_external";

export interface AirborneHealth {
  header: Header;
  /** aggregate host utilization over two proc-stat samples */
  cpu_pct: number;
  /** configured CPU/SoC thermal-zone Celsius reading */
  temp_c: number;
  /** signed remaining chrony correction vs ground, positive = local slow */
  clock_offset_ms: number;
  /** filesystem bytes available to the running user */
  storage_free_bytes: number;
  active_warnings: string[];
}
