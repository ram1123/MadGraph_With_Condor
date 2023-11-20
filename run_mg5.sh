#!/bin/bash

# Stop on any error
set -e

echo "Job started..."
echo "Starting job on " $(date)
echo "Running on: $(uname -a)"
echo "System software: $(cat /etc/redhat-release)"
source /cvmfs/cms.cern.ch/cmsset_default.sh
echo "###################################################"
echo "#    List of Input Arguments: "
echo "###################################################"
echo "Input Arguments (Cluster ID): $1"
echo "Input Arguments (Proc ID): $2"
echo "Input Arguments (Output Dir): $3"
echo "Input Arguments (Input cards Dir): $4"
echo "Input Arguments (Cards Dir Name): $5"
echo ""

# Define CMSSW setup
CMSSW_VERSION="CMSSW_10_6_19"

export SCRAM_ARCH=slc7_amd64_gcc700

if [ -r ${CMSSW_VERSION}/src ] ; then
    echo release ${CMSSW_VERSION} already exists
else
    scram p CMSSW ${CMSSW_VERSION}
fi
cd ${CMSSW_VERSION}/src
eval `scram runtime -sh`
scram b
cd -

PWD=`pwd`
# Define variables
MG_DOWNLOAD_LINK="https://launchpad.net/mg5amcnlo/lts/2.6.x/+download/MG5_aMC_v2.6.7.tar.gz"
MODEL_DOWNLOAD_LINK="https://cms-project-generators.web.cern.ch/cms-project-generators/EWdim6NLO.tar.gz"
MG_DIR="MG5_aMC_v2_6_7"
MODEL_DIR="models"

# Check if script is running locally or on Condor
if [ "$#" -eq 5 ]; then
    # Running on Condor
    OUTPUT_DIR=$3
    CARD_DIR=${PWD}/${4}
    CARD_DIR_NAME=$5
else
    # Running locally
    OUTPUT_DIR="/eos/user/r/rasharma/post_doc_ihep/aTGC/StandaloneMG5"
    CARD_DIR="${PWD}/AnkitaCards/"
    CARD_DIR_NAME="WpWmToLpNujj_01j_aTGC_pTW-150toInf_mWV-600to800_4f_NLO_FXFX"
fi
MG5_COMMANDS="${CARD_DIR}/mg5_commands.txt"  # Command file for generate_events

# list files inside the CARD_DIR
echo "=================================="
echo "===> List files inside the CARD_DIR"
ls -l ${CARD_DIR}
echo "===> List files inside the CARD_DIR_NAME"
ls -l ${CARD_DIR}/${CARD_DIR_NAME}
echo "=================================="

# # Download and untar MadGraph
wget -N $MG_DOWNLOAD_LINK -O MG5_aMC_v2.6.7.tar.gz
tar -zxf MG5_aMC_v2.6.7.tar.gz

# # Download the model and move it to the models directory
wget -N $MODEL_DOWNLOAD_LINK
mv EWdim6NLO.tar.gz $MG_DIR/$MODEL_DIR/

# # Untar the model file inside the models directory
tar -zxf $MG_DIR/$MODEL_DIR/EWdim6NLO.tar.gz -C $MG_DIR/$MODEL_DIR/
cp $CARD_DIR/restrict_no_cmass_cwwwcbcw.dat $MG_DIR/models/EWdim6NLO/restrict_no_cmass_cwwwcbcw.dat
# Change to the MadGraph directory
cd $MG_DIR

# Run MadGraph with a specific proc card - Update with your proc card name
echo "./bin/mg5_aMC $CARD_DIR/$CARD_DIR_NAME/WpWmToLpNujj_01j_aTGC_pTW-150toInf_mWV-600to800_4f_NLO_FXFX_proc_card.dat"
./bin/mg5_aMC $CARD_DIR/$CARD_DIR_NAME/WpWmToLpNujj_01j_aTGC_pTW-150toInf_mWV-600to800_4f_NLO_FXFX_proc_card.dat

# Copy and rename cards from the specified directory to the MadGraph Cards directory
cp ${CARD_DIR}/${CARD_DIR_NAME}/${CARD_DIR_NAME}_customizecards.dat ${CARD_DIR_NAME}/Cards/customizecards.dat
cp ${CARD_DIR}/${CARD_DIR_NAME}/${CARD_DIR_NAME}_proc_card.dat ${CARD_DIR_NAME}/Cards/proc_card.dat
# cp ${CARD_DIR}/${CARD_DIR_NAME}/${CARD_DIR_NAME}_extramodels.dat ${CARD_DIR_NAME}/Cards/extramodels.dat
cp ${CARD_DIR}/${CARD_DIR_NAME}/${CARD_DIR_NAME}_reweight_card.dat ${CARD_DIR_NAME}/Cards/reweight_card.dat
cp ${CARD_DIR}/${CARD_DIR_NAME}/${CARD_DIR_NAME}_FKS_params.dat ${CARD_DIR_NAME}/Cards/FKS_params.dat
cp ${CARD_DIR}/${CARD_DIR_NAME}/${CARD_DIR_NAME}_run_card.dat ${CARD_DIR_NAME}/Cards/run_card.dat

# Generate events - Replace with specific command if different
cd ${CARD_DIR_NAME}
echo `pwd`
echo "./bin/generate_events $MG5_COMMANDS"
./bin/generate_events < $MG5_COMMANDS

# Find all LHE files in the Events directory
LHE_FILES=$(find Events/run_*/*.lhe.gz -type f)

# Check if any LHE files were found
if [ -z "$LHE_FILES" ]; then
    echo "No LHE files found."
    exit 1
fi

# Copy each LHE file to the output directory with a suffix indicating its run number
for LHE_FILE in $LHE_FILES; do
    # Extract the run number from the file path
    RUN_NUMBER=$(echo $LHE_FILE | grep -o 'run_[0-9]*' | head -n 1)
    if [ -n "$RUN_NUMBER" ]; then
        # Copy the file with a new name including the run number
        echo "cp ${LHE_FILE} ${OUTPUT_DIR}/output_${RUN_NUMBER}.lhe.gz"
        cp "$LHE_FILE" "${OUTPUT_DIR}/output_${RUN_NUMBER}.lhe.gz"
    else
        echo "Run number not found in file path: ${LHE_FILE}"
    fi
done

echo "Process completed."
echo "Starting finished on " $(date)
