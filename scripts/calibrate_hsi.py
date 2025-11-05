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


# putting raw hyperspectral cube, white reference file and dark reference file paths into variables below
# globs
#pattern for raw cube headers
raw_glob = 
# white reference
white_path =
dark_path =
output_dir = "data/calibrated"
# makes a directory in which to store calibrated data
os.makedirs(output_dir, exist_ok = True)
# small number to avoid division by zero
eps = 1e-9