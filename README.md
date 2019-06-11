# Run Standalone Madgraph Using Condor

The main script is  `generate_lhe_condor.py`. Its help argument goes like:

```bash
python generate_lhe_condor.py -h
usage: generate_lhe_condor.py [-h] [-i INPUTPATH] -f TARFILE [-o OUTPUTPATH]
                              [-od OUTPUTDIR] [-t TESTRUN] [-c CMSSWVERSION]
                              [-j JDLFILENAME] [-m MEMORY] [-n NEVENTS]
                              [-cpu NCPU] [-r RANDOMNUMBER]

User inputs

optional arguments:
  -h, --help            show this help message and exit
  -i INPUTPATH, --inputpath INPUTPATH
                        tar file path
  -f TARFILE, --tarfile TARFILE
                        input tar file name
  -o OUTPUTPATH, --outputpath OUTPUTPATH
                        outputpath path of LHEFiles
  -od OUTPUTDIR, --outputdir OUTPUTDIR
                        Name of output directory
  -t TESTRUN, --testrun TESTRUN
                        is it a test run for check? True/False
  -c CMSSWVERSION, --cmsswversion CMSSWVERSION
                        cmssw version to be used
  -j JDLFILENAME, --jdlfilename JDLFILENAME
                        name of jdl file and its sh file
  -m MEMORY, --memory MEMORY
                        memory for condor jobs
  -n NEVENTS, --nevents NEVENTS
                        Total number of events to generate.
  -cpu NCPU, --ncpu NCPU
                        number of cpu to run
  -r RANDOMNUMBER, --randomnumber RANDOMNUMBER
                        random seed
```

# How to use

1. STEP: 1:
   ```bash
   python generate_lhe_condor.py -f <Proc_card_name.dat>
   ```
   This will create the `jdl` and `sh` file for the condor submission. 

2. STEP: 2: Submit the condor job using the file created by STEP:1.
