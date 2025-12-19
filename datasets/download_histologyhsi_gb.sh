# this script helps the user download and set up the dataset as required for calibration etc.


# I have currently only downloaded data for P1's ROIs 03 and 04 - this part is not fully downloaded

DATASET_DIR="./datasets"
RAW_DIR="./datasets/raw"
WHITE_DIR="./datasets/white"
DARK_DIR="./datasets/dark"
PREPROCESSED_DIR="./datasets/preprocessed"
RGB_DIR="./datasets/rgb"
TRAIN_A="./datasets/trainA"
TEST_A="./datasets/testA"
TRAIN_B="./datasets/trainB"
TEST_B="./datasets/testB"
# create expected dataset folder structure for preprocessing
mkdir -p ${RAW_DIR} ${WHITE_DIR} ${DARK_DIR} ${PREPROCESSED_DIR} ${RGB_DIR} ${TRAIN_A} ${TEST_A} ${TRAIN_B} ${TEST_B}



# ---- USER INSTRUCTIONS ----

# Step 1: Get user to download dataset
mkdir -p "${DATASET_DIR}/temp"
echo "Please manually download the dataset via TCIA (Aspera). Without renaming any of the files, unzip the folder and move it into ./datasets/temp"


# Step 2: Organise files into subfolders
# rename files then move

# organise hdr files
for hdr_path in "${DATASET_DIR}"/temp/P*/ROI*/raw.hdr; do
    # extract P* and ROI* parts from path
    # ROI* part includes cover image number and tumor marker  eg. ROI_1_C01_T
    patient=$(basename "$(dirname "$(dirname "$hdr_path")")")
    roi=$(basename "$(dirname "$hdr_path")")

    new_name="${patient}_${roi}_raw.hdr"

    mv "$hdr_path" "${RAW_DIR}/${new_name}"
done

# organise hsi files
for hdr_path in "${DATASET_DIR}"/temp/P*/ROI*/raw; do
    # extract P* and ROI* parts from path
    # ROI* part includes cover image number and tumor marker  eg. ROI_1_C01_T
    patient=$(basename "$(dirname "$(dirname "$hdr_path")")")
    roi=$(basename "$(dirname "$hdr_path")")

    new_name="${patient}_${roi}_raw"

    mv "$hdr_path" "${RAW_DIR}/${new_name}"
done

# organise whiteReference files
for hdr_path in "${DATASET_DIR}"/temp/P*/ROI*/whiteReference.hdr; do
    # extract P* and ROI* parts from path
    patient=$(basename "$(dirname "$(dirname "$hdr_path")")")
    roi=$(basename "$(dirname "$hdr_path")")

    new_name="${patient}_${roi}_whiteReference.hdr"

    mv "$hdr_path" "${WHITE_DIR}/${new_name}"
done

# organise darkReference files
for hdr_path in "${DATASET_DIR}"/temp/P*/ROI*/darkReference.hdr; do
    # extract P* and ROI* parts from path
    patient=$(basename "$(dirname "$(dirname "$hdr_path")")")
    roi=$(basename "$(dirname "$hdr_path")")

    new_name="${patient}_${roi}_darkReference.hdr"

    mv "$hdr_path" "${DARK_DIR}/${new_name}"
done

# organise rgb files
for hdr_path in "${DATASET_DIR}"/temp/P*/ROI*/rgb.png; do
    # extract P* and ROI* parts from path
    patient=$(basename "$(dirname "$(dirname "$hdr_path")")")
    roi=$(basename "$(dirname "$hdr_path")")

    new_name="${patient}_${roi}_rgb.hdr"

    mv "$hdr_path" "${RGB_DIR}/${new_name}"
done

# Step 4: Clean up temporary files
#rm -rf "${DATASET_DIR}/temp" "${DATASET_DIR}/HistologyHSI-GB.zip"

echo "Dataset organisation complete!"
echo "Raw hyperspectral data:     ${DATASET_DIR}/raw"
echo "White reference:      ${DATASET_DIR}/white"
echo "Dark reference:       ${DATASET_DIR}/dark"
echo "rgb data:     ${DATASET_DIR}/rgb"
echo "Ready for preprocessing script (scripts/calibrate_and_reduce_hsi.py)"