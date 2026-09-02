# Published on /dashboard/final_metrics by georeferencing_node -- the single
# topic the dashboard subscribes to for analytics. SRS-00 SS4.4.
#
# FR-WEB-24: the dashboard computes nothing. Every displayed value comes from
# this message. Formatting and unit display are presentation, not computation.

std_msgs/Header header

string   mission_id
string   segment_name               # "Tumana Bridge" | "Marikina Bridge"

ObstructionCluster[] clusters       # metric cards, one per choke-point

float32  total_hyacinth_area_m2
float32  total_waste_area_m2
float32  total_volume_m3
float32  total_truck_loads
float32  total_wet_biomass_kg
float32  max_rwor_pct
geographic_msgs/GeoPoint max_rwor_location
bool     rwor_alert_active          # flood early warning for MCDRRMO

# KDE surface for leaflet-heat: [lat, lon, weight] triples.
# The three arrays are index-aligned and must be of equal length.
float32[] kde_lat
float32[] kde_lon
float32[] kde_weight

float32  segment_covered_m
uint32   frames_inferred
