"""
Day 24 of 2024 advent of code
"""

import re

# Inputs

Test = False

if Test:
    Input = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""
else:
    with open("/2024/Input/day24.txt") as String:
        Input = String.read().strip()

Valeurs, Operations = Input.split("\n\n")
ValeursMem = dict()
for i in Valeurs.split("\n"):
    val, bit = i.split(": ")
    ValeursMem[val] = int(bit)

def FormatOperation(String):
    val1, oper, val2, res = String.split(" ")
    return (res, val1, val2, oper)
Operations = [FormatOperation(re.sub(" ->", "", s)) for s in Operations.split("\n")]
OperationsMem = dict()
for op in Operations:
    OperationsMem[op[0]] = (op[1], op[2], op[3])

# Functions

def Gate(x, y, oper):
    match oper:
        case "AND": return x & y
        case "OR": return x | y
        case "XOR": return x ^ y

def ResolveConnexions(Operation):
    res = Operation
    val1, val2, oper = OperationsMem[Operation]
    if res in ValeursMem:
        return ValeursMem[res]
    else:
        if val1 not in ValeursMem:
            ValeursMem[val1] = ResolveConnexions(val1)
        if val2 not in ValeursMem:
            ValeursMem[val2] = ResolveConnexions(val2)
        Resultat = Gate(ValeursMem[val1], ValeursMem[val2], oper)
        ValeursMem[res] = Resultat
        return Resultat

# Part 1

for op in Operations:
    print("Operation for " + op[0] + ": result of " + str(ResolveConnexions(op[0])))
Res = 0
MaxZ = max([int(re.sub(r"^z", "", s)) if re.search(r"^z\d+", s) != None else 0 for s in ValeursMem.keys()])
for z in range(MaxZ + 1):
    Res += 2 ** z * ValeursMem["z" + str(z).rjust(2, "0")]
print("Solution part 1: " + str(Res))

# Part 2

Bit1 = set()
Bit0 = set()
for i in OperationsMem.keys():
    if ValeursMem[i] == 0:
        Bit0.add(i)
    else:
        Bit1.add(i)

Errors = []
Carry = 0
VraiesValeurs = []
for i in range(MaxZ):
    Res = ValeursMem["x" + str(i).rjust(2, "0")] + ValeursMem["y" + str(i).rjust(2, "0")] + Carry
    Carry = Res // 2
    Bit = Res % 2
    if Bit != ValeursMem["z" + str(i).rjust(2, "0")]: Errors.append("z" + str(i).rjust(2, "0"))
    VraiesValeurs.append(Bit)
if ValeursMem["z" + str(i + 1).rjust(2, "0")] != Carry: Errors.append("z" + str(i + 1).rjust(2, "0"))
VraiesValeurs.append(Carry)

def RechOperations(Resultat):
    Reponses = set()
    ARegarder = [Resultat]
    while len(ARegarder) > 0:
        Res = ARegarder.pop(0)
        if Res in OperationsMem:
            Reponses.add(OperationsMem[Res][0])
            Reponses.add(OperationsMem[Res][1])
            ARegarder.append(OperationsMem[Res][0])
            ARegarder.append(OperationsMem[Res][1])
    return Reponses

Sets = dict()
for i in range(MaxZ):
    if i == 0:
        Sets["z" + str(i).rjust(2, "0")] = RechOperations("z" + str(i).rjust(2, "0"))
    else:
        Sets["z" + str(i).rjust(2, "0")] = RechOperations("z" + str(i).rjust(2, "0")).difference(Sets["z" + str(i - 1).rjust(2, "0")])

for er in Errors:
    print(er + ":" + str(OperationsMem[er]))

# Les erreurs commencent à 14 et s'arrêtent à 34
# On peut supposer que les permutations sont entre les fils de ces operations

PossiblesSwaps = []
for z in Errors:
    for i in Sets[z]:
        if i in OperationsMem: PossiblesSwaps.append(i)
"""from itertools import combinations
Possibilites = [i for i in combinations(PossiblesSwaps, 8)]"""

def ExamineGates(Operation, Depth=0, StopExam=r"^x\d+|^y\d+", MaxDepth = 5):
    if Depth <= MaxDepth:
        print("|   " * (Depth) + OperationsMem[Operation][2])
        print("|   " * (Depth) + "  -" + OperationsMem[Operation][0])
        if re.search(StopExam, OperationsMem[Operation][0]) == None: ExamineGates(OperationsMem[Operation][0], Depth + 1)
        print("|   " * (Depth) + "  -" + OperationsMem[Operation][1])
        if re.search(StopExam, OperationsMem[Operation][1]) == None: ExamineGates(OperationsMem[Operation][1], Depth + 1)

ExamineGates("z18", 0, r"^x\d+|^y\d+", 3)
for i, j in OperationsMem.items():
    #if j[2] == "XOR" and (j[0] == "x23" or j[1] == "x23"):
    if (j[0] == "tfn" or j[1] == "tfn"):
        print(i)
        print(j)


# Résolution
Input2 = Input
Input2 = re.sub("dfb XOR bfn -> hbk", "dfb XOR bfn -> z14", Input2)
Input2 = re.sub("sjr OR tck -> z14", "sjr OR tck -> hbk", Input2)
Input2 = re.sub("dvw AND rpg -> z23", "dvw AND rpg -> dbb", Input2)
Input2 = re.sub("dvw XOR rpg -> dbb", "dvw XOR rpg -> z23", Input2)
Input2 = re.sub("grp XOR fgr -> kvn", "grp XOR fgr -> z18", Input2)
Input2 = re.sub("y18 AND x18 -> z18", "y18 AND x18 -> kvn", Input2)
Input2 = re.sub("x34 XOR y34 -> tfn", "x34 XOR y34 -> cvh", Input2)
Input2 = re.sub("x34 AND y34 -> cvh", "x34 AND y34 -> tfn", Input2)


Valeurs, Operations = Input2.split("\n\n")
ValeursMem = dict()
for i in Valeurs.split("\n"):
    val, bit = i.split(": ")
    ValeursMem[val] = int(bit)
Operations = [FormatOperation(re.sub(" ->", "", s)) for s in Operations.split("\n")]
OperationsMem = dict()
for op in Operations:
    OperationsMem[op[0]] = (op[1], op[2], op[3])

for op in Operations:
    print("Operation for " + op[0] + ": result of " + str(ResolveConnexions(op[0])))

# Check

Bit1 = set()
Bit0 = set()
for i in OperationsMem.keys():
    if ValeursMem[i] == 0:
        Bit0.add(i)
    else:
        Bit1.add(i)
Errors = []
Carry = 0
VraiesValeurs = []
for i in range(MaxZ):
    Res = ValeursMem["x" + str(i).rjust(2, "0")] + ValeursMem["y" + str(i).rjust(2, "0")] + Carry
    Carry = Res // 2
    Bit = Res % 2
    if Bit != ValeursMem["z" + str(i).rjust(2, "0")]: Errors.append("z" + str(i).rjust(2, "0"))
    VraiesValeurs.append(Bit)
if ValeursMem["z" + str(i + 1).rjust(2, "0")] != Carry: Errors.append("z" + str(i + 1).rjust(2, "0"))
VraiesValeurs.append(Carry)

Sets = dict()
for i in range(MaxZ):
    if i == 0:
        Sets["z" + str(i).rjust(2, "0")] = RechOperations("z" + str(i).rjust(2, "0"))
    else:
        Sets["z" + str(i).rjust(2, "0")] = RechOperations("z" + str(i).rjust(2, "0")).difference(Sets["z" + str(i - 1).rjust(2, "0")])

for er in Errors:
    print(er + ":" + str(OperationsMem[er]))