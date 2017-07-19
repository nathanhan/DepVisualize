#!/usr/bin/env python3

import modulemd
import subprocess
import string
import pydot
import nahan
import re
import sys

#read in and store input
if len(sys.argv) < 2:
	print("error! sys.argv too small. need argument for path to input file")
big3, custom, ignore = nahan.readgraphmakerinput(sys.argv[1])
big3 = nahan.onetimeload(big3)

#generate dot structure
dot = pydot.Dot(graph_type='digraph',simplify=True)

#initialize labeling
innerlabel = {}
for key in big3:
	innerlabel[key] = []
 
unifieddeps = {}

print("chasing everything at once")
deps = nahan.chasedeps(custom)
tolabel = nahan.pastebig3(deps,ignore+["fedora-release","fedora-repos"], big3)

print("drawing everything at once")
#initialize label tracking
for key in list(tolabel):
	innerlabel[key]+=list(tolabel[key])

#draw nodes
for key in deps:
	if nahan.isinbigthree(key, big3) == "is-it":
		dot.add_node(pydot.Node(key, shape="box"))
	elif key in custom:
		dot.add_node(pydot.Node(key))
	else:
		dot.add_node(pydot.Node(key,shape="plaintext"))
#draw edges
for key in deps:
	for value in deps[key]:
		dot.add_edge(pydot.Edge(key,value))

for key in deps:
	if key in unifieddeps:
		unifieddeps[key] += deps[key]
	else:
		unifieddeps[key] = deps[key]

#draw subgraphs around logical modules
print("drawing logical modules...")
for item in custom:
	logicalmod = pydot.Cluster(item, fontname="Arial Bold",label = "proposed for " + item, style="filled", color="lightgrey")
	lookuptable = [item]
	nahan.get_loose(lookuptable,unifieddeps,big3)
	#print(lookuptable)
	for key in lookuptable:
		if dot.get_node(key):
			nodename = key
		else:
			nodename = '"' + key + '"'
		#print(nodename)
		logicalmod.add_node(dot.get_node(nodename)[0])
		dot.del_node(dot.get_node(nodename)[0])
	dot.add_subgraph(logicalmod)

#label box nodes with innards plus highlights
for key in big3:
	if [x for x in innerlabel[key] if x in custom]:
		finallabel = key + "\n" + "\n".join([x for x in innerlabel[key] if x in custom])
		dot.add_node(pydot.Node(key, shape = "box",label=finallabel,color="red"))

outputfilename = 'graph.svg'
dot.write_svg(outputfilename)
print("success! output to " + outputfilename)