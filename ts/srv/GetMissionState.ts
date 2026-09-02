// THIS FILE IS GENERATED. DO NOT EDIT.
//
// Source:    topics/registry.yaml and msg/*.msg
// Generator: scripts/generate.py
//
// Edit the source and re-run scripts/generate.py. CI fails if the committed
// output does not match what the generator produces (FR-IF-03, FR-IF-06).

import type { FinalMetrics } from "../msg/FinalMetrics";

export interface GetMissionStateRequest {
  mission_id: string;
}

export interface GetMissionStateResponse {
  snapshot: FinalMetrics;
  ok: boolean;
}
