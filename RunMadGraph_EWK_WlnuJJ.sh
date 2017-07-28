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
sed  "s/39/${RandNum}/g" $1
./bin/mg5_aMC $1

echo -e "\n\n=====================================================================\n\n"
test=`echo $* | sed 's/_proc_card.dat//g'`
echo "=====> Variable test = "$test
echo "List all root files = "
ls 
echo "List all files"
ls $test/Events
ls $test/Events/*

# copy output to eos
OUTDIR=root://cmseos.fnal.gov//store/user/rasharma/MonteCarlo_Samples/MadGraph/EWK_Wlnujj

#eos root://cmseos.fnal.gov mkdir $OUTDIR/$RandNum
eos root://cmseos.fnal.gov mkdir $OUTDIR/${FILE}_$3_$2

#OUTDIR=$OUTDIR/$RandNum
#
#
echo "xrdcp output for condor"
for FILE in $test/Events/*/*
do
  echo "xrdcp -f ${FILE} ${OUTDIR}/${FILE}_$3_$2"
  xrdcp -f ${FILE} ${OUTDIR}/${FILE}_$3_$2 2>&1
done
date
