"""
Day 19 advent of code 2024
"""

import re
import numpy as np
import functools

# Inputs

Test = False

if Test:
    Input = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""
else:
    with open("C:/Users/gmulier/Documents/GitHub/AdventCode/2024/Input/day19.txt") as String:
        Input = String.read().strip()

Towels, Designs = Input.split("\n\n")
Towels = Towels.split(", ")
Designs = Designs.split("\n")

# Functions

# Not working for some reason I don't understand why...
# EDIT: you have to not put the array of towels in its arguments to make it work
"""@functools.cache
def NbDesignPossible(Design):
    Nb = 0
    for pattern in ListTowels:
        Finding = re.search(r"^" + pattern, Design)
        if Finding != None:
           NouveauDesign = re.sub(r"^" + pattern, r"", Design)
           if NouveauDesign == "":
               Nb += 1
           else:
               NbPossibleNext = NbDesignPossible(NouveauDesign)
               Nb += NbPossibleNext
    return Nb"""

Cache = dict()
def NbDesignPossible(Design, ListTowels):
    if Design in Cache:
        return Cache[Design]
    else:
        Nb = 0
        for pattern in ListTowels:
            Finding = re.search(r"^" + pattern, Design)
            if Finding != None:
                NouveauDesign = re.sub(r"^" + pattern, r"", Design)
                if NouveauDesign == "":
                    Nb += 1
                else:
                    NbPossibleNext = NbDesignPossible(NouveauDesign, ListTowels)
                    Nb += NbPossibleNext
            Cache[Design] = Nb
        return Nb



# Part 1

Possibilites = [NbDesignPossible(d, Towels) for d in Designs]
Possibilites = np.array(Possibilites)

print("Solution part 1: " + str(sum(np.greater(Possibilites, 0))))

# Part 2

print("Solution part 2: " + str(sum(Possibilites)))
