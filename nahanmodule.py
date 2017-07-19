#!/usr/bin/env python3

import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("command", help="graphone: generate dep graph and submodules for single target, graphmany: generate dep graph and modules for many targets, genmodule: generate modulemd for given api package set")
parser.add_argument("inputfile", help="path to input file")
#parser.add_argument("-n","--nopropose", help="don't draw proposed modules when graphing. WARNING: depreciated", action="store_true")
#parser.add_argument("-o","--outputfile", help="path to output file")
args = parser.parse_args()

if args.command == "graphone":
	#subprocess.run(["python3", "nomodulegraphmaker.py", args.inputfile])
	subprocess.run(["python3", "modulegraphmaker.py", args.inputfile])

elif args.command == "genmodule":
	subprocess.run(["python3", "generatemodulemd.py", args.inputfile])

elif args.command == "graphmany":
	subprocess.run(["python3", "manygraphmaker.py", args.inputfile])

else:
	print("Error! Unrecognized command.")