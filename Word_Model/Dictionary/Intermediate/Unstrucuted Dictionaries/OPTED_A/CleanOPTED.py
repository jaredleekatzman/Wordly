#!/usr/bin/python
# coding: latin-1

# CleanOPTED.py

# tim's mac py loc: /Applications/anaconda/bin/python

import subprocess
import pickle
import numpy
import os
import re
import sys

infile = sys.argv[1]
outfile = sys.argv[2]

pEx = re.compile("<P>.*</P>", re.IGNORECASE)
bEx = re.compile("(?<=<B>).*(?=</B>)", re.IGNORECASE)
defEx = re.compile("(?<=\) ).*(?=</P>)", re.IGNORECASE)

with open (outfile, "w") as outfile:
	with open ('clean.log', 'w') as logfile:
		for line in open(infile, 'rb'):
			line = line.strip()						# Isolate line
			if line == "":							# Ignore empty lines
				continue
			else:
				entry = pEx.search(line)
				if entry and entry.group():
					word = bEx.search(entry.group())
					defn = defEx.search(entry.group())
					print "{}\t{}\n".format(word.group(),defn.group())
					outfile.write("{}\t{}\n".format(word.group(),defn.group()))

				else:
					logfile.write("\nBAD LINE: {}".format(line))
