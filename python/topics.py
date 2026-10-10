"""
THIS FILE IS GENERATED. DO NOT EDIT.

Source:    topics/registry.yaml and msg/*.msg
Generator: scripts/generate.py

Edit the source and re-run scripts/generate.py. CI fails if the committed
output does not match what the generator produces (FR-IF-03, FR-IF-06).
"""

from __future__ import annotations

# --- Topics ---

# intra-process only -- never crosses DDS (C-01)
#: sensor_msgs/msg/Image
CAMERA_IMAGE_RAW = '/camera/image_raw'

# image_transport compressed plugin -- the only video crossing the radio link. rosbridge_websocket_node composites the MJPEG feed from it; health_node measures downlink_fps from receipts (1.1.0)
#: sensor_msgs/msg/CompressedImage
CAMERA_IMAGE_RAW_COMPRESSED = '/camera/image_raw/compressed'

#: sensor_msgs/msg/Image
CAMERA_IMAGE_PROCESSED = '/camera/image_processed'

# intrinsics for GSD; rosbridge_websocket_node undistorts the MJPEG frame with the same K before drawing held overlays (1.1.0)
#: sensor_msgs/msg/CameraInfo
CAMERA_INFO = '/camera/camera_info'

# every inferred frame before admission; georeferencing counts unique capture stamps only; rosbridge_websocket_node holds the latest valid set as the MJPEG overlay; health_node measures inference receipt (1.1.0)
#: bagwis_interfaces/msg/SegmentedDetectionArray
AI_DETECTIONS_RAW = '/ai/detections_raw'

# atomic admitted segmentation with lossless masks; incompatible with Detection2DArray
#: bagwis_interfaces/msg/SegmentedDetectionArray
AI_DETECTIONS = '/ai/detections'

# C-13 -- spelling is load-bearing. Shares a header stamp with AI_DETECTIONS. health_node derives nir_available from it (1.1.0)
#: bagwis_interfaces/msg/NdviResult
AI_NDVI = '/ai/ndvi'

# NEW -- not in SRS-00 SS3; FR-CN-07, FR-CN-09. health_node copies it to SystemHealth
#: bagwis_interfaces/msg/AdmissionStatus
CORE_ADMISSION_STATUS = '/core/admission_status'

# NEW -- one per admitted detection; recorded as the G3 lat/lon evidence (FR-CN-31)
#: bagwis_interfaces/msg/GeoDetection
CORE_GEO_DETECTIONS = '/core/geo_detections'

# NEW -- not in SRS-00 SS3; FR-CN-28 unmatched-set counters, cluster count
#: bagwis_interfaces/msg/GeoreferencingStatus
CORE_GEOREFERENCING_STATUS = '/core/georeferencing_status'

# health_node measures telemetry receipt age for link_state (1.1.0); NavSatFix carries no satellite count or MAVLink fix type
#: sensor_msgs/msg/NavSatFix
MAVROS_GLOBAL_POSITION = '/mavros/global_position/global'

# GSD, FOV footprint
#: std_msgs/msg/Float64
MAVROS_REL_ALT = '/mavros/global_position/rel_alt'

# ground speed -> sampling interval
#: geometry_msgs/msg/TwistStamped
MAVROS_VELOCITY_LOCAL = '/mavros/local_position/velocity_local'

# yaw -> North/East rotation
#: sensor_msgs/msg/Imu
MAVROS_IMU = '/mavros/imu/data'

# operator HUD
#: sensor_msgs/msg/BatteryState
MAVROS_BATTERY = '/mavros/battery'

# VL53L1X, advisory only -- never feeds altitude or GSD (DD-CN-12)
#: sensor_msgs/msg/Range
MAVROS_RANGEFINDER = '/mavros/distance_sensor/rangefinder'

# uplink -- waypoint guard vetoes >120 m AGL (T1.2.5)
#: mavros_msgs/msg/WaypointList
MAVROS_WAYPOINTS = '/mavros/mission/waypoints'

#: bagwis_interfaces/msg/FinalMetrics
DASHBOARD_FINAL_METRICS = '/dashboard/final_metrics'

# independent of the perception chain (DD-CN-10); health_node derives lidar_available only from fresh alerts (1.1.0)
#: bagwis_interfaces/msg/SafetyAlert
DASHBOARD_SAFETY_ALERTS = '/dashboard/safety_alerts'

# NEW -- not named in SRS-00 SS3; justified by FR-CN-67 and SADD-04 healthStore.ts
#: bagwis_interfaces/msg/SystemHealth
DASHBOARD_SYSTEM_HEALTH = '/dashboard/system_health'

# NEW -- not named in SRS-00 SS3; justified by FR-CN-47 and FR-WEB-21. Latched.
#: bagwis_interfaces/msg/AnalyticsAssumptions
DASHBOARD_ASSUMPTIONS = '/dashboard/assumptions'

# number of connected WebSocket clients (rosbridge_server ClientManager)
#: std_msgs/msg/Int32
BRIDGE_CLIENT_COUNT = '/client_count'

# per-client address and connection time (rosbridge_server ClientManager)
#: rosbridge_msgs/msg/ConnectedClients
BRIDGE_CONNECTED_CLIENTS = '/connected_clients'

# --- Services ---

#: bagwis_interfaces/srv/StartMission
MISSION_START = '/mission/start'

#: bagwis_interfaces/srv/StopMission
MISSION_STOP = '/mission/stop'

#: bagwis_interfaces/srv/GetMissionState
MISSION_STATE = '/mission/state'

#: bagwis_interfaces/srv/ExportBiomassSample
BIOMASS_EXPORT = '/analytics/export_biomass_sample'

# Machine-readable form, consumed by the startup graph-conformance check
# (FR-CN-63), which compares `ros2 topic list` against these entries and
# fails loudly on a mismatch rather than presenting as a dead sensor.
TOPICS = {
    'CAMERA_IMAGE_RAW': {
        'name': '/camera/image_raw',
        'type': 'sensor_msgs/msg/Image',
        'publisher': 'v4l2_camera_node',
        'subscribers': [],
        'qos': 'sensor_data',
    },
    'CAMERA_IMAGE_RAW_COMPRESSED': {
        'name': '/camera/image_raw/compressed',
        'type': 'sensor_msgs/msg/CompressedImage',
        'publisher': 'v4l2_camera_node',
        'subscribers': ['preprocessing_node', 'rosbridge_websocket_node', 'health_node'],
        'qos': 'sensor_data',
    },
    'CAMERA_IMAGE_PROCESSED': {
        'name': '/camera/image_processed',
        'type': 'sensor_msgs/msg/Image',
        'publisher': 'preprocessing_node',
        'subscribers': ['yolo26n_inference_node'],
        'qos': 'sensor_data',
    },
    'CAMERA_INFO': {
        'name': '/camera/camera_info',
        'type': 'sensor_msgs/msg/CameraInfo',
        'publisher': 'v4l2_camera_node',
        'subscribers': ['georeferencing_node', 'rosbridge_websocket_node'],
        'qos': 'default',
    },
    'AI_DETECTIONS_RAW': {
        'name': '/ai/detections_raw',
        'type': 'bagwis_interfaces/msg/SegmentedDetectionArray',
        'publisher': 'yolo26n_inference_node',
        'subscribers': ['dynamic_sampling_node', 'georeferencing_node', 'rosbridge_websocket_node', 'health_node'],
        'qos': 'sensor_data',
    },
    'AI_DETECTIONS': {
        'name': '/ai/detections',
        'type': 'bagwis_interfaces/msg/SegmentedDetectionArray',
        'publisher': 'dynamic_sampling_node',
        'subscribers': ['georeferencing_node', 'ndvi_computation_node'],
        'qos': 'default',
    },
    'AI_NDVI': {
        'name': '/ai/ndvi',
        'type': 'bagwis_interfaces/msg/NdviResult',
        'publisher': 'ndvi_computation_node',
        'subscribers': ['georeferencing_node', 'dynamic_sampling_node', 'health_node'],
        'qos': 'default',
    },
    'CORE_ADMISSION_STATUS': {
        'name': '/core/admission_status',
        'type': 'bagwis_interfaces/msg/AdmissionStatus',
        'publisher': 'dynamic_sampling_node',
        'subscribers': ['health_node'],
        'qos': 'default',
    },
    'CORE_GEO_DETECTIONS': {
        'name': '/core/geo_detections',
        'type': 'bagwis_interfaces/msg/GeoDetection',
        'publisher': 'georeferencing_node',
        'subscribers': [],
        'qos': 'default',
    },
    'CORE_GEOREFERENCING_STATUS': {
        'name': '/core/georeferencing_status',
        'type': 'bagwis_interfaces/msg/GeoreferencingStatus',
        'publisher': 'georeferencing_node',
        'subscribers': ['health_node'],
        'qos': 'default',
    },
    'MAVROS_GLOBAL_POSITION': {
        'name': '/mavros/global_position/global',
        'type': 'sensor_msgs/msg/NavSatFix',
        'publisher': 'mavros_node',
        'subscribers': ['georeferencing_node', 'dynamic_sampling_node', 'health_node'],
        'qos': 'sensor_data',
    },
    'MAVROS_REL_ALT': {
        'name': '/mavros/global_position/rel_alt',
        'type': 'std_msgs/msg/Float64',
        'publisher': 'mavros_node',
        'subscribers': ['georeferencing_node', 'dynamic_sampling_node'],
        'qos': 'sensor_data',
    },
    'MAVROS_VELOCITY_LOCAL': {
        'name': '/mavros/local_position/velocity_local',
        'type': 'geometry_msgs/msg/TwistStamped',
        'publisher': 'mavros_node',
        'subscribers': ['dynamic_sampling_node'],
        'qos': 'sensor_data',
    },
    'MAVROS_IMU': {
        'name': '/mavros/imu/data',
        'type': 'sensor_msgs/msg/Imu',
        'publisher': 'mavros_node',
        'subscribers': ['georeferencing_node'],
        'qos': 'sensor_data',
    },
    'MAVROS_BATTERY': {
        'name': '/mavros/battery',
        'type': 'sensor_msgs/msg/BatteryState',
        'publisher': 'mavros_node',
        'subscribers': ['health_node'],
        'qos': 'sensor_data',
    },
    'MAVROS_RANGEFINDER': {
        'name': '/mavros/distance_sensor/rangefinder',
        'type': 'sensor_msgs/msg/Range',
        'publisher': 'mavros_node',
        'subscribers': ['lidar_safety_node'],
        'qos': 'sensor_data',
    },
    'MAVROS_WAYPOINTS': {
        'name': '/mavros/mission/waypoints',
        'type': 'mavros_msgs/msg/WaypointList',
        'publisher': 'rosbridge_websocket_node',
        'subscribers': ['mavros_node'],
        'qos': 'default',
    },
    'DASHBOARD_FINAL_METRICS': {
        'name': '/dashboard/final_metrics',
        'type': 'bagwis_interfaces/msg/FinalMetrics',
        'publisher': 'georeferencing_node',
        'subscribers': ['rosbridge_websocket_node'],
        'qos': 'default',
    },
    'DASHBOARD_SAFETY_ALERTS': {
        'name': '/dashboard/safety_alerts',
        'type': 'bagwis_interfaces/msg/SafetyAlert',
        'publisher': 'lidar_safety_node',
        'subscribers': ['rosbridge_websocket_node', 'health_node'],
        'qos': 'default',
    },
    'DASHBOARD_SYSTEM_HEALTH': {
        'name': '/dashboard/system_health',
        'type': 'bagwis_interfaces/msg/SystemHealth',
        'publisher': 'health_node',
        'subscribers': ['rosbridge_websocket_node'],
        'qos': 'default',
    },
    'DASHBOARD_ASSUMPTIONS': {
        'name': '/dashboard/assumptions',
        'type': 'bagwis_interfaces/msg/AnalyticsAssumptions',
        'publisher': 'georeferencing_node',
        'subscribers': ['rosbridge_websocket_node'],
        'qos': 'transient_local',
    },
    'BRIDGE_CLIENT_COUNT': {
        'name': '/client_count',
        'type': 'std_msgs/msg/Int32',
        'publisher': 'rosbridge_websocket_node',
        'subscribers': [],
        'qos': 'transient_local',
    },
    'BRIDGE_CONNECTED_CLIENTS': {
        'name': '/connected_clients',
        'type': 'rosbridge_msgs/msg/ConnectedClients',
        'publisher': 'rosbridge_websocket_node',
        'subscribers': [],
        'qos': 'transient_local',
    },
}

SERVICES = {
    'MISSION_START': {
        'name': '/mission/start',
        'type': 'bagwis_interfaces/srv/StartMission',
        'server': 'rosbridge_websocket_node',
    },
    'MISSION_STOP': {
        'name': '/mission/stop',
        'type': 'bagwis_interfaces/srv/StopMission',
        'server': 'rosbridge_websocket_node',
    },
    'MISSION_STATE': {
        'name': '/mission/state',
        'type': 'bagwis_interfaces/srv/GetMissionState',
        'server': 'rosbridge_websocket_node',
    },
    'BIOMASS_EXPORT': {
        'name': '/analytics/export_biomass_sample',
        'type': 'bagwis_interfaces/srv/ExportBiomassSample',
        'server': 'georeferencing_node',
    },
}
