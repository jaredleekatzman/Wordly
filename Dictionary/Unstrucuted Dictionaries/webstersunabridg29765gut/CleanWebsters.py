#!/usr/bin/python
# coding: latin-1

# CleanWebsters.py

# tim's mac py loc: /Applications/anaconda/bin/python

import subprocess
import pickle
import numpy
import os
import re
import sys

import subprocess
import pickle
import numpy
import os
import re
import sys

infile = sys.argv[1]
outfile = sys.argv[2]

wordEx = re.compile("^[^a-z*]+(?:(?=\W)|$)")
prewordEx = re.compile("^[^a-z]+(?=;|$)")
filterwordsEx = re.compile("^[^;\.]*(?=;|$)")
defEx = re.compile("(?<=Defn: ).*")

# (?<=Defn: ).*(?=\n\n)

# bwWords = ""
# paragraph = ""
# bwct = 0
# wordFlag = False
# words = []
currentWord=""
defFlag = False
defn = ""

with open (outfile, "w") as outfile:
	with open ('clean.log', 'w') as logfile:
		for line in open(infile, 'rb'):

			word = wordEx.search(line.strip())
			preword = prewordEx.search(line.strip())
			definition = defEx.search(line.strip())

			# print "line:"
			# print line
			# print "word:"
			# print word
			# print "preword:"
			# print preword
			# print "definition:"
			# print definition
			# print "definition:"
			# print definition
			# print "flag:"
			# print defFlag
			# print '\n'

			if word or preword:
				if preword==None and word:
					logfile.write("\t\t{}".format(line))
				elif preword==None:
					logfile.write("\t\t\t{}".format(line))
				elif word==None and preword:
					print preword.group()
				else:
					word = filterwordsEx.search(word.group())
					if word:
						currentWord = word.group()
						print "WORD:"
						print currentWord
						logfile.write("\n{}".format(word.group()))
			else:
				print "{}:{}".format(defFlag, line.strip())
				if line.strip()=="" and defFlag:
					print "off"
					defFlag = False
					defn = ""
				elif defFlag:
					print "add"
					defn = line.strip()
					outfile.write(" {}".format(defn))
				elif definition:
					print "on"
					defFlag = True
					defn = definition.group()
					outfile.write("\n{}\t{}".format(currentWord,defn))