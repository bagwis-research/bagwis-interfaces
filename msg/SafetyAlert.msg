# Published on /dashboard/safety_alerts by lidar_safety_node, on a path fully
# independent of the perception chain (DD-CN-10). SRS-00 SS4.5.
#
# reading_in_range matters. The VL53L1X tops out around 4 m while the flight
# envelope is 40-80 m, so for most of a mission the sensor is legitimately out
# of range. That state must be distinguishable from a fault, or the operator
# sees a permanent false alarm and starts ignoring the panel -- which is exactly
# when a real proximity alert stops working (C-16, DD-CN-11).

std_msgs/Header header

uint8    LEVEL_INFO=0
uint8    LEVEL_CAUTION=1
uint8    LEVEL_WARNING=2
uint8    LEVEL_CRITICAL=3

uint8    level
string   alert_type                 # proximity | sensor_fault | out_of_range | stale
float32  measured_range_m           # from sensor_msgs/Range
float32  min_valid_range_m          # sensor floor, from Range.min_range
float32  max_valid_range_m          # sensor ceiling, from Range.max_range -- see C-16
bool     reading_in_range           # false when altitude exceeds sensor capability
geographic_msgs/GeoPoint location   # where the alert fired
string   message                    # plain-language text for the operator
builtin_interfaces/Time raised_at
