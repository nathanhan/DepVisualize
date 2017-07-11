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

#generate dot structure
dot = Digraph(comment="graph for " + ",".join(custom),format="svg")

#establish nodes
for item in custom:

	deps = nahan.chasedeps(item)
	nahan.pastebig3(deps)

	for key in deps:
		if nahan.isinbigthree(key) == "is-it":
			dot.node(key,key,constraint="false")
		else:
			dot.node(key,key,shape="plaintext", constraint="false")

#draw edges
for key in deps:
	for value in deps[key]:
		dot.edge(key,value)

dot.render(view=True)