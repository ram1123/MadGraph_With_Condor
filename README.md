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


# Few points noted/learned

1. If the seed value given to madgraph is too long then it throws error like:
   ```bash
   set maxjetflavor 5
   INFO: modify parameter maxjetflavor of the run_card.dat to 5 
   set iseed 6132039411
   INFO: modify parameter iseed of the run_card.dat to 6132039411 
   Do you want to edit a card (press enter to bypass editing)?
   /------------------------------------------------------------\
   |  1. param : param_card.dat                                 |
   |  2. run   : run_card.dat                                   |
   \------------------------------------------------------------/
    you can also
      - enter the path to a valid card or banner.
      - use the 'set' command to modify a parameter directly.
        The set option works only for param_card and run_card.
        Type 'help set' for more information on this command.
      - call an external program (ASperGE/MadWidth/...).
        Type 'help' for the list of available command
    [0, done, 1, param, 2, run, enter path]
   The answer to the previous question is not set in your input file
   Use 0 value
   INFO: Update the dependent parameter of the param_card.dat 
   Generating 5000 events with run name run_01
   survey  run_01 
   INFO: compile directory 
   Not able to open file /storage/local/data1/condor/execute/dir_41567/CMSSW_9_3_8/src/MG5_aMC_v2_6_5/LpNuWMhadJJ_EWK_LO_SM_mjj100_pTj10/crossx.html since no program configured.Please set one in ./input/mg5_configuration.txt
   compile Source Directory
   Using random number seed offset = 6132039411
   Error detected in "generate_events run_01"
   write debug file /storage/local/data1/condor/execute/dir_41567/CMSSW_9_3_8/src/MG5_aMC_v2_6_5/LpNuWMhadJJ_EWK_LO_SM_mjj100_pTj10/run_01_tag_1_debug.log 
   If you need help with this issue please contact us on https://answers.launchpad.net/mg5amcnlo
   MadGraph5Error : Random seed too large 6132039414 > 30081*30081
   INFO:  
   quit
   INFO:  
   quit
   ```
