# Capture timing and radiometric provenance for the corresponding compressed frame.
# Header matches the image and CameraInfo: original common-time capture stamp and
# sensor optical frame_id. Metadata alone does not establish NDVI availability.
uint8 TIME_REFERENCE_UNKNOWN=0
uint8 TIME_REFERENCE_EXPOSURE_START=1
uint8 TIME_REFERENCE_EXPOSURE_END=2

std_msgs/Header header
uint64 sequence
string source  # file_replay for offline recordings; never claims live hardware
string source_clock  # original recorded clock name, e.g. ros or monotonic
int64 source_timestamp_ns  # original source clock value, not publication time
uint8 timestamp_reference
string encoding
uint8 sample_bit_depth
string spectral_band  # visible_rgb, unfiltered_noir, or nir
float64 exposure_us  # NaN if unknown
float64 analogue_gain  # multiplicative factor, not register code; NaN if unknown
float64 black_level  # native sample units; NaN if unknown
float64 white_level  # native sample units; NaN if unknown
bool radiometry_valid
string calibration_id  # radiometric provenance ID; empty if absent, not intrinsic calibration
