import sys
import os

source = "/eos/uscms/store/user/rasharma/MonteCarlo_Samples/"

print source

neglect1="VBFNLO_outputs"
neglect2="tWch"

for root, dirs, filenames in os.walk(source):
	for f in filenames:
		filepath = root + os.sep + f
		if filepath.find(neglect1) == -1:
			if filepath.find(neglect2) == -1:
				if filepath.endswith(".lhe"):
					#print root
					print filepath
