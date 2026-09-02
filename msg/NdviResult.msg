# Published on /ai/ndvi by ndvi_computation_node, consumed by georeferencing_node.
#
# SRS-00 SS4.1. Computed only on frames admitted by dynamic_sampling_node, so
# /ai/detections and /ai/ndvi share a header stamp and georeferencing_node fuses
# them directly. The mask_* arrays are index-aligned to that frame's detections:
# that alignment is the contract which lets a detection be matched to its NDVI
# value without a second association step.
#
# C-13: the topic is /ai/ndvi. NDVI is spelled correctly everywhere.

std_msgs/Header header

float32   mean_ndvi                 # over the vegetation mask
float32   vegetation_threshold      # threshold applied, for auditability
uint32    vegetation_pixel_count    # Px for the hyacinth mask
float32[] mask_ndvi                 # per-instance mean NDVI, index-aligned to detections
uint32[]  mask_pixel_count          # per-instance Px, index-aligned to detections
bool      nir_available             # false -> all NDVI fields are meaningless
string    registration_status       # homography state: ok | degraded | unavailable
