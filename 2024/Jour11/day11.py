"""
Day 11 of advent of code
Too slow in R so trying memoization in Python
"""

import functools

Chemin = "C:/Users/gmulier/Documents/Github/AdventCode/2024"
Input = open(Chemin + "/Input/day11.txt").read().strip()
Input = Input.split(" ")

# Part 1

@functools.cache
def BlinkRecurr (Pierre, IterRest):
    """
    Recursive function to compute number of stones after the iterations

    :param Pierre: Number written on stone
    :param IterRest: Number of iteration left
    :return: Number of stone after the IterRest iterations
    """
    if IterRest == 0:
        return 1
    elif Pierre == "0":
        return BlinkRecurr("1", IterRest - 1)
    elif (len(Pierre) % 2) == 0:
        MoitieUne = BlinkRecurr(str(int(Pierre[0:(len(Pierre) // 2)])), IterRest - 1)
        MoitieDeux = BlinkRecurr(str(int(Pierre[(len(Pierre)//2):len(Pierre)])), IterRest - 1)
        return MoitieUne + MoitieDeux
    else:
        return BlinkRecurr(str(int(Pierre) * 2024), IterRest - 1)

ResPart1 = 0
# Loop over the Input and update the result with the function
for s in Input:
    ResPart1 += BlinkRecurr(s, 25)
print("Résultat part 1 : " + str(ResPart1))

# Part 2 : memoization
ResPart2 = 0
for s in Input:
    ResPart2 += BlinkRecurr(s, 75)
print("Résultat part 2 : " + str(ResPart2))