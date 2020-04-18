import os
import sys
import re



match = re.search(r'-?\d', "drone45-434")
if match:
    print(match.group())

match = re.findall(r'-?\d+', "drone45-43+4654-656lul7+8")
print(match)


uri = "frg%//grE1E3448"
print(uri[-1])