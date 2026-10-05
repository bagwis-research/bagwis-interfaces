# Published on /core/admission_status by dynamic_sampling_node at 1 Hz and
# consumed by health_node, which copies sampling_interval_s, fov_footprint_m,
# admitted_frames and shed_rate into SystemHealth (FR-CN-07).
#
# Counts are cumulative since the node started. Every detection set the node
# receives lands in exactly one of admitted_frames, shed_frames or a rejected_*
# counter, so their sum is the number of sets seen. A shed (FR-CN-09) is kept
# apart from the rejections because it is the only outcome caused by
# downstream pressure rather than by the frame itself.

std_msgs/Header header

float32  sampling_interval_s        # FOV / ground speed; +inf while hovering
float32  fov_footprint_m            # along-track footprint at the current height above water

uint32   admitted_frames
uint32   shed_frames
float32  shed_rate                  # shed / (admitted + shed); 0 when both are 0

uint32   rejected_no_fix            # FR-CN-08
uint32   rejected_stale_telemetry   # FR-CN-08, including frames with no telemetry at all
uint32   rejected_hover             # FR-CN-05
uint32   rejected_not_cleared       # footprint has not moved off the last admitted one

uint32   downstream_timeouts        # admitted frames /ai/ndvi never answered within the timeout
