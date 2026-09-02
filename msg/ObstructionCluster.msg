# A choke-point cluster. The dashboard renders one metric card per cluster
# (Table 6 SS3). SRS-00 SS4.3.
#
# No std_msgs/Header: this message is nested inside FinalMetrics.clusters and is
# never published on a topic of its own. first_seen / last_seen carry its time
# extent instead. See CHANGELOG "Deviations from SRS-00 SS4".

string   cluster_id
uint8    dominant_class_id
uint32   observation_count

geographic_msgs/GeoPoint centroid
geographic_msgs/GeoPoint[] hull

float32  area_m2                    # O-3
float32  volume_m3                  # O-4  = area_m2 x 0.15
float32  truck_loads                # O-5  = volume_m3 / 6.0
float32  wet_biomass_kg             # O-6  = area_m2 x 40.0, hyacinth only; 0.0 otherwise
float32  rwor_pct                   # O-7
float32  river_width_m              # RWOR denominator, for auditability
bool     is_organic                 # true -> O-6/O-7 apply; false -> O-3/O-4/O-5 apply

builtin_interfaces/Time first_seen
builtin_interfaces/Time last_seen
