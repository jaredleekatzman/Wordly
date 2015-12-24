#!/usr/bin/python
# coding: latin-1

# CleanOxford.py

# tim's mac py loc: /Applications/anaconda/bin/python

import subprocess
import pickle
import numpy
import os
import re
import sys

infile = sys.argv[1]
outfile = sys.argv[2]

wordEx = re.compile("^.+?(?= prefix| +n\.| +v\.| +pl\.| +adj\.| +abbr\.| +contr\.| +symb\.| +slang| +int\.| +poss\.| +pron\.| +adv\.| +naut\.| +colloq\.| +—n\.| +—v\.| +—pl\.| +—adj\.| +—[aA]bbr\.| +—contr\.| +—symb\.| +—slang| +—int\.| +—poss\.| +—pron\.| +—adv\.| +—naut\.| +—colloq\.| +—prep\.| +prep\.| +suffix| +archaic| +past part\.| +predic\.| +attrib\.| +comb\.| +interrog\.| +conj\.| +—predic\.| +—attrib\.| +—comb\.| +—interrog\.| +—conj\.| +\(| +gram\.| +mus\.| +—gram\.| +—mus\.| +[0-9]| +—[0-9]| +coarse| +—coarse)", re.IGNORECASE)

# (?<=\) | [0-9]).*(?= [0-9]|\[|$)
# (?<=\)| +prefix| +n\.| +v\.| +pl\.| +adj\.| +abbr\.| +contr\.| +symb\.| +slang| +int\.| +poss\.| +pron\.| +adv\.| +naut\.| +colloq\.| +—n\.| +—v\.| +—pl\.| +—adj\.| +—[aA]bbr\.| +—contr\.| +—symb\.| +—slang| +—int\.| +—poss\.| +—pron\.| +—adv\.| +—naut\.| +—colloq\.| +—prep\.| +prep\.| +suffix| +archaic| +past part\.| +predic\.| +attrib\.| +comb\.| +interrog\.| +conj\.| +—predic\.| +—attrib\.| +—comb\.| +—interrog\.| +—conj\.| +\(| +gram\.| +mus\.| +—gram\.| +—mus\.| +[0-9]| +—[0-9]| +coarse| +—coarse).*

defEx = re.compile("(?<=slang|refix|oarse)|(?<=[0-9] |\) |\. |\; ).*(?= [0-9]| \[|$)", re.IGNORECASE)
splitEx = re.compile(" prefix| +n\.| +v\.| +pl\.| +adj\.| +abbr\.| +contr\.| +symb\.| +slang| +int\.| +poss\.| +pron\.| +adv\.| +naut\.| +colloq\.| +—n\.| +—v\.| +—pl\.| +—adj\.| +—[aA]bbr\.| +—contr\.| +—symb\.| +—slang| +—int\.| +—poss\.| +—pron\.| +—adv\.| +—naut\.| +—colloq\.| +—prep\.| +prep\.| +suffix| +archaic| +past part\.| +predic\.| +attrib\.| +comb\.| +interrog\.| +conj\.| +—predic\.| +—attrib\.| +—comb\.| +—interrog\.| +—conj\.| +gram\.| +mus\.| +—gram\.| +—mus\.| +[0-9]| +—[0-9]| +coarse| +—coarse|\[.*\]", re.IGNORECASE)

parenEx = re.compile("\(\W*(?:-ting|usu\.|prefix|n\.|v\.|pl\.|adj\.|abbr\.|contr\.|symb\.|slang|int\.|poss\.|pron\.|adv\.|naut\.|colloq\.|—n\.|—v\.|—pl\.|—adj\.|—[aA]bbr\.|—contr\.|—symb\.|—slang|—int\.|—poss\.|—pron\.|—adv\.|—naut\.|—colloq\.|—prep\.|prep\.|suffix|archaic|past part\.|predic\.|attrib\.|comb\.|interrog\.|conj\.|—predic\.|—attrib\.|—comb\.|—interrog\.|—conj\.|gram\.|mus\.|—gram\.|—mus\.|[0-9]|—[0-9]|coarse|—coarse|-*refl.|-*sing)[^\)]*\)", re.IGNORECASE)

#  [ABCDEFGHJKLMNOPQRSTUVWXYZ&] 
letterEx = re.compile(" [ABCDEFGHJKLMNOPQRSTUVWXYZ&] ")

explainEx = re.compile("(?:.*$|= \*.*$|\([^\)]*\))")

with open (outfile, "w") as outfile:
	with open ('clean.log', 'w') as logfile:
		for line in open(infile, 'rb'):
			line = line.strip()						# Isolate line
			if line == "":							# Ignore empty lines
				continue
			else:
				word = wordEx.search(line)
				if word and "  " not in word.group():
					definition = re.sub(wordEx, "", line, 1)#defEx.findall(line)
					#for defn in definitions:
					logfile.write("{}\n".format(word.group()))
					splits = re.split(splitEx, definition)
					for defn in splits:
						if defn and defn != "" and defn != " ":
							splits2 = re.split(parenEx, defn)
							for defn2 in splits2:
								if defn2 and defn2 != "" and defn2 != " ":
									splits3 = re.split(letterEx, defn2)
									for defn3 in splits3:
										if defn3 and defn3 != "" and defn3 != " " and defn3 != "&":
											splits4 = re.split(explainEx, defn3)

											# print '\n'
											# print defn3
											# print splits4

											for defn4 in splits4:
												if defn4 and len(defn4) > 3:
													logfile.write(":\t{}\n".format(defn4.strip()))
													outfile.write("{}\t{}\n".format(word.group(), defn4.strip()))
					else:
						logfile.write("\nBAD WORD: {}".format(line))

