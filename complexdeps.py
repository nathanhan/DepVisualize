#!/usr/bin/env python3

import modulemd
import subprocess
import string

module = modulemd.ModuleMetadata()
module.load("postgresql.yaml")
module.components.clear_rpms()

for item in module.api.rpms:

	test = subprocess.run(["depchase","-a", "x86_64","-c","Fedora-26-Beta-repos.cfg","-vv","resolve", item],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	rawresults = test.stdout

	#parse verbose info for depth
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

	for key in finaldependencyinfo:
		module.components.add_rpm(key,'FIXME: Runtime dependency for ' + ','.join(finaldependencyinfo[key]))

module.dump("out.yaml")
print(len(finaldependencyinfo))