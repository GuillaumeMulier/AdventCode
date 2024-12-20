"""
Day 18 advent of code 2024
"""

import numpy as np
import heapq
import copy

# Function

def PrintMap(Carte):
    NRows, NCols = Carte.shape
    Temp1 = ["".join(Carte[i, ]) for i in range(NRows)]
    Map = "\n".join(Temp1)
    print(Map)
    return None

def FallingBytes(NRows, NCols, ListeBytes, NumBytes):
    Carte = np.array([["_" for i in range(NCols)] for j in range(NRows)])
    for b in ListeBytes[:NumBytes]:
        Carte[b] = "#"
    return Carte

def Voisins(rr, cc, NRows, NCols):
    Directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    Temp = [tuple(np.add((rr, cc), x)) for x in Directions]
    Res = []
    for x in Temp:
        if x[0] >= 0 and x[0] < NRows and x[1] >= 0 and x[1] < NCols:
            Res.append(x)
    return Res

def PrintPossible(Possible, N, NCorr):
    if Possible:
        return "Possible path with " + str(NCorr) + " corrupted bytes in " + str(N) + " moves!"
    else:
        return "Impossible path with " + str(NCorr) + " corrupted bytes!"

def Dijkstra(MemoryMap, RDep, CDep, REnd, CEnd):
    Possible = False
    NbMoves = -99
    ListeBytesEnCours = []
    heapq.heappush(ListeBytesEnCours, (0, (RDep, CDep), []))
    Distances = dict()
    while (len(ListeBytesEnCours) > 0):
        Distance, Position, Chemin = heapq.heappop(ListeBytesEnCours)
        if Position == (REnd, CEnd):
            Possible = True
            NbMoves = Distance
            break
        else:
            VoisinsExam = Voisins(Position[0], Position[1], NROWS, NCOLS)
            for rr, cc in VoisinsExam:
                if MemoryMap[rr, cc] != "#":
                    if (rr, cc) not in Distances:
                        chem = copy.deepcopy(Chemin)
                        chem.append((rr, cc))
                        Distances[(rr, cc)] = Distance + 1
                        heapq.heappush(ListeBytesEnCours, (Distance + 1, (rr, cc), chem))
                    elif (Distance + 1) < Distances[(rr, cc)]:
                        chem = copy.deepcopy(Chemin)
                        chem.append((rr, cc))
                        Distances[(rr, cc)] = Distance + 1
                        heapq.heappush(ListeBytesEnCours, (Distance + 1, (rr, cc), chem))
    return (Possible, NbMoves)

# Import inputs

Test = False

if Test:
    Input = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""
    NROWS = 7
    NCOLS = 7
else:
    with open("C:/Users/gmulier/Documents/GitHub/AdventCode/2024/Input/day18.txt") as String:
        Input = String.read().strip()
    NROWS = 71
    NCOLS = 71

Coordonnees = list(map(lambda x: (int(x.split(",")[1]), int(x.split(",")[0])), Input.split("\n")))
CDep, RDep = 0, 0
CEnd, REnd = NCOLS - 1, NROWS - 1

# Part 1

if Test:
    MemoryMap = FallingBytes(NROWS, NCOLS, Coordonnees, 12)
else:
    MemoryMap = FallingBytes(NROWS, NCOLS, Coordonnees, 1024)

PrintMap(MemoryMap)

ListeBytesEnCours = []
heapq.heappush(ListeBytesEnCours, (0, (RDep, CDep), []))
Distances = dict()
CheminsPossibles = []

while (len(ListeBytesEnCours) > 0):
    Distance, Position, Chemin = heapq.heappop(ListeBytesEnCours)
    if Position == (REnd, CEnd):
        heapq.heappush(CheminsPossibles, (Distance, Position, Chemin))
        break
    else:
        VoisinsExam = Voisins(Position[0], Position[1], NROWS, NCOLS)
        for rr, cc in VoisinsExam:
            if MemoryMap[rr, cc] != "#":
                if (rr, cc) not in Distances:
                    chem = copy.deepcopy(Chemin)
                    chem.append((rr, cc))
                    Distances[(rr, cc)] = Distance + 1
                    heapq.heappush(ListeBytesEnCours, (Distance + 1, (rr, cc), chem))
                elif (Distance + 1) < Distances[(rr, cc)]:
                    chem = copy.deepcopy(Chemin)
                    chem.append((rr, cc))
                    Distances[(rr, cc)] = Distance + 1
                    heapq.heappush(ListeBytesEnCours, (Distance + 1, (rr, cc), chem))

"""MapChemin = copy.deepcopy(MemoryMap)
for rr, cc in CheminsPossibles[0][2]:
    MapChemin[rr, cc] = "O"
PrintMap(MapChemin)"""

print("Solution part 1: " + str(CheminsPossibles[0][0]))

# Part 2

"""
# Brute force solution that is really slow
for NbBytes in range(len(Coordonnees)):
    Possible = False
    MemoryMap = FallingBytes(NROWS, NCOLS, Coordonnees, NbBytes)
    ListeBytesEnCours = []
    heapq.heappush(ListeBytesEnCours, (0, (RDep, CDep), []))
    Distances = dict()
    while (len(ListeBytesEnCours) > 0):
        Distance, Position, Chemin = heapq.heappop(ListeBytesEnCours)
        if Position == (REnd, CEnd):
            print("For " + str(NbBytes) + " corrupted bytes, a path is possible in " + str(Distance) + " moves!")
            Possible = True
            break
        else:
            VoisinsExam = Voisins(Position[0], Position[1], NROWS, NCOLS)
            for rr, cc in VoisinsExam:
                if MemoryMap[rr, cc] != "#":
                    if (rr, cc) not in Distances:
                        chem = copy.deepcopy(Chemin)
                        chem.append((rr, cc))
                        Distances[(rr, cc)] = Distance + 1
                        heapq.heappush(ListeBytesEnCours, (Distance + 1, (rr, cc), chem))
                    elif (Distance + 1) < Distances[(rr, cc)]:
                        chem = copy.deepcopy(Chemin)
                        chem.append((rr, cc))
                        Distances[(rr, cc)] = Distance + 1
                        heapq.heappush(ListeBytesEnCours, (Distance + 1, (rr, cc), chem))
    if not Possible: break

print("Solution part 2: " + str(NbBytes) + " bytes with first byte making path impossible " + str(Coordonnees[NbBytes - 1][::-1]))
"""

# Binary search

NbG = 0
MemoryMap = FallingBytes(NROWS, NCOLS, Coordonnees, NbG)
ChemPossG, NbMovesG = Dijkstra(MemoryMap, RDep, CDep, REnd, CEnd)
print(PrintPossible(ChemPossG, NbMovesG, NbG))

NbD = len(Coordonnees)
MemoryMap = FallingBytes(NROWS, NCOLS, Coordonnees, NbD)
ChemPossD, NbMovesD = Dijkstra(MemoryMap, RDep, CDep, REnd, CEnd)
print(PrintPossible(ChemPossD, NbMovesD, NbD))

while NbG < NbD:
    NbMid = (NbD + NbG) // 2
    MemoryMap = FallingBytes(NROWS, NCOLS, Coordonnees, NbMid)
    ChemPossMid, NbMovesMid = Dijkstra(MemoryMap, RDep, CDep, REnd, CEnd)
    print(PrintPossible(ChemPossMid, NbMovesMid, NbMid))
    if ChemPossMid:
        # Possible path on the left so the searched impossible path is on the right
        NbG = NbMid + 1
    else:
        NbD = NbMid
print("Solution part 2: impossible path after " + str(NbG) + " corrupted bytes with corresponding critical byte " + str(Coordonnees[NbG - 1][::-1]))
