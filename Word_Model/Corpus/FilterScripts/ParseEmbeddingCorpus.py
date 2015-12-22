#!/Applications/anaconda/bin/python

import sys

# TODO
# loop to accept multiple args

filepath = sys.argv[1]

with open (filepath, "r") as myfile:
    doc=myfile.read()



# from bs4 import BeautifulSoup

# soup = BeautifulSoup(doc, 'xml.parser')

# TODO
# For each of these

# print soup.find_all('text')[int(sys.argv[2])]