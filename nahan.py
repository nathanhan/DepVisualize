#!/usr/bin/env python3

import modulemd
import subprocess
import string

def simplifypackname(name):
	parseprocess = subprocess.run("./outputparse2.sh",input=(name+"\n").encode("utf-8"),stdout=subprocess.PIPE)
	return parseprocess.stdout.decode("utf-8")[:-1]

#wrapper for depchase
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

#open Big 3 modulemd files to reference, need this outside since modulemd forgets to close file streams
bruntime = modulemd.ModuleMetadata()
bruntime.load("yamls/base-runtime.yaml")

commonbuilddep = modulemd.ModuleMetadata()
commonbuilddep.load("yamls/common-build-dependencies.yaml")

sharedus = modulemd.ModuleMetadata()
sharedus.load("yamls/shared-userspace.yaml")

def isinbigthree(packname):

	if packname in bruntime.components.rpms:
		return "base-runtime"
	elif packname in commonbuilddep.components.rpms:
		return "common-build-dependencies"
	elif packname in sharedus.components.rpms:
		return "shared-userspace"
	elif packname in ["base-runtime","shared-userspace","common-build-dependencies"]:
		return "is-it"
	else:
		return ""

#MASKED FOR BIG3 DEPENDENCIES
def pastebig3(dict):

	dict["base-runtime"] = []
	dict["shared-userspace"] = []
	dict["common-build-dependencies"] = []

	for key in list(dict):
		if isinbigthree(key) != "" and isinbigthree(key) != "is-it":
			dict[isinbigthree(key)]+=dict[key]
			del dict[key]
		else:
			for index, value in enumerate(list(dict[key])):
				if isinbigthree(value) != "": #or value not in list(dict):
					dict[key][index] = isinbigthree(value)#""

	for key in list(dict):
		dict[key] = list(set([x for x in dict[key] if x]))
		#if dict[key] == []:
		#	del dict[key]
		#if key not in dict.values() and key != "postgresql":
		#	del dict[key]

#old FULL FUNCTIONING: replace entries in dependency dictionary with big3 names
#def pastebig3(dict):
#
#	dict["base-runtime"] = []
#	dict["shared-userspace"] = []
#	dict["common-build-dependencies"] = []
#
#	for key in list(dict):
#		if isinbigthree(key) != "" and isinbigthree(key) != "is-it":
#			dict[isinbigthree(key)]+=dict[key]
#			del dict[key]
#		else:
#			for index, value in enumerate(list(dict[key])):
#				if isinbigthree(value) != "":
#					if isinbigthree(key)!= "is-it":
#						dict[key][index] = isinbigthree(value)
#					else:
#						dict[key][index] = ""
#
#	#prune all self-references within big 3 modules
#	dict["base-runtime"] = [x for x in dict["base-runtime"] if x]
#	dict["shared-userspace"] = [x for x in dict["shared-userspace"] if x]
#	dict["common-build-dependencies"] = [x for x in dict["common-build-dependencies"] if x]