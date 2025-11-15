# data preprocessing step 1
# calibrate hyperspectral cubes using white and dark reference images

# data preprocessing step 2
# generate spectrally reduced HS images by averaging spectral bands of adjacent neighbouring bands
# use spectral window of 3 neighbours - apart from the last 4 bands which will form a group since 826 doesn't divide by 3
# reduce original 826 bands to 275
# dimension reduction also slightly decreases the presence of white Gaussian noise

# each band corresponds to a narrow wavelength range


import os
import numpy as np
import scipy
# spectral is a module for processing hyperspectral image data eg. reading, displaying, manipulating
from spectral import io as spio
from spectral import save_image
# glob is a module that provides tools to find path names matching specified patterns that follow Unix shell rules
from glob import glob



# glob
# pattern to match for raw cube headers
raw_glob = "datasets/raw/*.hdr"

# directory in which to store calibrated images
output_dir = "datasets/calibrated"


# an ENVI cube is a 3D data structure (hence cube) used to process and visualise images with multiple spectral bands
# a header file eg. .hdr and its corresponding binary file eg. .dat or .img together store one hyperspectral image cube in ENVI format
# .hdr tells ENVI and the loader how to interpret the .dat binary
# each ROI has 3 cubes: raw, white and dark

# helper function to load ENVI hyperspectral cube
def load_hyperspectral_cube(hdr_path):
    """
    Parameters
    ---------- 
    hdr_path : str
        File location of the ENVI header related to the hyperspectral data

    Variables
    ----------
    cube_metadata
        metadata object containing metadata about the hs cube eg. image dimensions

    Returns
    ----------
    hs_data : ndarray (np.float32)
        3D numpy array containing radiance/intensity measurements from the camera sensor. It stores an array of values at consecutive wavelengths (spectrum) for each pixel ie. each row and column. array contains hyperspectral cube

    wavelengths : ndarray
        1D nump array containing spectral bands corresponding to the hyperspectral cube
    """
    
    # parses .hdr file to read useful metadata eg. image dimensions
    # loads binary data from paired .dat file
    # array.shape = (height, width, spectral_channels)
    cube_metadata = spio.envi.open(hdr_path)
    # specifically load array with float values for calculations
    hs_data = cube_metadata.load().astype(np.float32)
    wavelengths = cube_metadata.bands.centers
    return hs_data, wavelengths, cube_metadata


# need to import wavelengths from calibration file
def reduce_spectral_dimensions(intensity_array, wavelengths, n=3):
    """
    Parameters
    ----------
    input_data : ndarray
        Array containing the raw hyperspectral cube
    wavelengths : ndarray
        1D nump array containing spectral bands corresponding to the hyperspectral cube
    n : Integer
        width of the spectral window

    Returns
    ----------
    band_reduced_cube : ndarray
        3D numpy array containing the hyperspectral cube after band reduction
    wavelength_reduced : ndarray
        1D numpy array containing the spectral bands corresponding to the hyperspectral cube after the band reduction
    """
    w = np.ones(n)/n
    moving_averaged_image = scipy.ndimage.convolved(intensity_array, w, axis=2)
    band_reduced_cube = moving_averaged_image[:,:,1:-1:n]
    wavelength_reduced = wavelengths[1:-1:n]
    return band_reduced_cube, wavelength_reduced


# go through each raw hyperspectral file in order
for raw_hdr in sorted(glob(raw_glob)):
    # load the correct references for this raw hdr

    #CALIBRATION
    base = os.path.splitext(os.path.basename(raw_hdr))[0]
    prefix = base.replace("_raw", "")
    white_hdr = f"datasets/white/{prefix}_whiteReference.hdr"
    dark_hdr = f"datasets/dark/{prefix}_darkReference"

    white_reference_hs_data, white_wavelengths, white_cube_metadata = load_hyperspectral_cube(white_hdr)
    dark_reference_hs_data, dark_wavelengths, dark_cube_metadata = load_hyperspectral_cube(dark_hdr)
    raw_hs_data, raw_wavelengths, raw_cube_metadata = load_hyperspectral_cube(raw_hdr)


    # white and dark cubes are full-size and match shape so use per-pixel calibration
    # If you get an error here, check that cubes match shape and if not broadcast per-band spectrum to image shape
    numerator = raw_hs_data - dark_reference_hs_data
    denominator = white_reference_hs_data - dark_reference_hs_data
    # dividing normalises the raw data to a [0-1] reflectance scale
    calibrated_cube = numerator / denominator
    # clipping to a sensible range
    calibrated_cube = np.clip(calibrated_cube, 0, 1)


    # BAND REDUCTION
    band_reduced_cube = reduce_spectral_dimensions(calibrated_cube, raw_wavelengths, n=3)



    # save calibrated_cube as ENVI float32 cube in datasets/calibrated folder
    # Example:
    # raw_hdr = "/datasets/raw/P1_ROI03_raw.hdr"
    # os.path.basename(raw_hdr) = "P1_ROI03_raw.hdr"
    # os.path.splitext(os.path.basename(raw_hdr)) = ("P1_ROI03_raw", ".hdr")
    # base = "P1_ROI03_raw"
    base = os.path.splitext(os.path.basename(raw_hdr))[0]
    output_hdr = os.path.join(output_dir, base + "_calibrated_reduced.hdr")
    # save calibrated cube to output_hdr
    # use same interleave as original cube's metadate to avoid format mismatch
    interleave = raw_cube_metadata.metadata.get('interleave', 'bill')
    save_image(output_hdr, calibrated_cube.astype(np.float32), dtype=np.float32, interleave=interleave, ext='', force=True)

print("Data calibration and band reduction complete!")
print("Ready for patching.")