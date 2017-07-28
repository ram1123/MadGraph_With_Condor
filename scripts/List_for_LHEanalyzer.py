import sys
import os

source = "/eos/uscms/store/user/rasharma/MonteCarlo_Samples/VBFNLO_outputs/July262017/"

print source

#neglect1="VBFNLO_outputs"
neglect1="Events"
neglect2="tWch"

#include="202_WPWMhadjj"
include="jj"

for root, dirs, filenames in os.walk(source):
	for f in filenames:
		filepath = root + os.sep + f
		if filepath.find(neglect1) == -1:
			if filepath.find(neglect2) == -1:
				if filepath.find(include) != -1:
					if filepath.endswith(".lhe"):
						#print root
						#print filepath
						print "./LHEanalyzer "+filepath+" "+filepath.replace("lhe","root")
