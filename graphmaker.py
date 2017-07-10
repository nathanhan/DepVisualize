#!/usr/bin/env python3

import modulemd
import subprocess
import string
import graphviz
from graphviz import Digraph
import complexdepsclean

#read in and store input
with open("exampleinput.txt") as inputfile:
	content = [x.strip() for x in f.readlines()]
	content = [x for x in content if x]
	big3 = content[content.index("infra_modules_start")+1:content.index("infra_modules_end")]
	custom = content[content.index("custom_modules_api_start")+1:content.index("custom_modules_api_end")]

#generate dot file
dot = Digraph(comment="graph for " + ",".join(custom))

#copy paste from modulemd generator script starts here
for item in custom:
	finaldependencyinfo = chasedeps(item)
	if isinbigthree(key) != "":
		dot.node(item,item,shape="plaintext")
	else:
		module.components.add_rpm(key,'FIXME: Runtime dependency for ' + ','.join(finaldependencyinfo[key]))
