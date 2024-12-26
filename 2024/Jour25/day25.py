"""
Day 25 of 2024 advent of code
"""

Test = False

if Test:
    Input = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""
else:
    with open("C:/Users/DRY12/Documents/GitHub/AdventCode/2024/Input/day25.txt") as String:
        Input = String.read().strip()

Locks = []
Keys = []
for s in Input.split("\n\n"):
    if s[0] == "#":
        Locks.append(s)
    else:
        Keys.append(s)

HKeys = [[str(x).count("#") for x in list(zip(*k.split("\n")))] for k in Keys]
HLocks = [[str(x).count(".") for x in list(zip(*k.split("\n")))] for k in Locks]

res = 0
for k in HKeys:
    for l in HLocks:
        if all([i <= j for i, j in list(zip(k, l))]): res += 1
print("Solution Part 1: "+ str(res))
