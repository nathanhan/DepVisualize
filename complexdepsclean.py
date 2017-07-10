#!/usr/bin/env python3

import modulemd
import subprocess
import string

def simplifypackname(name):
	parseprocess = subprocess.run("./outputparse2.sh",input=(name+"\n").encode("utf-8"),stdout=subprocess.PIPE)
	return parseprocess.stdout.decode("utf-8")[:-1]

def chasedeps(packname):
	#run depchase verbose on packname package
	test = subprocess.run(["depchase","-a", "x86_64","-c","Fedora-26-Beta-repos.cfg","-vv","resolve", packname],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	rawresults = test.stdout

	#parse verbose info stdout from depchase for depth information
	depinfo = test.stderr.decode("utf-8").split("\n")
	depinfo2 = depinfo[depinfo.index("DEBUG:depchase:INFO")+1:][:-1]
	finaldependencyinfo = {}
	index = 0
	while len(depinfo2) > 2 :
		if depinfo2[index][1] == '─' and depinfo2[index+1][1] != '─':
			key = depinfo2[0]
			finaldependencyinfo[simplifypackname(key)] = list(set([simplifypackname(i) for i in [i.split(" requires")[0][2:] for i in depinfo2[1:index+1]]]))
			del depinfo2[:index+1]
			index=0
		else:
			index+=1
	finaldependencyinfo[simplifypackname(depinfo2[0])] = list(set([simplifypackname(i) for i in [i.split(" requires")[0][2:] for i in depinfo2[1:]]]))
	return finaldependencyinfo
	#returns dict with runtime dependency packages as keys and rationale as values

def isinbigthree(packname):
	#open Big 3 modulemd files to reference
	bruntime = modulemd.ModuleMetadata()
	bruntime.load("yamls/base-runtime.yaml")

	commonbuilddep = modulemd.ModuleMetadata()
	commonbuilddep.load("yamls/common-build-dependencies.yaml")
	
	sharedus = modulemd.ModuleMetadata()
	sharedus.load("yamls/shared-userspace.yaml")

	if packname in bruntime.components.rpms:
		return "base-runtime"
	elif packname in commonbuilddep.components.rpms:
		return "common-build-dependencies"
	elif packname in sharedus.components.rpms:
		return "shared-userspace"
	else:
		return ""