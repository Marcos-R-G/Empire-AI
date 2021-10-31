#!/usr/bin/env python3


import sys
import os
import pickle

All = {}


if os.path.exists("sectors.p"):
    fin = open("sectors.p", "rb")
    sectors = pickle.load(fin)
    fin.close()
else:
    sectors = {}
# f = open("random.txt", "r") #deleteafter

def dictAll(words):
    dictAll = {}
    listOfMeaning = ["owner","xloc","yloc","des", "effic", "mobil", "off", "terr0", "terr1", "terr2", "terr3", "xdist", "ydist", "avail", "work", "coastal", "newdes", "min", "gold", "fert", "ocontent", "uran", "oldown", "civil", "milit", "shell", "gun", "petrol", "iron", "dust", "bar", "food", "oil", "lcm", "hcm", "uw", "rad", "c_dist", "m_dist", "s_dist", "g_dist", "p_dist", "i_dist", "d_dist", "b_dist", "f_dist", "o_dist", "l_dist", "h_dist", "u_dist", "r_dist", "c_del", "m_del", "s_del", "g_del", "p_del", "i_del", "d_del", "b_del", "f_del", "o_del", "l_del", "h_del", "u_del", "r_del", "fallout", "access", "road", "rail", "dfense"]
    for i in range(len(listOfMeaning)):
        dictAll[listOfMeaning[i]] = words[i]
    return dictAll


for line in sys.stdin.readlines():
    line = line.strip()
    words = line.split()
    if len(words) < 10:
        continue
    x = int(words[1])
    y = int(words[2])
    key = (x, y)

    # for i in range(len(listOfMeaning)):
    #     All[listOfMeaning[i]] = words[i]
    sectors[key] = dictAll(words)

# print()
# print()
# print()
# print(sectors)

fout = open("sectors.p", "wb")
pickle.dump(sectors, fout)
fout.close()

# print("as far as you know this is parsed")