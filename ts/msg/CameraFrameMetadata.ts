// THIS FILE IS GENERATED. DO NOT EDIT.
//
// Source:    topics/registry.yaml and msg/*.msg
// Generator: scripts/generate.py
//
// Edit the source and re-run scripts/generate.py. CI fails if the committed
// output does not match what the generator produces (FR-IF-03, FR-IF-06).

import type { Header } from "./_external";

export const CameraFrameMetadata_TIME_REFERENCE_UNKNOWN = 0;
export const CameraFrameMetadata_TIME_REFERENCE_EXPOSURE_START = 1;
export const CameraFrameMetadata_TIME_REFERENCE_EXPOSURE_END = 2;

export interface CameraFrameMetadata {
  header: Header;
  sequence: number;
  /** file_replay for offline recordings; never claims live hardware */
  source: string;
  /** original recorded clock name, e.g. ros or monotonic */
  source_clock: string;
  /** original source clock value, not publication time */
  source_timestamp_ns: number;
  timestamp_reference: number;
  encoding: string;
  sample_bit_depth: number;
  /** visible_rgb, unfiltered_noir, or nir */
  spectral_band: string;
  /** NaN if unknown */
  exposure_us: number;
  /** multiplicative factor, not register code; NaN if unknown */
  analogue_gain: number;
  /** native sample units; NaN if unknown */
  black_level: number;
  /** native sample units; NaN if unknown */
  white_level: number;
  radiometry_valid: boolean;
  /** radiometric provenance ID; empty if absent, not intrinsic calibration */
  calibration_id: string;
}
