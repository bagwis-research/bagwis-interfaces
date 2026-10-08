# Published on /core/georeferencing_status by georeferencing_node at 1 Hz and
# consumed by health_node.
#
# FR-CN-28: detection sets and NDVI results are paired by header stamp, and
# anything left unpaired is discarded and counted here. A paired frame then
# needs telemetry taken at or before its capture stamp; frames without it are
# counted by reason. Counts are cumulative since the node started.

std_msgs/Header header

uint32   frames_georeferenced       # paired frames that produced GeoDetections
uint32   detections_georeferenced
uint32   unmatched_detections       # admitted sets /ai/ndvi never answered
uint32   unmatched_ndvi             # NDVI results with no detection set
uint32   rejected_no_fix
uint32   rejected_stale_telemetry   # including frames with no telemetry at all
uint32   rejected_invalid_mask      # malformed atomic segmentation frames
uint32   clusters                   # obstruction clusters in the mission registry
