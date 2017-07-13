#!/usr/bin/env python3

import modulemd
import subprocess
import string
import pydot
import nahan


#read in and store input
big3, custom, ignore = nahan.readgraphmakerinput("graphmaker_input.txt")
big3 = nahan.onetimeload(big3)

#generate dot structure
dot = pydot.Dot(graph_type='digraph',simplify=True)

#initialize labeling
innerlabel = {}
for key in big3:
	innerlabel[key] = []

for item in custom:

	print("handling " + item)
	deps = nahan.chasedeps(item)
	
	#initialize label tracking
	tolabel = nahan.pastebig3(deps,ignore+["fedora-release","fedora-repos"], big3)
	for key in list(tolabel):
		innerlabel[key]+=list(tolabel[key])

	#draw nodes
	for key in deps:
		if nahan.isinbigthree(key, big3) == "is-it":
			dot.add_node(pydot.Node(key, shape="box"))
		elif key == item:
			dot.add_node(pydot.Node(key))
		else:
			dot.add_node(pydot.Node(key,shape="plaintext"))
	#draw edges
	for key in deps:
		for value in deps[key]:
			dot.add_edge(pydot.Edge(key,value))

#label box nodes with innards plus highlights
for key in big3:
	if [x for x in innerlabel[key] if x in custom]:
		finallabel = key + "\n" + "\n".join([x for x in innerlabel[key] if x in custom])
		dot.add_node(pydot.Node(key, shape = "box",label=finallabel,color="red"))

dot.write_svg("dot.svg")