"""
Day 20 of 2024 advent of code
"""

import numpy as np

# Inputs

Test = False

if Test:
    Input = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""
else:
    with open("C:/Users/gmulier/Documents/GitHub/AdventCode/2024/Input/day20.txt") as String:
        Input = String.read().strip()
Input = np.array([[s[i] for i in range(len(s))] for s in Input.split("\n")])

# Functions

def Voisins(rr, cc, NRows, NCols):
    Directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    Temp = [tuple(np.add((rr, cc), x)) for x in Directions]
    Res = []
    for x in Temp:
        if x[0] >= 0 and x[0] < NRows and x[1] >= 0 and x[1] < NCols:
            Res.append(x)
    return Res

def DictPos(Carte):
    NRows, NCols = Carte.shape
    Depart = np.where(Carte == "S")
    RDep = Depart[0][0]
    CDep = Depart[1][0]
    Positions = dict()
    PosEnCours = (RDep, CDep)
    Dist = 0
    Positions[PosEnCours] = Dist
    while Carte[PosEnCours] != "E":
        VoisinsPos = Voisins(PosEnCours[0], PosEnCours[1], NRows, NCols)
        Dist += 1
        for rr, cc in VoisinsPos:
            if Carte[rr, cc] != "#":
                if (rr, cc) in Positions:
                    continue
                else:
                    Positions[(rr, cc)] = Dist
                    PosEnCours = (rr, cc)
    return Positions

def CheatOnce(Carte, DictPositions):
    DictCheat = dict()
    NRows, NCols = Carte.shape
    for i, (pos, value) in enumerate(DictPositions.items()):
        Voisins1 = Voisins(pos[0], pos[1], NRows, NCols)
        for pos1 in Voisins1:
            Voisins2 = Voisins(pos1[0], pos1[1], NRows, NCols)
            for pos2 in Voisins2:
                if Carte[pos2] != "#":
                    Gain = DictPositions[pos2] - value - 2
                    if Gain > 0:
                        if Gain in DictCheat:
                            DictCheat[Gain] += 1
                        else:
                            DictCheat[Gain] = 1
    return DictCheat

def CheatMaxTime(Carte, DictPositions, MaxTime):
    DictCheats = dict()
    for i in range(DictPositions[max(DictPositions, key=DictPositions.get)] + 1):
        DictCheats[i] = 0
    NRows, NCols = Carte.shape
    for i, (pos, value) in enumerate(DictPositions.items()):
        if i % 100 == 0: print("Position " + str(i) + "/" + str(len(DictPositions)) + ": " + str(round(100 * i / len(DictPositions))) + "%!")
        ArrayDist = np.array([[abs(r - pos[0]) + abs(c - pos[1]) for c in range(NCols)] for r in range(NRows)])
        for i in range(1, MaxTime + 1):
            PosExplo = np.where(ArrayDist == i)
            if len(PosExplo[0]) == 0:
                break
            else:
                for j in range(len(PosExplo[0])):
                    rr = PosExplo[0][j]
                    cc = PosExplo[1][j]
                    if Carte[rr, cc] != "#":
                        Gain = DictPositions[(rr, cc)] - value - i
                        if Gain > 0:
                            DictCheats[Gain] += 1
    return DictCheats

# Part 1

DictTemps = DictPos(Input)
DictCheats = CheatOnce(Input, DictTemps)
Res = 0
for i, (gain, nb) in enumerate(DictCheats.items()):
    if gain >= 100: Res += nb
print("Solution part 1: " + str(Res))

# Part 2

DictCheatsP2 = CheatMaxTime(Input, DictTemps, 20)
Res = 0
for i, (gain, nb) in enumerate(DictCheatsP2.items()):
    if gain >= 100: Res += nb
print("Solution part 2: " + str(Res))

