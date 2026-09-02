// THIS FILE IS GENERATED. DO NOT EDIT.
//
// Source:    topics/registry.yaml and msg/*.msg
// Generator: scripts/generate.py
//
// Edit the source and re-run scripts/generate.py. CI fails if the committed
// output does not match what the generator produces (FR-IF-03, FR-IF-06).

import type { FlightParams } from "../msg/FlightParams";

export interface StartMissionRequest {
  mission_id: string;
  params: FlightParams;
}

export interface StartMissionResponse {
  ok: boolean;
  message: string;
}
