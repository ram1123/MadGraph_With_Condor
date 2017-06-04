# MadGraph_With_Condor

	cmsrel CMSSW_8_0_11
	cd CMSSW_8_0_11/src
	cmsenv
	wget https://launchpad.net/mg5amcnlo/2.0/2.5.x/+download/MG5_aMC_v2.5.5.tar.gz

* Modify files RunMadGraph_condor.sh and RunMadGraph_condor.jdl, then submit it using

		condor_submit RunMadGraph_condor.jdl
