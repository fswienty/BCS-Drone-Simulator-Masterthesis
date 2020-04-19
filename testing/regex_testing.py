import os
import sys
import re
import random



match = re.search(r'-?\d', "drone45-434")
if match:
    print(match.group())

match = re.findall(r'-?\d+', "drone45-43+4654-656lul7+8")
print(match)


uri = "frg%//grE1E3448"
for i in range(0, 10):
    print(random.uniform(0, 1))