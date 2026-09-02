// THIS FILE IS GENERATED. DO NOT EDIT.
//
// Source:    topics/registry.yaml and msg/*.msg
// Generator: scripts/generate.py
//
// Edit the source and re-run scripts/generate.py. CI fails if the committed
// output does not match what the generator produces (FR-IF-03, FR-IF-06).

/** intra-process only -- never crosses DDS (C-01) */
/** Type: `sensor_msgs/msg/Image` */
export const CAMERA_IMAGE_RAW = "/camera/image_raw" as const;

/** image_transport compressed plugin -- the only video crossing the radio link */
/** Type: `sensor_msgs/msg/CompressedImage` */
export const CAMERA_IMAGE_RAW_COMPRESSED = "/camera/image_raw/compressed" as const;

/** Type: `sensor_msgs/msg/Image` */
export const CAMERA_IMAGE_PROCESSED = "/camera/image_processed" as const;

/** intrinsics for GSD */
/** Type: `sensor_msgs/msg/CameraInfo` */
export const CAMERA_INFO = "/camera/camera_info" as const;

/** C-17 -- the diagram writes Detection2dArray; the ROS type is Detection2DArray */
/** Type: `vision_msgs/msg/Detection2DArray` */
export const AI_DETECTIONS = "/ai/detections" as const;

/** C-13 -- spelling is load-bearing. Shares a header stamp with AI_DETECTIONS. */
/** Type: `bagwis_interfaces/msg/NdviResult` */
export const AI_NDVI = "/ai/ndvi" as const;

/** Type: `sensor_msgs/msg/NavSatFix` */
export const MAVROS_GLOBAL_POSITION = "/mavros/global_position/global" as const;

/** GSD, FOV footprint */
/** Type: `std_msgs/msg/Float64` */
export const MAVROS_REL_ALT = "/mavros/global_position/rel_alt" as const;

/** ground speed -> sampling interval */
/** Type: `geometry_msgs/msg/TwistStamped` */
export const MAVROS_VELOCITY_LOCAL = "/mavros/local_position/velocity_local" as const;

/** yaw -> North/East rotation */
/** Type: `sensor_msgs/msg/Imu` */
export const MAVROS_IMU = "/mavros/imu/data" as const;

/** operator HUD */
/** Type: `sensor_msgs/msg/BatteryState` */
export const MAVROS_BATTERY = "/mavros/battery" as const;

/** VL53L1X, advisory only -- never feeds altitude or GSD (DD-CN-12) */
/** Type: `sensor_msgs/msg/Range` */
export const MAVROS_RANGEFINDER = "/mavros/distance_sensor/rangefinder" as const;

/** uplink -- waypoint guard vetoes >120 m AGL (T1.2.5) */
/** Type: `mavros_msgs/msg/WaypointList` */
export const MAVROS_WAYPOINTS = "/mavros/mission/waypoints" as const;

/** Type: `bagwis_interfaces/msg/FinalMetrics` */
export const DASHBOARD_FINAL_METRICS = "/dashboard/final_metrics" as const;

/** independent of the perception chain (DD-CN-10) */
/** Type: `bagwis_interfaces/msg/SafetyAlert` */
export const DASHBOARD_SAFETY_ALERTS = "/dashboard/safety_alerts" as const;

/** NEW -- not named in SRS-00 SS3; justified by FR-CN-67 and SADD-04 healthStore.ts */
/** Type: `bagwis_interfaces/msg/SystemHealth` */
export const DASHBOARD_SYSTEM_HEALTH = "/dashboard/system_health" as const;

/** NEW -- not named in SRS-00 SS3; justified by FR-CN-47 and FR-WEB-21. Latched. */
/** Type: `bagwis_interfaces/msg/AnalyticsAssumptions` */
export const DASHBOARD_ASSUMPTIONS = "/dashboard/assumptions" as const;

/** Type: `bagwis_interfaces/srv/StartMission` */
export const MISSION_START = "/mission/start" as const;

/** Type: `bagwis_interfaces/srv/StopMission` */
export const MISSION_STOP = "/mission/stop" as const;

/** Type: `bagwis_interfaces/srv/GetMissionState` */
export const MISSION_STATE = "/mission/state" as const;

/** Every topic name, for exhaustiveness checks and the mock harness. */
export const ALL_TOPICS = [
  CAMERA_IMAGE_RAW,
  CAMERA_IMAGE_RAW_COMPRESSED,
  CAMERA_IMAGE_PROCESSED,
  CAMERA_INFO,
  AI_DETECTIONS,
  AI_NDVI,
  MAVROS_GLOBAL_POSITION,
  MAVROS_REL_ALT,
  MAVROS_VELOCITY_LOCAL,
  MAVROS_IMU,
  MAVROS_BATTERY,
  MAVROS_RANGEFINDER,
  MAVROS_WAYPOINTS,
  DASHBOARD_FINAL_METRICS,
  DASHBOARD_SAFETY_ALERTS,
  DASHBOARD_SYSTEM_HEALTH,
  DASHBOARD_ASSUMPTIONS,
] as const;

export type TopicName = (typeof ALL_TOPICS)[number];
