#! /usr/bin/env python

import os
import argparse
import datetime

def getbasic_parser():
    parser = argparse.ArgumentParser(description='User inputs')

    parser.add_argument('-i', '--inputpath',
                        default='/store/user/lnujj/VVjj_aQGC/Gridpacks/',
                        help='tar file path'
                       )
    parser.add_argument('-f', '--tarfile',
                        required=True,
                        help='input tar file name'
                       )
    parser.add_argument('-o', '--outputpath',
                        default='/store/user/lnujj/VVjj_aQGC/LHEFiles/',
                        help='outputpath path of LHEFiles'
                       )
    parser.add_argument('-od', '--outputdir',
                        default='LpNuWMhadJJ_EWK_LO_SM_mjj100_pTj10',
                        help='Name of output directory'
                       )
    parser.add_argument('-t', '--testrun',
                        default=True,
                        help='is it a test run for check? True/False'
                       )
    parser.add_argument('-c', '--cmsswversion',
                        default='CMSSW_9_3_8',
                        help='cmssw version to be used'
                       )
    parser.add_argument('-j', '--jdlfilename',
                        default='run_mg5_condor',
                        help='name of jdl file and its sh file'
                       )
    parser.add_argument('-m', '--memory',
    			default=5000,
			help='memory for condor jobs'
		       )
    return parser

def create_output_directory(args):
    """
    This function will create two directories.
    - First directory will be created in PWD for storing the log files
    - Another directory will be created in eos for storing the outputs
    """
    if args.testrun:
        output_folder = args.outputpath+datetime.datetime.now().strftime('%Y_%m_%d_%Hh%M')+"_TEST/"
        output_log_path = "output_logs/" + datetime.datetime.now().strftime('%Y_%m_%d_%Hh%M') + "_TEST"
        print "Name of output dir: ", output_folder
    else:
        os.system('xrdfs root://cmseos.fnal.gov/ mkdir ' + args.outputpath + args.outputdir)
        output_folder = args.outputpath+args.outputdir+"/"+datetime.datetime.now().strftime('%Y_%m_%d_%Hh%M')
        output_log_path = "output_logs/" + args.outputdir+"/"+ datetime.datetime.now().strftime('%Y_%m_%d_%Hh%M')
        print "Name of output directory    : ", output_folder
	print "Name of output log directory: ",output_log_path

    # create directory in eos for output files
    os.system('xrdfs root://cmseos.fnal.gov/ mkdir ' + output_folder)
    # create directory in pwd for log files
    os.system('mkdir -p ' + output_log_path)
    return output_folder, output_log_path

def exclude_function(filename):
    """
    Function that returns True/False if the filename ends with
    *.log  or *.stdout
    Input arguments:
    filename    Name of file
    """
    return bool(filename.endswith('.log') or filename.endswith('.stdout'))

def make_tarfile(output_filename, source_dir):
    """
    Function to create the tar file.
    Input arguments:
    output_filename     Name of output file
    source_dir          path of source directory to make tar file
    """
    import tarfile
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def create_jdl_file_for_condor(args, inputlist, output_log_path):
    outjdl_file = open(args.jdlfilename+".jdl", "w")
    outjdl_file.write("Executable = "+args.jdlfilename+".sh\n")
    outjdl_file.write("Universe = vanilla\n")
    #outjdl_file.write("Requirements =FileSystemDomain==\"fnal.gov\" && Arch==\"X86_64\"")
    outjdl_file.write("Notification = ERROR\n")
    outjdl_file.write("Should_Transfer_Files = YES\n")
    outjdl_file.write("WhenToTransferOutput = ON_EXIT\n")
    outjdl_file.write("request_memory = "+str(args.memory)+"\n")
    outjdl_file.write("request_cpus = 8\n")
    #outjdl_file.write("include : list-infiles.sh |\n")
    if inputlist != "":
        outjdl_file.write("Transfer_Input_Files = "+inputlist+"\n")
    outjdl_file.write("x509userproxy = $ENV(X509_USER_PROXY)\n")

    outjdl_file.write("Output = "+output_log_path+"/"+args.outputdir+"_$(Process).stdout\n")
    outjdl_file.write("Error  = "+output_log_path+"/"+args.outputdir+"_$(Process).stdout\n")
    outjdl_file.write("Log  = "+output_log_path+"/"+args.outputdir+"_$(Process).log\n")
    outjdl_file.write("Arguments = $(Process) $(Cluster)\n")
    outjdl_file.write("Queue 5\n")

def create_sh_file_for_condor(args, command, output_folder):
    outscript = open(args.jdlfilename+".sh", "w")
    outscript.write('#!/bin/bash')
    outscript.write("\n"+'echo "Starting job on " `date`')
    outscript.write("\n"+'echo "Running on: `uname -a`"')
    outscript.write("\n"+'echo "System software: `cat /etc/redhat-release`"')
    outscript.write("\n"+'source /cvmfs/cms.cern.ch/cmsset_default.sh')
    outscript.write("\n"+'export SCRAM_ARCH=slc6_amd64_gcc530')
    outscript.write("\n"+'eval `scramv1 project CMSSW '+args.cmsswversion+'`')
    outscript.write("\n"+'cd '+ args.cmsswversion + '/src/')
    outscript.write("\n"+'eval `scram runtime -sh`')
    outscript.write("\n"+'wget https://launchpad.net/mg5amcnlo/2.0/2.6.x/+download/MG5_aMC_v2.6.5.tar.gz')
    outscript.write("\n"+'tar -xf MG5_aMC_v2.6.5.tar.gz')
    outscript.write("\n"+'cd MG5_aMC_v2_6_5')
    outscript.write("\n"+'cp ../../../'+args.tarfile+' .')
    outscript.write("\n"+'echo "====> List files : " ')
    outscript.write("\n"+'ls -alh')
    outscript.write("\n"+'sed -i "s/39/$1/g" '+args.tarfile)
    outscript.write("\n"+"=================================")
    outscript.write("\n"+"cat "+args.tarfile)
    outscript.write("\n"+"=================================")
    outscript.write("\n"+command)
    outscript.write("\n"+'echo "====> List files : " ')
    outscript.write("\n"+'ls -alh')
    outscript.write("\n"+'echo "====> List only LHE files : " ')
    outscript.write("\n"+'ls LpNuWMhadJJ_EWK_LO_SM_mjj100_pTj10/')
    outscript.write("\n"+'echo "====> List only LHE files : " ')
    outscript.write("\n"+'ls LpNuWMhadJJ_EWK_LO_SM_mjj100_pTj10/Events/')
    outscript.write("\n"+'echo "====> List only LHE files : " ')
    outscript.write("\n"+'ls LpNuWMhadJJ_EWK_LO_SM_mjj100_pTj10/Events/run_01/')
    outscript.write("\n"+'echo "====> copying *.lhe file to stores area..." ')
    outscript.write("\n"+'xrdcp -f LpNuWMhadJJ_EWK_LO_SM_mjj100_pTj10/Events/run_01/*.lhe.gz root://cmseos.fnal.gov/' + output_folder+'/'+args.tarfile+'_'+'${1}'+'.lhe.gz')
    outscript.write("\n"+'echo "End job on " `date`')
    outscript.write("\n"+'cd ${_CONDOR_SCRATCH_DIR}')
    outscript.write("\n"+'rm -rf ' + args.cmsswversion)
    outscript.write("\n")
    outscript.close()
    os.system("chmod 777 "+args.jdlfilename+".sh")
