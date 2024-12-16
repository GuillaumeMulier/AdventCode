"""
Script for day 15 of advent of code
"""

import numpy as np
import re

Test = False

if (Test) :
    Input = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""
else:
    with open("C:/Users/gmulier/Documents/GitHub/AdventCode/2024/Input/day15.txt") as String:
        Input = String.read().strip()

Carte, Instructions = Input.split("\n\n")
Carte = Carte.split("\n")
Carte = [[ligne[i] for i in range(len(ligne))] for ligne in Carte]
Carte = np.array(Carte)

Robot = np.where(Carte == "@")
RobotR = Robot[0][0]
RobotC = Robot[1][0]

def MoveRobot(CurrentR, CurrentC, Direction, NbMoves):
    if Direction == "<":
        CurrentC -= NbMoves
    elif Direction == ">":
        CurrentC += NbMoves
    elif Direction == "v":
        CurrentR += NbMoves
    elif Direction == "^":
        CurrentR -= NbMoves
    else:
        print("Error, unrecognized direction : " + Direction)
    return [CurrentR, CurrentC]

def CompteBoites(Carte, RobotR, RobotC, Direction):
    EnCours = True
    Possible = 1
    NBoxes = 0
    CurrentR = RobotR
    CurrentC = RobotC
    while EnCours:
        # New coordinates of Robot
        CurrentR, CurrentC = MoveRobot(CurrentR, CurrentC, Direction, 1)
        # Count the boxes to move
        if Carte[CurrentR, CurrentC] == "O":
            NBoxes += 1
        else:
            if Carte[CurrentR, CurrentC] == "#":
                Possible = 0
            EnCours = False
    return [NBoxes, Possible]

def BoxesToMove(RobotR, RobotC, ListeBoites, ListeMurs, Direction):
    EnCours = True
    NBoxes = []
    Stack = [(RobotR, RobotC)]
    while EnCours:
        CoordsToCheck = [tuple(MoveRobot(coords[0], coords[1], Direction, 1)) for coords in Stack]
        Stack = []
        Possible = int(1 - (sum([x in ListeMurs for x in CoordsToCheck]) > 0))
        if Possible == 0:
            EnCours = False
        else:
            BoolBoites = [sum([x in y for x in CoordsToCheck]) > 0 for y in ListeBoites]
            if sum(BoolBoites) == 0:
                EnCours = False
            else:
                for x in np.where(BoolBoites)[0]:
                    NBoxes.append(x)
                    if Direction == ">":
                        Stack.append(ListeBoites[x][1])
                    elif Direction == "<":
                        Stack.append(ListeBoites[x][0])
                    else:
                        Stack.append(ListeBoites[x][1])
                        Stack.append(ListeBoites[x][0])
    return [NBoxes, Possible]

def AfficherCarte(Carte, ListeBoites, ListeMurs, Robot):
    NRows = len(Carte)
    NCols = len(Carte[0])
    Affichage = ""
    BoitesG = [x[0] for x in ListeBoites]
    BoitesD = [x[1] for x in ListeBoites]
    for i in range(NRows):
        for j in range(NCols):
            if (i, j) in ListeMurs:
                Affichage = Affichage + "#"
            elif (i, j) in BoitesG:
                Affichage = Affichage + "["
            elif (i, j) in BoitesD:
                Affichage = Affichage + "]"
            elif (i, j) == Robot:
                Affichage = Affichage + "@"
            else:
                Affichage = Affichage + "."
        Affichage = Affichage + "\n"
    return(Affichage)

# Part 1

for i in Instructions:
    NbBoites, Possibilite = CompteBoites(Carte, RobotR, RobotC, i)
    if Possibilite == 1:
        print("Direction " + i + " : Robot moving !")
        if NbBoites == 0:
            rr, cc = MoveRobot(RobotR, RobotC, i, 1)
            Carte[rr, cc] = "@"
            Carte[RobotR, RobotC] = "."
            RobotR, RobotC = rr, cc
        else:
            for b in range(NbBoites + 1, 1, -1):
                rr, cc = MoveRobot(RobotR, RobotC, i, b)
                Carte[rr, cc] = "O"
            rr, cc = MoveRobot(RobotR, RobotC, i, 1)
            Carte[rr, cc] = "@"
            Carte[RobotR, RobotC] = "."
            RobotR, RobotC = rr, cc
    else:
        print("Direction " + i + " : Robot unable to move !")
    #print(Carte)

Lignes, Colonnes = np.where(Carte == "O")
print("Result part 1: " + str(sum(Lignes * 100 + Colonnes)))
print("\n\n-----------------\n\n")

# Part 2

Input = re.sub(r"#", r"##", Input)
Input = re.sub(r"O", r"[]", Input)
Input = re.sub(r"\.", r"..", Input)
Input = re.sub(r"@", r"@.", Input)
Carte, Instructions = Input.split("\n\n")
Carte = Carte.split("\n")
Carte = [[ligne[i] for i in range(len(ligne))] for ligne in Carte]
Carte = np.array(Carte)

Boites = np.where(Carte == "[")
ListeBoites = [[(Boites[0][i], Boites[1][i]), (Boites[0][i], Boites[1][i] + 1)] for i in range(len(Boites[0]))]
Murs = np.where(Carte == "#")
ListeMurs = [(Murs[0][i], Murs[1][i]) for i in range(len(Murs[0]))]

Robot = np.where(Carte == "@")
RobotR = Robot[0][0]
RobotC = Robot[1][0]

for i in Instructions:
    BoitesToMove, Possibilite = BoxesToMove(RobotR, RobotC, ListeBoites, ListeMurs, i)
    if Possibilite == 1:
        print("Direction " + i + " : Robot moving !")
        if len(BoitesToMove) == 0:
            rr, cc = MoveRobot(RobotR, RobotC, i, 1)
            Carte[rr, cc] = "@"
            Carte[RobotR, RobotC] = "."
            RobotR, RobotC = rr, cc
        else:
            for b in range(len(BoitesToMove)):
                BoiteToMove = ListeBoites[BoitesToMove[b]]
                rr, cc = MoveRobot(BoiteToMove[0][0], BoiteToMove[0][1], i, 1)
                ListeBoites[BoitesToMove[b]][0] = (rr, cc)
                rr, cc = MoveRobot(BoiteToMove[1][0], BoiteToMove[1][1], i, 1)
                ListeBoites[BoitesToMove[b]][1] = (rr, cc)
            rr, cc = MoveRobot(RobotR, RobotC, i, 1)
            RobotR, RobotC = rr, cc
    else:
        print("Direction " + i + " : Robot unable to move !")
print(AfficherCarte(Carte, ListeBoites, ListeMurs, (RobotR, RobotC)))

print("Result part 2: " + str(sum([Boite[0][0] * 100 + Boite[0][1] for Boite in ListeBoites])))
print("\n\n-----------------\n\n")




