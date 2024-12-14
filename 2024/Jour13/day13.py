import re

with open("C:/Users/gmulier/Documents/GitHub/AdventCode/2024/Input/day13.txt") as String:
    Machines = String.read().split('\n\n')

"""with open('C:/Users/gmulier/Documents/GitHub/AdventCode/2024/Input/day13.txt') as f:
    scenarios = f.read().split('\n\n')


def parse(scenario):
    output = {}
    a, b, prize = scenario.splitlines()
    output['A'] = [int(item.split('+')[1]) for item in a.split(':')[1].split(', ')]
    output['B'] = [int(item.split('+')[1]) for item in b.split(':')[1].split(', ')]
    output['Prize'] = [10000000000000 + int(item.split('=')[1]) for item in prize.split(':')[1].split(', ')]
    return output


scenarios = [parse(scenario) for scenario in scenarios]


def solve(scenario):
    ax, ay = scenario['A']
    bx, by = scenario['B']
    tx, ty = scenario['Prize']
    b = (tx * ay - ty * ax) // (ay * bx - by * ax)
    a = (tx * by - ty * bx) // (by * ax - bx * ay)
    print(a)
    print(b)
    if ax * a + bx * b == tx and ay * a + by * b == ty:
        return 3 * a + b
    else:
        return 0


answer = [solve(scenario) for scenario in scenarios]
print(sum(answer))"""


def ExtractInputs(Machine, part2=False):
    Regex = r"^Button A: X([\+0-9]+), Y([\+0-9]+)\nButton B: X([\+0-9]+), Y([\+0-9]+)\nPrize: X=([0-9]+), Y=([0-9]+)$"
    Ajout = part2 * 10000000000000
    Ax = int(re.sub(Regex, r"\1", Machine))
    Ay = int(re.sub(Regex, r"\2", Machine))
    Bx = int(re.sub(Regex, r"\3", Machine))
    By = int(re.sub(Regex, r"\4", Machine))
    X = int(re.sub(Regex, r"\5", Machine)) + Ajout
    Y = int(re.sub(Regex, r"\6", Machine)) + Ajout
    return [Ax, Ay, Bx, By, X, Y]
def ResoudreMachine(Machine):
    Ax, Ay, Bx, By, X, Y = Machine
    a = (X * By - Y * Bx) // (By * Ax - Bx * Ay)
    b = (X * Ay - Y * Ax) // (Ay * Bx - By * Ax)
    if Ax * a + Bx * b == X and Ay * a + By * b == Y:
        return 3 * a + b
    else:
        return 0

MachinesP1 = [ResoudreMachine(ExtractInputs(Machine)) for Machine in Machines]
print("Réponse part 1 = " + str(sum(MachinesP1)))
MachinesP2 = [ResoudreMachine(ExtractInputs(Machine, True)) for Machine in Machines]
print("Réponse part 2 = " + str(sum(MachinesP2)))





