# Mission parameters supplied with StartMission. SRS-00 SS4.8.
#
# No std_msgs/Header: nested inside StartMission.srv only, never published on a
# topic. See CHANGELOG "Deviations from SRS-00 SS4".
#
# target_altitude_m is hard-capped at 120 m by the waypoint guard (T1.2.5),
# per CAAP PCAR Part 11.

float32  target_altitude_m          # 40..80, hard-capped at 120 (CAAP PCAR Part 11)
float32  target_speed_ms            # default 5.35 (Lanca et al., 2025)
float32  launch_to_water_offset_m
string   segment_name
