#!/bin/bash
date
cd /uscms_data/d3/rasharma/aQGC_analysis/CMS_FulllSimulation_April2017/LHE_GEN/CMSSW_8_0_21/src
cmsenv
echo $PWD
eval `scram runtime -sh`
cd -
echo $PWD
a=$PWD
echo $a

RandNum=`python -c "import random; print random.randint(0,10000000)"`

echo "Random Seed = ${RandNum}"

tar -xf MG5_aMC_v2.5.4.tar.gz
cd MG5_aMC_v2_5_4
cp ../*.dat .
sed  "s/39/${RandNum}/g" $*
./bin/mg5_aMC $*

echo -e "\n\n=====================================================================\n\n"
test=`echo $* | sed 's/_proc_card.dat//g'`
echo "=====> Variable test = "$test
echo "List all root files = "
ls 
echo "List all files"
ls $test/Events
ls $test/Events/*

# copy output to eos
OUTDIR=root://cmseos.fnal.gov//store/user/rasharma/MonteCarlo_Samples/MadGraph/EWK

eos root://cmseos.fnal.gov mkdir $OUTDIR/$RandNum

OUTDIR=$OUTDIR/$RandNum
#
#
echo "xrdcp output for condor"
for FILE in $test/Events/*/*
do
  echo "xrdcp -f ${FILE} ${OUTDIR}/${FILE}"
  xrdcp -f ${FILE} ${OUTDIR}/${FILE} 2>&1
  XRDEXIT=$?
  if [[ $XRDEXIT -ne 0 ]]; then
    rm *.root
    echo "exit code $XRDEXIT, failure in xrdcp"
    exit $XRDEXIT
  fi
  rm ${FILE}
done
date
