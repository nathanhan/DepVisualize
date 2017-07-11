#!/usr/bin/env python3

import modulemd
import subprocess
import string
import os

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
	#returns dictionary with runtime dependency packages as keys and rationale as values

def onetimeload(inframodules):

	dictionary = {}
	modfile = modulemd.ModuleMetadata()
	for location in inframodules:
		modfile.load(location)
		inframodulename = os.path.basename(location).split(".yaml")[0]
		dictionary[inframodulename] = modfile.api.rpms
	return dictionary

def readgraphmakerinput(file):

	with open(file) as inputfile:
		content = [x.strip() for x in inputfile.readlines()]
		content = [x for x in content if x]
		big3 = content[content.index("infra_modules_start")+1:content.index("infra_modules_end")]
		custom = content[content.index("custom_modules_api_start")+1:content.index("custom_modules_api_end")]
		ignore = content[content.index("ignore_start")+1:content.index("ignore_end")]
	return [big3,custom,ignore]

def isinbigthree(packname,loadedinfra):

	for key in loadedinfra:
		if packname == key:
			return "is-it"
		elif packname in loadedinfra[key]:
			return key
	return ""

def pastebig3(dictionary, toignore, big3):

	for key in big3:
		if key not in dictionary:
			dictionary[key] = []

	for key in list(dictionary):
		#if key is in big3, merge deps with big3 and remove from individual consideration
		if isinbigthree(key,big3) != "" and isinbigthree(key,big3) != "is-it":
			dictionary[isinbigthree(key,big3)]+=dictionary[key]
			del dictionary[key]
		else:

			for index, value in enumerate(list(dictionary[key])):
				#if value is in big3, replace with big3 name
				if isinbigthree(value,big3) != "" and isinbigthree(value,big3) != "is-it":
					dictionary[key][index] = isinbigthree(value,big3)
				#delete values matching toignore names
				elif value == "requested by user" or value in toignore:
					dictionary[key][index] = ""
#				if value == key:
#					dictionary[key][index] = ""
			#delete duplicate connections and empty values
			dictionary[key] = list(set([x for x in dictionary[key] if x]))
			#delete keys matching toignore names and empty keys
			if dictionary[key] == [] or key in toignore:
				del dictionary[key]

#def walkforloose(towalk, dictionary, big3):

#	for key in list(dictionary):
#		if no value in big3
