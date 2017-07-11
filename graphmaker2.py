#!/usr/bin/env python3

import modulemd
import subprocess
import string
import graphviz
from graphviz import Digraph
import pydot
import nahan


#read in and store input
with open("exampleinput.txt") as inputfile:
	content = [x.strip() for x in inputfile.readlines()]
	content = [x for x in content if x]
	big3 = content[content.index("infra_modules_start")+1:content.index("infra_modules_end")]
	custom = content[content.index("custom_modules_api_start")+1:content.index("custom_modules_api_end")]
	ignore = content[content.index("ignore_start")+1:content.index("ignore_end")]

#generate dot structure
dot = pydot.Dot(graph_type='digraph')

#establish nodes
for item in custom:

	deps = nahan.chasedeps(item)
	nahan.pastebig3(deps,ignore+["fedora-release","fedora-repos"])

	for key in deps:
		if nahan.isinbigthree(key) == "is-it":
			dot.add_node(pydot.Node(key, shape="box"))
		elif key == item:
			dot.add_node(pydot.Node(key))
		else:
			dot.add_node(pydot.Node(key,shape="plaintext"))
	#draw edges
	for key in deps:
		for value in deps[key]:
			dot.add_edge(pydot.Edge(key,value))

dot.write_svg("dot2.svg")

#constraint="false"