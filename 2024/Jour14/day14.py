"""
Script for day 14 of advent of code
"""

import re
import matplotlib.pyplot as plt
import numpy as np
Test = False

if (Test) :
    Input = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
    NROWS = 7
    NCOLS = 11
else:
    with open("C:/Users/gmulier/Documents/GitHub/AdventCode/2024/Input/day14.txt") as String:
        Input = String.read()
    NROWS = 103
    NCOLS = 101


def ExtractData(Robot):
    Regex = r"^p=([0-9]+),([0-9]+) v=([\-0-9]+),([\-0-9]+)$"
    Px = int(re.sub(Regex, r"\1", Robot))
    Py = int(re.sub(Regex, r"\2", Robot))
    Vx = int(re.sub(Regex, r"\3", Robot))
    Vy = int(re.sub(Regex, r"\4", Robot))
    return [(Py, Px), [Vy, Vx]]

def AfficherCarte(ListeRobots, NRows, NCols):
    Carte = [[0 for i in range(NCols)] for j in range(NRows)]
    for Robot in ListeRobots:
        Carte[Robot[0][0]][Robot[0][1]] += 1
    return Carte

def DeplacerRobot(Px, Py, Dx, Dy, Nr, Nc):
    Px = Px + Dx
    if Px < 0:
        Px += Nc
    elif Px >= Nc:
        Px -= Nc
    Py = Py + Dy
    if Py < 0:
        Py += Nr
    elif Py >= Nr:
        Py -= Nr
    return (Py, Px)

def SimuRobots(ListeRobots, NSec, Nr, Nc):
    for i in range(len(ListeRobots)):
        for sec in range(NSec):
            ListeRobots[i][0] = DeplacerRobot(ListeRobots[i][0][1], ListeRobots[i][0][0],
                          ListeRobots[i][1][1], ListeRobots[i][1][0],
                          Nr, Nc)
    return ListeRobots

def SafeFactor(ListeRobots, Nr, Nc):
    MidRow = Nr // 2
    MidCol = Nc // 2
    Carte = AfficherCarte(ListeRobots, Nr, Nc)
    Quad1 = sum([Carte[i][j] for i in range(MidRow) for j in range(MidCol)])
    Quad2 = sum([Carte[i][j] for i in range(MidRow + 1, Nr) for j in range(MidCol)])
    Quad3 = sum([Carte[i][j] for i in range(MidRow) for j in range(MidCol + 1, Nc)])
    Quad4 = sum([Carte[i][j] for i in range(MidRow + 1, Nr) for j in range(MidCol + 1, Nc)])
    return Quad1 * Quad2 * Quad3 * Quad4

def NumLoca(Carte, Nr, Nc):
    Nb = 0
    for i in range(Nr):
        for j in range(Nc):
            if Carte[i][j] != 0:
                Nb += 1
    return Nb

# Part 1

ListeRobots = [ExtractData(Robot) for Robot in Input.strip().split("\n")]
ListeRobots = SimuRobots(ListeRobots, 100, NROWS, NCOLS)
print("Résultat part 1 : " + str(SafeFactor(ListeRobots, NROWS, NCOLS)))

# Part 2

ListeRobots = [ExtractData(Robot) for Robot in Input.strip().split("\n")]
NbRobots = len(ListeRobots)

# Configuration initiale
Carte = AfficherCarte(ListeRobots, NROWS, NCOLS)
if NumLoca(Carte, NROWS, NCOLS) == NbRobots:
    ArrayRob = np.array(Carte)
    plt.imshow(ArrayRob, interpolation="nearest", origin="upper")
    cb = plt.colorbar()
    cb.remove()
    plt.savefig("C:/Users/gmulier/Documents/GitHub/AdventCode/2024/Jour14/sec0.png")

for s in range(10000):
    if s % 100 == 0:
        print(f"Simulation n°{s} / 10000 ({100 * s / 10000}%)")
    ListeRobots = SimuRobots(ListeRobots, 1, NROWS, NCOLS)
    Carte = AfficherCarte(ListeRobots, NROWS, NCOLS)
    if NumLoca(Carte, NROWS, NCOLS) == NbRobots:
        ArrayRob = np.array(Carte)
        plt.imshow(ArrayRob, interpolation="nearest", origin="upper")
        cb = plt.colorbar()
        cb.remove()
        plt.savefig("C:/Users/gmulier/Documents/GitHub/AdventCode/2024/Jour14/sec" + str(s + 1) + ".png")

