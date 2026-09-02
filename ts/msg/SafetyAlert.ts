// THIS FILE IS GENERATED. DO NOT EDIT.
//
// Source:    topics/registry.yaml and msg/*.msg
// Generator: scripts/generate.py
//
// Edit the source and re-run scripts/generate.py. CI fails if the committed
// output does not match what the generator produces (FR-IF-03, FR-IF-06).

import type { GeoPoint, Header, Time } from "./_external";

export const SafetyAlert_LEVEL_INFO = 0;
export const SafetyAlert_LEVEL_CAUTION = 1;
export const SafetyAlert_LEVEL_WARNING = 2;
export const SafetyAlert_LEVEL_CRITICAL = 3;

export interface SafetyAlert {
  header: Header;
  level: number;
  /** proximity | sensor_fault | out_of_range | stale */
  alert_type: string;
  /** from sensor_msgs/Range */
  measured_range_m: number;
  /** sensor floor, from Range.min_range */
  min_valid_range_m: number;
  /** sensor ceiling, from Range.max_range -- see C-16 */
  max_valid_range_m: number;
  /** false when altitude exceeds sensor capability */
  reading_in_range: boolean;
  /** where the alert fired */
  location: GeoPoint;
  /** plain-language text for the operator */
  message: string;
  raised_at: Time;
}
