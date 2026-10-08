# A choke-point cluster. The dashboard renders one metric card per cluster
# (Table 6 SS3). SRS-00 SS4.3.
#
# No std_msgs/Header: this message is nested inside FinalMetrics.clusters and is
# never published on a topic of its own. first_seen / last_seen carry its time
# extent instead. See CHANGELOG "Deviations from SRS-00 SS4".

string   cluster_id
uint8    dominant_class_id
uint32   observation_count
uint8[]   class_ids                 # sorted observed IDs, including 255; aligned with class_area_m2
float64[] class_area_m2             # per-class spatial union area, NaN if unmeasured

geographic_msgs/GeoPoint centroid
geographic_msgs/GeoPoint[] hull

float32  area_m2                    # O-3: union across all class layers, not their sum
float32  volume_m3                  # O-4: classes 1-4 union area x mat depth
float32  truck_loads                # O-5: waste volume / truck capacity; fractional equivalents
float32  wet_biomass_kg             # O-6: class-0 union area x hyacinth density, even without NIR
float32  rwor_pct                   # O-7: class-0 obstruction only
float32  river_width_m              # RWOR denominator, for auditability
bool     is_organic                 # dominant_class_id == 0; does not determine mixed-layer metrics

# Non-applicable biomass/volume/truck/RWOR are zero; applicable unmeasured values
# are NaN. Unknown class 255 contributes surface area only, not named analytics.

builtin_interfaces/Time first_seen
builtin_interfaces/Time last_seen
