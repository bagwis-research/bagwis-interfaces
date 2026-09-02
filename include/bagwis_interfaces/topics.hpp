// THIS FILE IS GENERATED. DO NOT EDIT.
//
// Source:    topics/registry.yaml and msg/*.msg
// Generator: scripts/generate.py
//
// Edit the source and re-run scripts/generate.py. CI fails if the committed
// output does not match what the generator produces (FR-IF-03, FR-IF-06).

#ifndef BAGWIS_INTERFACES__TOPICS_HPP_
#define BAGWIS_INTERFACES__TOPICS_HPP_

namespace bagwis
{
namespace topics
{

/// intra-process only -- never crosses DDS (C-01)
/// Type: sensor_msgs/msg/Image
inline constexpr char CAMERA_IMAGE_RAW[] = "/camera/image_raw";

/// image_transport compressed plugin -- the only video crossing the radio link
/// Type: sensor_msgs/msg/CompressedImage
inline constexpr char CAMERA_IMAGE_RAW_COMPRESSED[] = "/camera/image_raw/compressed";

/// Type: sensor_msgs/msg/Image
inline constexpr char CAMERA_IMAGE_PROCESSED[] = "/camera/image_processed";

/// intrinsics for GSD
/// Type: sensor_msgs/msg/CameraInfo
inline constexpr char CAMERA_INFO[] = "/camera/camera_info";

/// C-17 -- the diagram writes Detection2dArray; the ROS type is Detection2DArray
/// Type: vision_msgs/msg/Detection2DArray
inline constexpr char AI_DETECTIONS[] = "/ai/detections";

/// C-13 -- spelling is load-bearing. Shares a header stamp with AI_DETECTIONS.
/// Type: bagwis_interfaces/msg/NdviResult
inline constexpr char AI_NDVI[] = "/ai/ndvi";

/// Type: sensor_msgs/msg/NavSatFix
inline constexpr char MAVROS_GLOBAL_POSITION[] = "/mavros/global_position/global";

/// GSD, FOV footprint
/// Type: std_msgs/msg/Float64
inline constexpr char MAVROS_REL_ALT[] = "/mavros/global_position/rel_alt";

/// ground speed -> sampling interval
/// Type: geometry_msgs/msg/TwistStamped
inline constexpr char MAVROS_VELOCITY_LOCAL[] = "/mavros/local_position/velocity_local";

/// yaw -> North/East rotation
/// Type: sensor_msgs/msg/Imu
inline constexpr char MAVROS_IMU[] = "/mavros/imu/data";

/// operator HUD
/// Type: sensor_msgs/msg/BatteryState
inline constexpr char MAVROS_BATTERY[] = "/mavros/battery";

/// VL53L1X, advisory only -- never feeds altitude or GSD (DD-CN-12)
/// Type: sensor_msgs/msg/Range
inline constexpr char MAVROS_RANGEFINDER[] = "/mavros/distance_sensor/rangefinder";

/// uplink -- waypoint guard vetoes >120 m AGL (T1.2.5)
/// Type: mavros_msgs/msg/WaypointList
inline constexpr char MAVROS_WAYPOINTS[] = "/mavros/mission/waypoints";

/// Type: bagwis_interfaces/msg/FinalMetrics
inline constexpr char DASHBOARD_FINAL_METRICS[] = "/dashboard/final_metrics";

/// independent of the perception chain (DD-CN-10)
/// Type: bagwis_interfaces/msg/SafetyAlert
inline constexpr char DASHBOARD_SAFETY_ALERTS[] = "/dashboard/safety_alerts";

/// NEW -- not named in SRS-00 SS3; justified by FR-CN-67 and SADD-04 healthStore.ts
/// Type: bagwis_interfaces/msg/SystemHealth
inline constexpr char DASHBOARD_SYSTEM_HEALTH[] = "/dashboard/system_health";

/// NEW -- not named in SRS-00 SS3; justified by FR-CN-47 and FR-WEB-21. Latched.
/// Type: bagwis_interfaces/msg/AnalyticsAssumptions
inline constexpr char DASHBOARD_ASSUMPTIONS[] = "/dashboard/assumptions";

}  // namespace topics

namespace services
{

/// Type: bagwis_interfaces/srv/StartMission
inline constexpr char MISSION_START[] = "/mission/start";

/// Type: bagwis_interfaces/srv/StopMission
inline constexpr char MISSION_STOP[] = "/mission/stop";

/// Type: bagwis_interfaces/srv/GetMissionState
inline constexpr char MISSION_STATE[] = "/mission/state";

}  // namespace services
}  // namespace bagwis

#endif  // BAGWIS_INTERFACES__TOPICS_HPP_
