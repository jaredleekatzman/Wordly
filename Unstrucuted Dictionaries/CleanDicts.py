#!/usr/bin/python
# coding: latin-1

# CleanDicts.py

# tim's mac py loc: /Applications/anaconda/bin/python

import subprocess
import pickle
import numpy
import os
import re
import sys

mode = sys.argv[1]
infile = sys.argv[2]
outfile = sys.argv[3]

wordEx = re.compile("^.+?(?= prefix| +n\.| +v\.| +pl\.| +adj\.| +abbr\.| +contr\.| +symb\.| +slang| +int\.| +poss\.| +pron\.| +adv\.| +naut\.| +colloq\.| +—n\.| +—v\.| +—pl\.| +—adj\.| +—[aA]bbr\.| +—contr\.| +—symb\.| +—slang| +—int\.| +—poss\.| +—pron\.| +—adv\.| +—naut\.| +—colloq\.| +—prep\.| +prep\.| +suffix| +archaic| +past part\.| +predic\.| +attrib\.| +comb\.| +interrog\.| +conj\.| +—predic\.| +—attrib\.| +—comb\.| +—interrog\.| +—conj\.| +\(| +gram\.| +mus\.| +—gram\.| +—mus\.| +[0-9]| +—[0-9]| +coarse| +—coarse)", re.IGNORECASE)

# (?<=\) | [0-9]).*(?= [0-9]|\[|$)
# (?<=\)| +prefix| +n\.| +v\.| +pl\.| +adj\.| +abbr\.| +contr\.| +symb\.| +slang| +int\.| +poss\.| +pron\.| +adv\.| +naut\.| +colloq\.| +—n\.| +—v\.| +—pl\.| +—adj\.| +—[aA]bbr\.| +—contr\.| +—symb\.| +—slang| +—int\.| +—poss\.| +—pron\.| +—adv\.| +—naut\.| +—colloq\.| +—prep\.| +prep\.| +suffix| +archaic| +past part\.| +predic\.| +attrib\.| +comb\.| +interrog\.| +conj\.| +—predic\.| +—attrib\.| +—comb\.| +—interrog\.| +—conj\.| +\(| +gram\.| +mus\.| +—gram\.| +—mus\.| +[0-9]| +—[0-9]| +coarse| +—coarse).*

defEx = re.compile("(?<=slang|refix|oarse)|(?<=[0-9] |\) |\. |\; ).*(?= [0-9]| \[|$)", re.IGNORECASE)
splitEx = re.compile(" prefix| +n\.| +v\.| +pl\.| +adj\.| +abbr\.| +contr\.| +symb\.| +slang| +int\.| +poss\.| +pron\.| +adv\.| +naut\.| +colloq\.| +—n\.| +—v\.| +—pl\.| +—adj\.| +—[aA]bbr\.| +—contr\.| +—symb\.| +—slang| +—int\.| +—poss\.| +—pron\.| +—adv\.| +—naut\.| +—colloq\.| +—prep\.| +prep\.| +suffix| +archaic| +past part\.| +predic\.| +attrib\.| +comb\.| +interrog\.| +conj\.| +—predic\.| +—attrib\.| +—comb\.| +—interrog\.| +—conj\.| +gram\.| +mus\.| +—gram\.| +—mus\.| +[0-9]| +—[0-9]| +coarse| +—coarse|\[.*\]", re.IGNORECASE)

parenEx = re.compile("\(\W*(?:-ting|usu\.|prefix|n\.|v\.|pl\.|adj\.|abbr\.|contr\.|symb\.|slang|int\.|poss\.|pron\.|adv\.|naut\.|colloq\.|—n\.|—v\.|—pl\.|—adj\.|—[aA]bbr\.|—contr\.|—symb\.|—slang|—int\.|—poss\.|—pron\.|—adv\.|—naut\.|—colloq\.|—prep\.|prep\.|suffix|archaic|past part\.|predic\.|attrib\.|comb\.|interrog\.|conj\.|—predic\.|—attrib\.|—comb\.|—interrog\.|—conj\.|gram\.|mus\.|—gram\.|—mus\.|[0-9]|—[0-9]|coarse|—coarse|-*refl.|-*sing)[^\)]*\)", re.IGNORECASE)

#  [ABCDEFGHJKLMNOPQRSTUVWXYZ&] 
letterEx = re.compile(" [ABCDEFGHJKLMNOPQRSTUVWXYZ&] ")

with open (outfile, "w") as outfile:
	if mode == "oxford":
		for line in open(infile, 'rb'):
			line = line.strip()						# Isolate line
			if line == "":							# Ignore empty lines
				continue
			else:
				word = wordEx.search(line)
				if word and "  " not in word.group():
					definition = re.sub(wordEx, "", line, 1)#defEx.findall(line)
					#for defn in definitions:
					outfile.write("{}\n".format(word.group()))

					splits = re.split(splitEx, definition)
					for defn in splits:
						if defn and defn != "" and defn != " ":
							splits2 = re.split(parenEx, defn)
							for defn2 in splits2:
								if defn2 and defn2 != "" and defn2 != " ":
									splits3 = re.split(letterEx, defn2)
									for defn3 in splits3:
										if defn3 and defn3 != "" and defn3 != " ":
											outfile.write(":\t{}\n".format(defn3.strip()))
				else:
					print "{}".format(line)

# filepath = sys.argv[1]
# print "Printing to: {}".format(filepath)

# start = 0
# stop = len(words)

# if len(sys.argv)>2:
# 	start = int(sys.argv[2])
# 	stop = int(sys.argv[3])

# print "Start: {}".format(start)
# print "Stop: {}".format(stop)

# # Initialize data structures
# num_definitions = {}
# text_definitions = {}
# DefWordEmbed = []

# # Error counters
# misses = 0
# defMisses = 0
# senseMisses = 0
# pureMisses = 0
# badMisses = 0
# errors = 0

# # Define RegEx
# senseEx = re.compile("(?<=-- \().*(?=\))")
# defEx = re.compile("^[^\"]+?(?=;)|(?<=; )[^\"]+?(?=;|\)|$)|^[^\"]+?(?=;|\)|$|,|:)")

# with open (filepath, "w") as myfile:
# 	for i, word in enumerate(words[start:stop]):
# 		try:
# 			word = str(word).replace(" ", "_")
# 		except Exception:
# 			badMisses= 1
# 			misses += 1
# 			continue

# 		# if re.search("\W", word):
# 		# 	print "bad word: {}".format(word)
# 		# 	badMisses += 1
# 		# 	misses += 1
# 		# 	continue

# 		process = subprocess.Popen("wn \"{}\" -over".format( word ), stdout=subprocess.PIPE, shell=True)
# 		out, err = process.communicate()
# 		text_definitions[word] = out
# 		num_definitions[word] = process.returncode

# 		if num_definitions[word] == -1:
# 			# print "Error."
# 			errors += 1
# 			continue
# 		elif num_definitions[word] == 0:
# 			# print "Miss."
# 			print "missed word: {}".format(word)
# 			misses += 1
# 			pureMisses += 1
# 			continue

# 		senses = senseEx.findall(text_definitions[word])

# 		if len(senses)==0:
# 			if re.search("\W", word):
# 				# print "bad word: {}".format(word)
# 				badMisses += 1
# 				misses += 1
# 			else:
# 				# print "\nInner miss: senses"
# 				# print "word: {}".format(word)
# 				# print "def: {}\n".format(text_definitions[word])
# 				misses += 1
# 				senseMisses += 1

# 		for sense in senses:
# 			defs = defEx.findall(sense)

# 			if len(defs)==0:
# 				# print "Inner miss: defs"
# 				# print "word: {}".format(word)
# 				# print "sense: {}\n".format(sense)
# 				misses += 1
# 				defMisses += 1

# 			for definition in defs:
# 				# For managing tuples:
# 				# tup = (definition, word, embeddings[i])
# 				# DefWordEmbed.append(tup)

# 				# print "{}\t{}".format(word,definition)
# 				myfile.write("{}\t{}\n".format(word,definition))

# print "Errors: {}".format(errors)
# print "Misses: {}".format(misses)
# print "\tDef: {}".format(defMisses)
# print "\tSense: {}".format(senseMisses)
# print "\tPure: {}".format(pureMisses)
# print "\tBad: {}".format(badMisses)

# #--------------------------------------------------------------------------------------------------
# # REGEX rubular
# # Match definition within parens: (?<=-- \().*(?=\))
# # sub-regex, match lines without quotes; within above: ^[^\"]+?(?=;)|(?<=; )[^\"]+?(?=;|\)|$)
# # to include in-context usage /* outdated, check */: [^"]*?(?=;)|(?<=").*?(?=")
# # how to value frequency in tagged text?
# # include sysnonyms?

# # Test text:
# # Overview of adj certain

# # The adj certain has 7 senses (first 4 from tagged texts)
                                         
# # 1. (131) certain -- (definite but not specified or identified; "set aside a certain sum each week"; "to a certain degree"; "certain breeds do not make good pets"; "certain members have not paid their dues"; "a certain popular teacher"; "a certain Mrs. Jones")
# # 2. (16) certain, sure -- (having or feeling no doubt or uncertainty; confident and assured; "felt certain of success"; "was sure (or certain) she had seen it"; "was very sure in his beliefs"; "sure of her friends")
# # 3. (8) certain -- (established beyond doubt or question; definitely known; "what is certain is that every effect must have a cause"; "it is certain that they were on the bus"; "his fate is certain"; "the date for the invasion is certain")
# # 4. (4) certain, sure -- (certain to occur; destined or inevitable; "he was certain to fail"; "his fate is certain"; "In this life nothing is certain but death and taxes"- Benjamin Franklin; "he faced certain death"; "sudden but sure regret"; "he is sure to win")
# # 5. sealed, certain -- (established irrevocably; "his fate is sealed")
# # 6. certain, sure -- (reliable in operation or effect; "a quick and certain remedy"; "a sure way to distinguish the two"; "wood dust is a sure sign of termites")
# # 7. certain, sure -- (exercising or taking care great enough to bring assurance; "be certain to disconnect the iron when you are through"; "be sure to lock the doors")
# #--------------------------------------------------------------------------------------------------
