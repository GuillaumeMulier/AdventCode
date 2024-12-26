"""
Day 21 of 2024 advent of code
"""

import heapq
from functools import cache
import re
import math
import numpy as np

# Inputs

Test = True

if Test:
    Input = """029A
980A
179A
456A
379A"""
else:
    #with open("C:/Users/gmulier/Documents/GitHub/AdventCode/2024/Input/day21.txt") as String:
    with open("C:/Users/DRY12/Documents/GitHub/AdventCode/2024/Input/day21.txt") as String:
        Input = String.read().strip()

Input = Input.split("\n")

# Helpers

PaveNum = {
    "A": {"0": (1, "<"), "3": (1, "^")},
    "0": {"2": (1, "^"), "A": (1, ">")},
    "1": {"4": (1, "^"), "2": (1, ">")},
    "2": {"1": (1, "<"), "5": (1, "^"), "3": (1, ">"), "0": (1, "v")},
    "3": {"A": (1, "v"), "2": (1, "<"), "6": (1, "^")},
    "4": {"7": (1, "^"), "5": (1, ">"), "1": (1, "v")},
    "5": {"4": (1, "<"), "8": (1, "^"), "6": (1, ">"), "2": (1, "v")},
    "6": {"5": (1, "<"), "9": (1, "^"), "3": (1, "v")},
    "7": {"8": (1, ">"), "4": (1, "v")},
    "8": {"7": (1, "<"), "9": (1, ">"), "5": (1, "v")},
    "9": {"8": (1, "<"), "6": (1, "v")}
}

PaveDir = {
    "A": {"^": (1, "<"), ">": (1, "v")},
    "^": {"A": (1, ">"), "v": (1, "v")},
    "<": {"v": (1, ">")},
    "v": {"<": (1, "<"), "^": (1, "^"), ">": (1, ">")},
    ">": {"v": (1, "<"), "A": (1, "^")}
}

# Functions

def Dijkstra(Debut, Fin, AdjDict):
    TouchesEnCours = []
    heapq.heappush(TouchesEnCours, (0, Debut, ""))
    Distances = dict()
    CheminFini = []
    while (len(TouchesEnCours) > 0):
        Distance, Position, Chemin = heapq.heappop(TouchesEnCours)
        if Position == Fin:
            heapq.heappush(CheminFini, (Distance, Position, Chemin + "A"))
        else:
            for node, (dist, dir) in AdjDict[Position].items():
                if node in Distances:
                    if Distance + dist > Distances[node]: continue
                    Distances[node] = Distance + dist
                    heapq.heappush(TouchesEnCours, (Distance + dist, node, Chemin + dir))
                else:
                    Distances[node] = Distance + dist
                    heapq.heappush(TouchesEnCours, (Distance + dist, node, Chemin + dir))
    return CheminFini

"""@cache
def DijkstraCachedDir(Debut, Fin):
    TouchesEnCours = []
    heapq.heappush(TouchesEnCours, (0, Debut, ""))
    Distances = dict()
    CheminFini = []
    while (len(TouchesEnCours) > 0):
        Distance, Position, Chemin = heapq.heappop(TouchesEnCours)
        if Position == Fin:
            if len(Chemin) == 0:
                NumChgt = 0
            else:
                PremTouche = Chemin[0]
                NumChgt = 0
                for s in Chemin[1:]:
                    if s != PremTouche: NumChgt += 1
                    PremTouche = s
            heapq.heappush(CheminFini, (Distance, NumChgt, Position, Chemin + "A"))
        else:
            for node, (dist, dir) in PaveDir[Position].items():
                if node in Distances:
                    if Distance + dist > Distances[node]: continue
                    Distances[node] = Distance + dist
                    heapq.heappush(TouchesEnCours, (Distance + dist, node, Chemin + dir))
                else:
                    Distances[node] = Distance + dist
                    heapq.heappush(TouchesEnCours, (Distance + dist, node, Chemin + dir))
    return CheminFini[0]
"""
def PossiblePaths(Code):
    # Robot 1 instructions
    Debut1 = "A"
    PathEnCours1 = [(0, "")]
    for s in Code:
        Res = Dijkstra(Debut1, s, PaveNum)
        PathEnCours1 = [(p[0] + r[0], p[1] + r[2]) for p in PathEnCours1 for r in Res]
        Debut1 = s
    # Robot 2 instructions
    PathEnCours2 = []
    for dist1, path1 in PathEnCours1:
        Debut2 = "A"
        PathTemp2 = [(0, "")]
        for s in path1:
            Res = Dijkstra(Debut2, s, PaveDir)
            PathTemp2 = [(p[0] + r[0], p[1] + r[2]) for p in PathTemp2 for r in Res]
            Debut2 = s
        if len(PathEnCours2) == 0:
            PathEnCours2.extend(PathTemp2)
        elif PathEnCours2[0][0] > PathTemp2[0][0]:
            PathEnCours2 = PathTemp2
        elif PathEnCours2[0][0] == PathTemp2[0][0]:
            PathEnCours2.extend(PathTemp2)
        else:
            continue
    # Robot 3 instructions
    PathEnCours3 = []
    for dist2, path2 in PathEnCours2:
        Debut3 = "A"
        PathTemp3 = [(0, "")]
        for s in path2:
            Res = Dijkstra(Debut3, s, PaveDir)
            PathTemp3 = [(p[0] + r[0], p[1] + r[2]) for p in PathTemp3 for r in Res]
            Debut3 = s
        if len(PathEnCours3) == 0:
            PathEnCours3.extend(PathTemp3)
        elif PathEnCours3[0][0] > PathTemp3[0][0]:
            PathEnCours3 = PathTemp3
        elif PathEnCours3[0][0] == PathTemp3[0][0]:
            PathEnCours3.extend(PathTemp3)
        else:
            continue
    return PathEnCours3




def DirectionalPadInstruction(Instruction, NumRobot):
    Res = Robot(Instruction)
    if NumRobot == 1:
        return len(Res)
    else:
        SubPath = DirectionalPadInstruction(Res, NumRobot - 1)
        return SubPath


def PossiblePathsP2(Code, NumRobotSup):
    """
    Hint that we can cut the programm into instructions that ends at position A
    So recursive approach, trying to use functools.cache this time
    """
    # Robot 1 instructions
    Debut1 = "A"
    PathEnCours1 = [(0, "")]
    for s in Code:
        Res = Dijkstra(Debut1, s, PaveNum)
        PathEnCours1 = [(p[0] + r[0], p[1] + r[2]) for p in PathEnCours1 for r in Res]
        Debut1 = s
    # Other robots instructions
    Res = min([DirectionalPadInstruction(path[1], NumRobotSup) for path in PathEnCours1])
    return Res

def CalcCompl(ListeInstructions, Codes):
    Resultat = 0
    for i in range(len(ListeInstructions)):
        LengthShort = len(ListeInstructions[i][0][1])
        NumericPart = int(Codes[i][:-1])
        Resultat += LengthShort * NumericPart
    return Resultat



# Part 1

Res1 = []
for code in Input:
    Res1.append(PossiblePaths(code))
Complexity = CalcCompl(Res1, Input)
print("Solution part 1: " + str(Complexity))
"""
Res2 = 0
for code in Input:
    Res2 += PossiblePathsP2(code, 2) * int(code[:-1])
print("Solution part 1: " + str(Res2))
"""
# Part 2


"""
Res2 = 0
for code in Input:
    print("Code en cours : " + code)
    Res2 += PossiblePathsP2(code, 25) * int(code[:-1])
print("Solution part 2: " + str(Res2))

"""


# Precompute optimal paths for all combinations of directions
DictMoves = dict()
for i in PaveDir.keys():
    for j in PaveDir.keys():
        Res = Dijkstra(i, j, PaveDir)
        if len(Res) > 1:
            Longueurs = []
            for r in Res:
                LongueurInt = 0
                for k, l in zip("A" + r[2][:-1], r[2]):
                    ResInt = Dijkstra(k, l, PaveDir)
                    LongueurInt += len(ResInt[0][2])
                Longueurs.append(LongueurInt)
            Res = Res[np.argmin(Longueurs)]
        else:
            Res = Res[0]
        DictMoves[(i, j)] = Res[2]

def Robot(Instructions):
    PathRes = ""
    for s1, s2 in zip("A" + Instructions, Instructions):
        PathRes += DictMoves[(s1, s2)]
    return PathRes

@cache
def DirectionalPadInstruction(Instruction, NumRobot):
    Res = Robot(Instruction)
    if NumRobot == 1:
        return len(Res)
    else:
        SubPath = DirectionalPadInstruction(Res, NumRobot - 1)
        return SubPath

Res2 = []
for code in Input:
    Debut1 = "A"
    PathEnCours1 = [(0, "")]
    for s in code:
        Res = Dijkstra(Debut1, s, PaveNum)
        PathEnCours1 = [(p[0] + r[0], p[1] + r[2]) for p in PathEnCours1 for r in Res]
        Debut1 = s
    DirectionalPadInstruction(PathEnCours1[0][1], 20)
    Res2.append(PathEnCours1)


