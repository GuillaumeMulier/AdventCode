"""
Day 17 advent of code 2024
"""

import re
import numpy as np

# Function

def Combo(value, Ra, Rb, Rc):
    if value <= 3 and value >= 0:
        return value
    elif value == 4:
        return Ra
    elif value == 5:
        return Rb
    elif value == 6:
        return Rc
    else:
        return "Not valid"

def Instruction(opcode, operand, tup_stored, pointeur, output):
    Ra, Rb, Rc = tup_stored
    if opcode == 0:
        Ra = int(Ra / 2 ** Combo(operand, Ra, Rb, Rc))
    elif opcode == 1:
        Rb = operand ^ Rb
    elif opcode == 2:
        Rb = Combo(operand, Ra, Rb, Rc) % 8
    elif opcode == 3:
        if Ra != 0:
            pointeur = operand
            pointeur -= 2
    elif opcode == 4:
        Rb = Rb ^ Rc
    elif opcode == 5:
        output.append(Combo(operand, Ra, Rb, Rc) % 8)
    elif opcode == 6:
        Rb = int(Ra / 2 ** Combo(operand, Ra, Rb, Rc))
    elif opcode == 7:
        Rc = int(Ra / 2 ** Combo(operand, Ra, Rb, Rc))
    pointeur += 2
    return [(Ra, Rb, Rc), pointeur, output]

def OutputA(aa):
    B_1 = (aa % 8) ^ 2
    C_1 = int(aa / 2 ** B_1)
    B_1 = B_1 ^ C_1
    B_1 = B_1 ^ 7
    return B_1 % 8

# Import inputs

Test = False

if Test:
    Input = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""
else:
    with open("C:/Users/gmulier/Documents/GitHub/AdventCode/2024/Input/day17.txt") as String:
        Input = String.read().strip()

Registers, Programme = Input.split("\n\n")
Ra, Rb, Rc = [int(re.sub(r"^Register [A-C]: (\d+)$", r"\1", x)) for x in Registers.split("\n")]
RegisteredValues = (Ra, Rb, Rc)
Programme = [int(x) for x in re.sub("^Program: ", "", Programme).split(",")]
EndProg = len(Programme)

# Part 1

Pointeur = 0
Output = []
while Pointeur < EndProg:
    RegisteredValues, Pointeur, Output = Instruction(Programme[Pointeur], Programme[Pointeur + 1], RegisteredValues, Pointeur, Output)

print("Solution part 1: " + ",".join([str(x) for x in Output]))

# Part 2

# Brut force approach that doesn't work
"""
aa = -1
while aa > 0:
    if aa % 5000 == 0:
        print("We are at number " + str(aa))
    RegisteredValues = (aa, Rb, Rc)
    Pointeur = 0
    Output = []
    while Pointeur < EndProg:
        RegisteredValues, Pointeur, Output = Instruction(Programme[Pointeur], Programme[Pointeur + 1], RegisteredValues,
                                                         Pointeur, Output)
    if Output == Programme:
        print("Solution part 2: " + str(aa))
        aa = -1
    aa += 1
"""

# We know the last A is 0 si that the programm stops
InputPotentiels = [0]
# Going backwards from the programm
for output in Programme[::-1]:
    NewInputsAtStage = []
    for input_pot in InputPotentiels:
    # We know that the possible numbers modulo 8 give the potential input
        for i in range(8):
            # Had to convert to int64 due to overload
            InputConsidered = np.int64(8) * input_pot + i
            OutputFromInput = OutputA(InputConsidered)
            # If we find a valid A, we add it to the list of possible input at the stage
            if OutputFromInput == output:
                NewInputsAtStage.append(InputConsidered)
    # We now know all potential inputs at the stage that could give the number outputed
    # Si we update our potential input list
    InputPotentiels = np.unique(NewInputsAtStage)

print("Solution part 2: " + str(np.min(InputPotentiels)))
print("List of potential solutions found:")
print(InputPotentiels)




