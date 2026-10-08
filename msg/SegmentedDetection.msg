# One best hypothesis in an undistorted full-resolution image.
# Producers undo letterboxing on boxes and masks. Highest score wins;
# ties preserve producer order. No Detection2DArray compatibility payload.
uint8 class_id                 # 0..4 or 255 unknown
float32 confidence
float64 center_u
float64 center_v
float64 width_px
float64 height_px

# Flattened [start,length,...] runs of row-major foreground image indices.
# Each pixel is the cell [column,column+1] x [row,row+1] in pixel-edge coordinates.
# Positive lengths, inside one image row; sorted, non-overlapping and coalesced
# within each row. At least one foreground pixel is required per detection.
# Pixel count is the sum of lengths; bounding boxes are not measured masks.
uint32[] mask_runs
