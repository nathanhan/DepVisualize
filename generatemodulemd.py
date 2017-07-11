#!/usr/bin/env python3

import modulemd
import subprocess
import string
import nahan

#open and prep modulemd file to operate on
module = modulemd.ModuleMetadata()
module.load("yamls/postgresql.yaml")
module.components.clear_rpms()
module.clear_requires()

#depchase every api module, store in dict with what it's a dependency for
for item in module.api.rpms:

	finaldependencyinfo = nahan.chasedeps(item);
	#check if package is in Big 3 already, if so exclude in component section
	for key in finaldependencyinfo:
		if nahan.isinbigthree(key) != "":
			module.add_requires(nahan.isinbigthree(key),"f26")
		else:
			module.components.add_rpm(key,'FIXME: Runtime dependency for ' + ','.join(finaldependencyinfo[key]))

module.dump("out.yaml")
print(len(finaldependencyinfo))