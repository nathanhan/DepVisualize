#!/usr/bin/env python3

import modulemd
import subprocess
import string
import nahan

#read in and store input
big3, custom, ignore = nahan.readgraphmakerinput("graphmaker_input.txt")
big3 = nahan.onetimeload(big3)

#open and prep modulemd file to operate on
module = modulemd.ModuleMetadata()
module.load("yamls/system-tools.yaml")
module.components.clear_rpms()
module.clear_requires()

#depchase every api module, store in dict with what it's a dependency for
for item in module.api.rpms:

	print("chasing " + item)
	finaldependencyinfo = nahan.chasedeps(item);
	#check if package is in Big 3 already, if so exclude in component section
	for key in finaldependencyinfo:
		if nahan.isinbigthree(key, big3) != "":
			module.add_requires(nahan.isinbigthree(key, big3),"f26")
		else:
			module.components.add_rpm(key,'FIXME: Runtime dependency for ' + ','.join(finaldependencyinfo[key]))

module.dump("out.yaml")
print("results dumped to out.yaml")
#print(len(finaldependencyinfo))