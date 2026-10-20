# Published by airborne_health_node on /airborne/health. This is a host-local
# measurement input to core health_node, never a partial dashboard aggregate.
#
# Header stamp is acquisition start; frame_id is empty. Numeric values are NaN
# when unavailable, never substituted with zero or a prior sample. Warnings name
# only conditions in this sample, never accumulated history.
std_msgs/Header header

float32 cpu_pct                 # aggregate host utilization over two proc-stat samples
float32 temp_c                  # configured CPU/SoC thermal-zone Celsius reading
float32 clock_offset_ms         # signed remaining chrony correction vs ground, positive = local slow
float64 storage_free_bytes      # filesystem bytes available to the running user
string[] active_warnings
