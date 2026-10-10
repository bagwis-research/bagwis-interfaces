// THIS FILE IS GENERATED. DO NOT EDIT.
//
// Source:    topics/registry.yaml and msg/*.msg
// Generator: scripts/generate.py
//
// Edit the source and re-run scripts/generate.py. CI fails if the committed
// output does not match what the generator produces (FR-IF-03, FR-IF-06).

import type { Header } from "./_external";

export const SystemHealth_LINK_OK = 0;
export const SystemHealth_LINK_DEGRADED = 1;
export const SystemHealth_LINK_LOST = 2;
export const SystemHealth_BACKEND_ONNX = 0;
export const SystemHealth_BACKEND_RKNN = 1;
/** no trustworthy producer reported a backend (1.1.0) */
export const SystemHealth_BACKEND_UNKNOWN = 255;

export interface SystemHealth {
  header: Header;
  link_rssi_dbm: number;
  downlink_fps: number;
  /** mean processing latency, per Statistical Treatment */
  inference_latency_ms: number;
  end_to_end_latency_ms: number;
  /** current FOV / ground_speed result */
  sampling_interval_s: number;
  fov_footprint_m: number;
  /** cumulative admitted detection sets */
  admitted_frames: number;
  /** admissions dropped under downstream pressure, 0..1 */
  shed_rate: number;
  master_cpu_pct: number;
  master_temp_c: number;
  slave_cpu_pct: number;
  slave_temp_c: number;
  clock_offset_ms: number;
  battery_voltage: number;
  battery_remaining_pct: number;
  gps_fix_type: number;
  gps_satellites: number;
  /** 0 OK - 1 DEGRADED - 2 LOST */
  link_state: number;
  /** 0 ONNX - 1 RKNN - 255 UNKNOWN */
  inference_backend: number;
  nir_available: boolean;
  lidar_available: boolean;
  active_warnings: string[];
}
