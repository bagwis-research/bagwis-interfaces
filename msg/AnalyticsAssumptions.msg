# Published latched (transient_local) on /dashboard/assumptions. SRS-00 SS4.6.
#
# Carries the Table 5 constants so the dashboard and the CSV/KML exports can
# state the assumptions behind every number, and so a changed constant is never
# invisible (DD-CN-9, FR-CN-47, FR-WEB-21).
#
# header is an addition to SRS-00 SS4.6, required by FR-IF-08 because this
# message is published on its own topic. See CHANGELOG "Deviations from
# SRS-00 SS4".

std_msgs/Header header

float32  mat_depth_m                # D_avg,      default 0.15
float32  truck_capacity_m3          # V_truck,    default 6.0
float32  hyacinth_density_kg_m2     # W_density,  default 40.0
float32  confidence_threshold
float32  kde_bandwidth_m
float32  vegetation_ndvi_threshold
float32  launch_to_water_offset_m   # subtracted from barometric relative altitude
string   model_version              # artifact bundle tag
string   citation_note
