// THIS FILE IS GENERATED. DO NOT EDIT.
//
// Source:    topics/registry.yaml and msg/*.msg
// Generator: scripts/generate.py
//
// Edit the source and re-run scripts/generate.py. CI fails if the committed
// output does not match what the generator produces (FR-IF-03, FR-IF-06).

import type { Header } from "./_external";
import type { SegmentedDetection } from "./SegmentedDetection";

export interface SegmentedDetectionArray {
  /** capture stamp, undistorted full-resolution camera frame */
  header: Header;
  image_width_px: number;
  image_height_px: number;
  detections: SegmentedDetection[];
}
