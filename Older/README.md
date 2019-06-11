# MadGraph_With_Condor

* This repo contains script for submitting the madgraph jobs.
* Just we have to prepare the proc card and give its name in the \*.jdl file
* Also, if you need to generate a lot of events then you can use the **Queue** feature of condor job.
	* The script sets "iSeed" for every run so the seed should be unique and hence you are not going to replicate it.

# How to generate events

	cmsrel CMSSW_8_0_11
	cd CMSSW_8_0_11/src
	cmsenv
	wget https://launchpad.net/mg5amcnlo/2.0/2.5.x/+download/MG5_aMC_v2.5.5.tar.gz

* Modify files RunMadGraph_condor.sh and RunMadGraph_condor.jdl, then submit it using

		condor_submit RunMadGraph_condor.jdl

* Note that all input \*_proc_card.dat's prefix should be exactly same as  name of output file that madgraph will create.

* Before submitting the condor you have to 

		voms-proxy-init --voms cms --valid 168:00

Extract cross-section

	grep "Total:\|Cross-section"  <fileName>

Check the random seed from stdout file

	grep "Using random number seed offset" */*.stdout

Change the seed 

	sed -i 's/set iseed 15/set iseed 17/g' EWK_cards/*.dat
	sed -i 's/set iseed 15/set iseed 17/g' QCD_Cards/*.dat
	sed -i 's/set iseed 15/set iseed 17/g' EWKaQCD_cards/*.dat

change directory name

	sed -i 's/Ext3/Ext4/g' RunMadGraph_EWK.jdl
	sed -i 's/Ext3/Ext4/g' RunMadGraph_EWK.sh
	sed -i 's/Ext3/Ext4/g' RunMadGraph_QCD.jdl
	sed -i 's/Ext3/Ext4/g' RunMadGraph_QCD.sh
	sed -i 's/Ext3/Ext4/g' RunMadGraph_EWKaQCD.jdl
	sed -i 's/Ext3/Ext4/g' RunMadGraph_EWKaQCD.sho

condor_q -submitter rasharma | grep "running,\|idle,\|.fnal.gov" | awk -F "," '{print $3,$4}'
condor_q -submitter rasharma | grep "running,\|idle,\|.fnal.gov"
