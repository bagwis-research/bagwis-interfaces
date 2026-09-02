# One detection after georeferencing -- the atomic unit all seven analytics
# build on. SRS-00 SS4.2.
#
# Area comes from mask pixel count, never box area (DD-CN-18): box area
# over-reports a bottle's footprint by the surrounding empty space, and that
# error propagates through O-4 volume into O-5 truck loads.

std_msgs/Header header

string   cluster_id
uint8    class_id                   # Table 4 detection map, 0..4
string   class_name
float32  confidence

geographic_msgs/GeoPoint centroid          # WGS84
geographic_msgs/GeoPoint[] polygon         # footprint projected to WGS84

uint32   pixel_count                # Px, for Area = Px x GSD^2
float32  gsd_m_px
float32  area_m2                    # O-3
float32  max_length_m
float32  mean_ndvi                  # NaN when nir_available is false
float32  fov_footprint_m            # FOV length for this sampling interval
