import sys
import os

source = "/eos/uscms/store/user/rasharma/MonteCarlo_Samples/VBFNLO_outputs/July262017/201_WPhadWMjj/"

print source

neglect1="MadGraph"
neglect2="tWch"

for root, dirs, filenames in os.walk(source):
	for f in filenames:
		filepath = root + os.sep + f
		if filepath.find(neglect1) == -1:
			if filepath.find(neglect2) == -1:
				if filepath.endswith(".lhe"):
					#print root
					print filepath
