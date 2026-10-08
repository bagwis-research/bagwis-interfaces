# Atomic capture payload forwarded unchanged from raw inference to admission.
# A valid empty detections array is an empty frame. Non-empty arrays with
# absent/invalid masks are rejected, never interpreted as measured zero.
std_msgs/Header header         # capture stamp, undistorted full-resolution camera frame
uint32 image_width_px
uint32 image_height_px
SegmentedDetection[] detections
