#!/usr/bin/env python3

import modulemd
import subprocess
import string

#open and prep modulemd file to operate on
module = modulemd.ModuleMetadata()
module.load("postgresql.yaml")
module.components.clear_rpms()
module.clear_requires()

#open Big 3 modulemd files to reference
bruntime = modulemd.ModuleMetadata()
bruntime.load("base-runtime.yaml")

commonbuilddep = modulemd.ModuleMetadata()
commonbuilddep.load("common-build-dependencies.yaml")

sharedus = modulemd.ModuleMetadata()
sharedus.load("shared-userspace.yaml")

#depchase every api module, store in dict with what it's a dependency for
for item in module.api.rpms:

	test = subprocess.run(["depchase","-a", "x86_64","-c","Fedora-26-Beta-repos.cfg","-vv","resolve", item],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	rawresults = test.stdout

	#parse verbose info stdout from depchase for depth information
	depinfo = test.stderr.decode("utf-8").split("\n")
	depinfo2 = depinfo[depinfo.index("DEBUG:depchase:INFO")+1:][:-1]
	finaldependencyinfo = {}
	index = 0
	while len(depinfo2) > 2 :
		if depinfo2[index][1] == '─' and depinfo2[index+1][1] != '─':
			key = depinfo2[0]
			finaldependencyinfo[subprocess.run("./outputparse2.sh",input=(key+"\n").encode("utf-8"),stdout=subprocess.PIPE).stdout.decode("utf-8")[:-1]] = list(set([subprocess.run("./outputparse2.sh",input=(i+"\n").encode("utf-8"),stdout=subprocess.PIPE).stdout.decode("utf-8")[:-1] for i in [i.split(" requires")[0][2:] for i in depinfo2[1:index+1]]]))
			del depinfo2[:index+1]
			index=0
		else:
			index+=1
	finaldependencyinfo[subprocess.run("./outputparse2.sh",input=(depinfo2[0]+"\n").encode("utf-8"),stdout=subprocess.PIPE).stdout.decode("utf-8")[:-1]] = list(set([subprocess.run("./outputparse2.sh",input=(i+"\n").encode("utf-8"),stdout=subprocess.PIPE).stdout.decode("utf-8")[:-1] for i in [i.split(" requires")[0][2:] for i in depinfo2[1:]]]))
	print(finaldependencyinfo)

	#check if package is in Big 3 already, if so exclude in component section
	for key in finaldependencyinfo:
		if key in bruntime.components.rpms:
			module.add_requires("base-runtime","f26")
		elif key in commonbuilddep.components.rpms:
			module.add_requires("common-build-dependencies","f26")
		elif key in sharedus.components.rpms:
			module.add_requires("shared-userspace","f26")
		else:
			module.components.add_rpm(key,'FIXME: Runtime dependency for ' + ','.join(finaldependencyinfo[key]))

module.dump("out.yaml")
print(len(finaldependencyinfo))