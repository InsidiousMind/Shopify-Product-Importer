#!/usr/bin/python3

import re

line = "Cats are smarter than Humans"

matchObj = re.match(r"(.*) are (.*?) .*", line, re.M|re.I)

if matchObj:
    print ("Everything : ", matchObj.group())
    print (" Group 1 ", matchObj.group(1))
    print ("Group 2 ", matchObj.group(2))


search = re.search(r"(.*) are (.*?) .*", line, re.M|re.I)

print("search", search.group())
