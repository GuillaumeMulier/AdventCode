"""
Day 22 of 2024 advent of code
"""

from functools import cache

Test = False

if Test:
    Input = """1
2
3
2024"""
else:
    with open("C:/Users/DRY12/Documents/GitHub/AdventCode/2024/Input/day22.txt") as String:
        Input = String.read().strip()

Input = Input.split("\n")

# Functions

def Mix(Value, Secret):
    return Value ^ Secret

def Prune(Secret):
    return Secret % 16777216

def Evolve1(Donnees):
    Number, NumSeq = Donnees
    if NumSeq == 0:
        Res = Number * 64
    elif NumSeq == 1:
        Res = Number // 32
    else:
        Res = Number * 2048
    Res = Mix(Number, Res)
    Res = Prune(Res)
    NumSeq = (NumSeq + 1) % 3
    return (Res, NumSeq)

@cache
def Evolve(Number):
    Donnees = (Number, 0)
    Donnees = Evolve1(Donnees)
    Donnees = Evolve1(Donnees)
    Donnees = Evolve1(Donnees)
    return Donnees[0]


def EvolveN(SecNum, Nb, CachedDictMonkey=dict()):
    Change = []
    for i in range(Nb):
        SecNum2 = Evolve(SecNum)
        CurPrice = SecNum2 % 10
        PrevPrice = SecNum % 10
        if len(Change) < 4:
            Change.append(CurPrice - PrevPrice)
        else:
            Change = Change[1:]
            Change.append(CurPrice - PrevPrice)
        if len(Change) == 4:
            Index = tuple(Change)
            if Index not in CachedDictMonkey:
                CachedDictMonkey[Index] = CurPrice
        SecNum = SecNum2
    return (SecNum, CachedDictMonkey)



# Part 1

Resultat = []
DictTot = dict()
for s in Input:
    Temp = EvolveN(int(s), 2000, dict())
    Resultat.append(Temp[0])
    for key, value in Temp[1].items():
        if key in DictTot:
            DictTot[key] += value
        else:
            DictTot[key] = value
print("Solution part 1: " + str(sum(Resultat)))

# Part 2

KeyMax = max(DictTot, key=DictTot.get)
Maximum = DictTot[KeyMax]
print("Solution part 2: " + str(Maximum) + " with sequence of " + str(KeyMax))