"""
Day 23 of 2024 advent of code
"""

import copy
import re

# Inputs

Test = False

if Test:
    Input = """ka-co
ta-co
de-co
ta-ka
de-ta
ka-de"""
else:
    with open("C:/Users/DRY12/Documents/GitHub/AdventCode/2024/Input/day23.txt") as String:
        Input = String.read().strip()

Input = Input.split("\n")
Input = [tuple(i.split("-")) for i in Input]

# Functions

def CreateGraph(ListEdges):
    Graphe = dict()
    for i, j in ListEdges:
        if i not in Graphe:
            Graphe[i] = set()
        if j not in Graphe:
            Graphe[j] = set()
        Graphe[i].add(j)
        Graphe[j].add(i)
    return Graphe

def FindClique3(Graph):
    SubGraphs = []
    for node in Graph:
        for node2 in Graph[node]:
            Intersection = list(Graph[node] & Graph[node2])
            if len(Intersection) > 0:
                for node3 in Intersection:
                    Set = [node, node2, node3]
                    Set.sort()
                    Set = ",".join(Set)
                    if Set not in SubGraphs:
                        SubGraphs.append(Set)
    return SubGraphs

Cliques = set()
def FindAllCliques(Node, MaxClique):
    Sequence = tuple(sorted(MaxClique))
    if Sequence in Cliques:
        return None # Already found that clique
    Cliques.add(Sequence)
    for node in GrapheConnexions[Node]:
        if node in MaxClique: continue
        if not MaxClique <= GrapheConnexions[node]: continue # Maxclique is in the neighbours of node so node can be added
        FindAllCliques(node, {*MaxClique, node})


# Part 1

GrapheConnexions = CreateGraph(Input)
ListCliques3 = FindClique3(GrapheConnexions)
Res = sum([not re.search(r"^t|,t", s) is None for s in ListCliques3])

print("Solution part 1: " + str(Res))

# Part 2

for noderes in GrapheConnexions:
    FindAllCliques(noderes, {noderes})
Optimal = 0
OptimalSet = []
for sequence in Cliques:
    if len(sequence) > Optimal:
        Optimal = len(sequence)
        OptimalSet = [sequence]
    elif len(sequence) == Optimal:
        OptimalSet.append(sequence)
    else:
        continue

print("Solution part 2: " + ",".join(list(OptimalSet[0])))

# Using networkx

import networkx

NetworkLAN = networkx.Graph()
NetworkLAN.add_edges_from(Input)
ListeAllCliques = list(networkx.enumerate_all_cliques(NetworkLAN))
Clique3 = [",".join(clique) if len(clique) == 3 else "" for clique in ListeAllCliques]
print("Solution part 1: " + str(sum([not re.search(r"^t|,t", s) is None for s in Clique3])))
print("Solution part 2: " + ",".join(sorted(max(ListeAllCliques, key=len))))
