"""
Script for day 16 of advent of code
"""
import copy
import numpy as np
import math
import heapq

Test = False

if (Test) :
    Input = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""
else:
    with open("C:/Users/gmulier/Documents/GitHub/AdventCode/2024/Input/day16.txt") as String:
        Input = String.read().strip()

Carte = [[ligne[i] for i in range(len(ligne))] for ligne in Input.split("\n")]
Carte = np.array(Carte)
NROWS, NCOLS = Carte.shape

def MovePossible(Carte, row, col):
    if Carte[row, col] == "#":
        return False
    else:
        return True

def EndPath(Carte, row, col):
    if Carte[row, col] == "E":
        return True
    else:
        return False

def NexPossibleMoves(orientation, rr, cc):
    if orientation == ">":
        return [[rr - 1, cc], [rr, cc + 1], [rr + 1, cc]]
    elif orientation == "v":
        return [[rr, cc + 1], [rr + 1, cc], [rr, cc - 1]]
    elif orientation == "<":
        return [[rr + 1, cc], [rr, cc - 1], [rr - 1, cc]]
    elif orientation == "^":
        return [[rr, cc - 1], [rr - 1, cc], [rr, cc + 1]]

def Turn(Row, Col, RRow, CCol):
    if (Row + 1) == RRow and Col == CCol:
        return "v"
    elif (Row - 1) == RRow and Col == CCol:
        return "^"
    elif Row == RRow and (Col + 1) == CCol:
        return ">"
    elif Row == RRow and (Col - 1) == CCol:
        return "<"
    else:
        return "."

def CostOrient(DirBase, DirArr):
    if DirBase in [">", "<"]:
        if DirArr in ["^", "v"]:
            return 1001
        else:
            return 1
    if DirBase in ["v", "^"]:
        if DirArr in [">", "<"]:
            return 1001
        else:
            return 1

PosRenne = np.where(Carte == "S")
PosFin = np.where(Carte == "E")

ListeRennes = []
heapq.heappush(ListeRennes, (0, [(PosRenne[0][0], PosRenne[1][0])], ">"))

RennesArrives = []

CarteCouts = np.array([[math.inf for i in range(NCOLS)] for j in range(NROWS)])

# Trying to code for first time an A* like algorithm
while len(ListeRennes) > 0:
    # Get the reindeer with lowest cost
    RenneEnCours = heapq.heappop(ListeRennes)
    MvtsPossibles = NexPossibleMoves(RenneEnCours[2], RenneEnCours[1][0][0], RenneEnCours[1][0][1])
    for rr, cc in MvtsPossibles:
        DirArrivee = Turn(RenneEnCours[1][0][0], RenneEnCours[1][0][1], rr, cc)
        CoutUpdated = RenneEnCours[0] + CostOrient(RenneEnCours[2], DirArrivee)
        Chemin = [(rr, cc)]
        Chemin.append(RenneEnCours[1])
        # Is the reindeer arrived ?
        if EndPath(Carte, rr, cc):
            heapq.heappush(RennesArrives, (CoutUpdated, Chemin))
        # Is it a possible move ?
        elif MovePossible(Carte, rr, cc):
            # Is the next cost better than another cost of the queue ?
            if CoutUpdated <= CarteCouts[rr, cc]:
                CarteCouts[rr, cc] = CoutUpdated
                heapq.heappush(ListeRennes, (CoutUpdated, Chemin, DirArrivee))

# Fails and find 12 too much...
print("Solution of part 1 with A* like: " + str(RennesArrives[0][0]))

# Try dijkstra algorithm
Arrivee = (PosFin[0][0], PosFin[1][0])
DirIni = 0
Directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
def Voisins(Position, Direction):
    TtDroit = (1, tuple(np.add(Position, Directions[Direction])), Direction)
    TournerGche = (1001, tuple(np.add(Position, Directions[(Direction - 1) % 4])), (Direction - 1) % 4)
    TournerDte = (1001, tuple(np.add(Position, Directions[(Direction + 1) % 4])), (Direction + 1) % 4)
    return [TtDroit, TournerGche, TournerDte]
Distances = dict()

ListeRennes = []
heapq.heappush(ListeRennes, (0, (PosRenne[0][0], PosRenne[1][0]), 0, [(PosRenne[0][0], PosRenne[1][0])]))
RennesArrives = []

while (len(ListeRennes) > 0):
    Distance, Position, Direction, Chemin = heapq.heappop(ListeRennes)
    if Position == Arrivee:
        heapq.heappush(RennesArrives, (Distance, Position, Direction, Chemin))
    else:
        VoisinsExam = Voisins(Position, Direction)
        for cout, pos, dir in VoisinsExam:
            if Carte[pos] != "#":
                if (pos, dir) not in Distances:
                    chem = copy.deepcopy(Chemin)
                    chem.append(pos)
                    Distances[(pos, dir)] = Distance + cout
                    heapq.heappush(ListeRennes, (Distance + cout, pos, dir, chem))
                elif (Distance + cout) <= Distances[(pos, dir)]:
                    chem = copy.deepcopy(Chemin)
                    chem.append(pos)
                    Distances[(pos, dir)] = Distance + cout
                    heapq.heappush(ListeRennes, (Distance + cout, pos, dir, chem))

print("Solution of part 1 with Dijkstra: " + str(RennesArrives[0][0])) # Works !

CoutOptimal = RennesArrives[0][0]
CheminsOpt = []
EnCours = True
while EnCours and len(RennesArrives) > 0:
    Renne = heapq.heappop(RennesArrives)
    if Renne[0] == CoutOptimal:
        CheminsOpt += Renne[3]
    else:
        EnCours = False

print("Solution of part 2 with Dijkstra: " + str(len(set(CheminsOpt))))