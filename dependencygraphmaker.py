#!/usr/bin/env python3

import nahan

#read in and store input
big3, custom, ignore = nahan.readgraphmakerinput("graphmaker_input.txt")
big3 = nahan.onetimeload(big3)

for item in custom:

	deps = nahan.chasedeps(item)
	nahan.pastebig3(deps,ignore+["fedora-release","fedora-repos"], big3)

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

dot.write_svg("dot.svg")