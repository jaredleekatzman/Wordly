#!/Applications/anaconda/bin/python

import sys

# TODO
# loop to accept multiple args

filepath = sys.argv[1]

with open (filepath, "r") as myfile:
    doc=myfile.read()


