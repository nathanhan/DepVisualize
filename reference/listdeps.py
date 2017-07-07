#!/usr/bin/env python3

import modulemd
import subprocess
import string

module = modulemd.ModuleMetadata()
module.load("postgres.yaml")
module.components.clear_rpms()

for item in module.api.rpms:
	results = subprocess.run(["depchase","-a", "x86_64","-c","Fedora-26-Beta-repos.cfg","resolve", item],stdout=subprocess.PIPE).stdout
	subprocess.run(["./outputparse.sh",item],input=results)
	with open(item+"-binary-packages-short.txt") as myfile:
	    data = myfile.read().split("\n")[:-1]
	    for package in data:
	    	module.components.add_rpm(package,"FIXME: build dependency for "+ item)

module.dump("out.yaml")

#module.components.rpms
#.decode("utf-8")

