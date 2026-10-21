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
float32  truck_capacity_m3          # V_truck,    default 6.0; settable at runtime, [1.0, 40.0]
# Where the active V_truck comes from: the configured source (default
# "Manuscript Table 5 (project assumption)") or "Operator setting" after an
# accepted runtime change. Shown beside the value and in the exports.
string   truck_capacity_source
float32  hyacinth_density_kg_m2     # W_density,  default 40.0
float32  confidence_threshold
float32  kde_bandwidth_m
float32  rwor_alert_threshold_pct    # alert strictly above this percentage
float32  vegetation_ndvi_threshold
float32  launch_to_water_offset_m   # added to barometric relative altitude
string   model_version              # artifact bundle tag
string   river_profile_source       # actual measurement/source description
string   river_profile_revision     # actual survey/data revision
# Discloses cited uncalibrated empirical constants, mask-union deduplication,
# static targets, NIR-independent area-derived biomass, fractional truck
# equivalents and actual KDE grid spacing.
string   citation_note
# When the active analytic constants last changed: the latest accepted runtime
# change, or the first value this mission ran with. Wall-clock (UTC) time, from
# the mission registry's change log, so it survives a node restart.
builtin_interfaces/Time assumptions_updated_at
