#!/usr/bin/env python3


import sys
import os
import pickle

All = {}
listOfMeaning = ["uid", "owner", "xloc", "yloc", "type", "effic", "mobil", "off", "tech", "opx", "opy", "mission",
                 "radius", "fleet", "civil", "milit", "shell", "gun", "petrol", "iron", "dust", "bar", "food", "oil",
                 "lcm", "hcm", "uw", "rad", "access", "name", "rflags", "rpath"]

if os.path.exists("ship_sectors.p"):
    fin = open("ship_sectors.p", "rb")
    sectors = pickle.load(fin)
    fin.close()
else:
    sectors = {}
# f = open("ship.random.txt", "r") #deleteafter

def dictAll(words):
    dictAll = {}
    listOfMeaning = ["uid", "owner", "xloc", "yloc", "type", "effic", "mobil", "off", "tech", "opx", "opy", "mission", "radius", "fleet", "civil", "milit", "shell", "gun", "petrol", "iron", "dust", "bar", "food", "oil", "lcm", "hcm", "uw", "rad", "access", "name", "rflags", "rpath"]
    for i in range(len(listOfMeaning)):
        dictAll[listOfMeaning[i]] = words[i]
    return dictAll

for line in sys.stdin.readlines():
    line = line.strip()
    words = line.split()
    if len(words) < 10:
        continue
    uid = int(words[0])
    key = uid

    # for i in range(len(listOfMeaning)):
    #     All[listOfMeaning[i]] = words[i]
    sectors[key] = dictAll(words)

# print()
# print()
# print()
# print(sectors)

fout = open("ship_sectors.p", "wb")
pickle.dump(sectors, fout)
fout.close()

# print("as far as you know this is parsed")
# /usr/citlocal/cs4300/bin/empire -s empire.cs.dixie.edu:2834
# xdump 1 * | ./parseShip.py