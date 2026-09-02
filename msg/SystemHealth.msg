# Published on /dashboard/system_health at >= 1 Hz (FR-CN-67), aggregated by
# health_node. Feeds the operator display and the ISO 25010 Reliability
# evidence. SRS-00 SS4.7.
#
# sampling_interval_s and fov_footprint_m are here so the non-overlap claim is
# observable rather than asserted (FR-CN-07).

std_msgs/Header header

float32  link_rssi_dbm
float32  downlink_fps
float32  inference_latency_ms       # mean processing latency, per Statistical Treatment
float32  end_to_end_latency_ms
float32  sampling_interval_s        # current FOV / ground_speed result
float32  fov_footprint_m

float32  master_cpu_pct
float32  master_temp_c
float32  slave_cpu_pct
float32  slave_temp_c
float32  clock_offset_ms

float32  battery_voltage
float32  battery_remaining_pct
uint8    gps_fix_type
uint8    gps_satellites

uint8    LINK_OK=0
uint8    LINK_DEGRADED=1
uint8    LINK_LOST=2
uint8    link_state                 # 0 OK - 1 DEGRADED - 2 LOST

uint8    BACKEND_ONNX=0
uint8    BACKEND_RKNN=1
uint8    inference_backend          # 0 ONNX - 1 RKNN

bool     nir_available
bool     lidar_available
string[] active_warnings
