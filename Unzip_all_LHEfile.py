import sys
import os

source = "/eos/uscms/store/user/rasharma/MonteCarlo_Samples/"

print source

for root, dirs, filenames in os.walk(source):
	for f in filenames:
		filepath = root + os.sep + f
		if filepath.endswith(".gz"):
			print root
			print filepath
			os.system("mv "+filepath+" /tmp/rasharma/")
			print("listing all file in $PWD:")
			os.system("ls")
			os.system("gunzip /tmp/rasharma/"+f)
			os.system("mv /tmp/rasharma/unweighted_events.lhe "+root)
			print("\n\n#####################################\n\n")
