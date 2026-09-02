// THIS FILE IS GENERATED. DO NOT EDIT.
//
// Source:    topics/registry.yaml and msg/*.msg
// Generator: scripts/generate.py
//
// Edit the source and re-run scripts/generate.py. CI fails if the committed
// output does not match what the generator produces (FR-IF-03, FR-IF-06).
//
// Shapes owned by other ROS packages. Declared here rather than generated,
// because the dashboard has no ROS toolchain to generate them from and these
// three definitions are stable across every ROS 2 distribution.

/** builtin_interfaces/Time */
export interface Time {
  sec: number;
  nanosec: number;
}

/** std_msgs/Header -- stamp is the time of physical measurement (FR-IF-08). */
export interface Header {
  stamp: Time;
  frame_id: string;
}

/** geographic_msgs/GeoPoint -- WGS84. */
export interface GeoPoint {
  latitude: number;
  longitude: number;
  altitude: number;
}
