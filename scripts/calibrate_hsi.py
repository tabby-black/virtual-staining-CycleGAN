# data preprocessing step 1
# calibrate hyperspectral cubes using white and dark reference images

import os
import numpy as np
# spectral is a module for processing hyperspectral image data eg. reading, displaying, manipulating
from spectral import io as spio
from spectral import save_image
# glob is a module that provides tools to find path names matching specified patterns that follow Unix shell rules
from glob import glob
# tqdm is a library designed to provide progress bars to monitor the progress of running code
from tqdm import tqdm



# globs
# pattern to match for raw cube headers
raw_glob = "datasets/raw/*.hdr"
# pattern to match for white reference headers
white_path = "datasets/white/*.hdr"
# pattern to match for dark reference headers
dark_path = "datasets/dark/*.hdr"
# directory in which to store calibrated images
output_dir = "datasets/calibrated"
# small value to handle possible division by 0 eg. if some pixels have white==dark safely
eps = 1e-6

# an ENVI cube is a 3D data structure (hence cube) used to process and visualise images with multiple spectral bands
# a header file eg. .hdr and its corresponding binary file eg. .dat or .img together store one hyperspectral image cube in ENVI format
# .hdr tells ENVI and the loader how to interpret the .dat binary
# each ROI has 3 cubes: raw, white and dark

# helper function to load ENVI hyperspectral cube
def load_envi_cube(hdr_path):
    # parses .hdr file to read useful metadata eg. image dimensions
    # loads binary data from paired .dat file
    # cube = metadata object that knows how to interpret an ENVI file pair
    # array = single cube numpy.ndarray eg. (lines, samples, bands) ie. (height, width, spectral_channels)
    cube = spio.envi.open(hdr_path)
    # specifically load array with float values for calculations
    array = cube.load().astype(np.float32)
    return array, cube


for hdr in sorted(glob(raw_glob)):
    # load the correct references for this raw hdr
    hdr = "${patient}_${roi}_raw.hdr"
    white_path = "${patient}_${roi}_whiteReference.hdr"
    dark_path = "${patient}_${roi}_darkReference.hdr"
    white_array, white_cube = load_envi_cube(white_path)
    dark_array, dark_cube = load_envi_cube(dark_path)

    raw_array, raw_cube = load_envi_cube(hdr)
    # white and dark cubes are full-size and match shape so use per-pixel calibration
    # If you get an error here, check that cubes match shape and if not broadcast per-band spectrum to image shape
    # using equation from Nature paper
    numerator = raw_array - dark_array
    denominator = white_array - dark_array + eps

    calibrated_cube = numerator / denominator
    # clipping to a sensible range
    calibrated_cube = np.clip(calibrated_cube, 0, 1)

    # save calibrated_cube as ENVI float32 cube in datasets/calibrated folder
    # Example:
    # hdr = "/datasets/raw/P1_ROI03_raw.hdr"
    # os.path.basename(hdr) = "P1_ROI03_raw.hdr"
    # os.path.splitext(os.path.basename(hdr)) = ("P1_ROI03_raw", ".hdr")
    # base = "P1_ROI03_raw"
    base = os.path.splitext(os.path.basename(hdr))[0]
    output_hdr = os.path.join(output_dir, base + "_calibrated.hdr")
    # save calibrated cube to output_hdr
    # use same interleave as original cube's metadate to avoid format mismatch
    interleave = raw_cube.metadata.get('interleave', 'bill')
    save_image(output_hdr, calibrated_cube.astype(np.float32), dtype=np.float32, interleave=interleave, ext='', force=True)