import sys
import os

source = "/eos/uscms/store/user/rasharma/MonteCarlo_Samples/VBFNLO_outputs/July262017/"

print "\n======================================="
print "This is the name of the script: ", sys.argv[0]
print "Number of arguments: ", len(sys.argv)
print "The arguments are: " , str(sys.argv)

print source

neglect1="Events"
neglect2="tWch"

#include="WMlepWMhadJJ_SM_LO_EWK_mjj100_pTj10"
include=str(sys.argv[1])
#print "Include = ",include

#print "hadd "+include+".root ",
command="hadd -f "+include+"_VBFNLO.root "

for root, dirs, filenames in os.walk(source):
	for f in filenames:
		filepath = root + os.sep + f
		if filepath.find(neglect1) == -1:
			if filepath.find(neglect2) == -1:
				if filepath.find(include) != -1:
					if filepath.endswith("event.root"):
						#print root
						print filepath
						command+=" "+filepath+" "
print command
os.system(command)
