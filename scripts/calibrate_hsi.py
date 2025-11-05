# calibrate hyperspectral cubes using white and dark reference images

# requires: pip install spectral numpy tqdm

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
raw_glob = "datasets/raw/raw.hdr"
# pattern to match for white reference headers
white_path = "datasets/white/whiteReference.hdr"
# pattern to match for dark reference headers
dark_path = "datasets/dark/darkReference.hdr"
# directory in which to store calibrated images
output_dir = "datasets/calibrated"

# small number to avoid division by zero
eps = 1e-9

# an ENVI cube is a 3D data sctucture (hence cube) used to process and visualise images with multiple spectral bands