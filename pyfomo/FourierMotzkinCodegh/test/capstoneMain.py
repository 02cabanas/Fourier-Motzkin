#%%
# -*- coding: utf-8 -*-
print("\n\n\n")


import math
from queue import Empty
from tokenize import String
from typing import *
import numpy as np
import pprint #pretty printer
from itertools import chain, combinations, permutations
import time
import re

from src.main import fourier_motzkin_eliminate_single

# Story 10 method / function
def getNumOfVar() -> int:
    numofvar = int(input("\nHow many different variables would you like?\nPlease type an integer Number:\n"))
    print("\nYou want %d different variables. "%numofvar)
    correct = str(input("Is this correct (Y/n)?\n"))
    if correct == "Y":
        return numofvar
    else:
        return getNumOfVar()

# Story 11 method / function
def getVarNames() -> List[str]:
    listofvar = str(input("\nWhat variable names would you like?\nPlease type words (strings) seperated by tabs:\n"))
    listofvar = listofvar.split("\t")
    print("\nYou want the following variable names: %s. "%listofvar)
    correct = str(input("Is this correct (Y/n)?\n"))
    if correct == "Y":
        return listofvar
    else:
        return getVarNames()

# Story 12 method / function
def intToVarList(numofvar: int) -> List[str]:
    listofvar = list()
    for i in range(1, numofvar + 1):
        tempstr = "X" + str(i)
        SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")             # translation doesnt work now for some reason
        tempstr.translate(SUB)                                      # translation doesnt work now for some reason
        listofvar.append(tempstr)
    return listofvar

# ====================
# Getting usser input as an information theoretic inequality (method / function)
inputvalues = list()
inputsigns = list()
inputvaluesright = list()
def getUsserInequalityInput(posiblecombosdict):
    inputinequality = input("\nWhat extra condition would you like to add?\n\tUsing the dictionary above use the key for the the desired combination of varibales:\n\tNote dictionary above is in form {1 = [EMPTY], 2 = [X1], 3 = [X2], 4 = [X1, X2], 5 = [X3], 6 = [X1, X3], 7 = [X2, X3], 8 = [X1, X2, X3]} \n\tPlease enter an information theoretic inequality with no spaces in the form of e.x. ->\tH(2)<5\t(this would be equivalant to H(X1) < 5)\n\tRestructure your inequality to only use less than '<', move all constants to the right hand side, and only use plus '+' / minus '-' operations.\n")
    inputvaluesparen = re.findall('\(.*?\)', inputinequality)
    index = 0
    inputinequalitycopy = inputinequality
    index = inputinequalitycopy.find('H')
    while index != -1:
        if index == 0:
            inputsigns.append("+")
            inputinequalitycopy = inputinequalitycopy[inputinequalitycopy.find('H')+1:len(inputinequalitycopy)]
            index = inputinequalitycopy.find('H')
        else:
            inputsigns.append(inputinequalitycopy[inputinequalitycopy.find('H')-1])
            inputinequalitycopy = inputinequalitycopy[inputinequalitycopy.find('H')+1:len(inputinequalitycopy)]
            index = inputinequalitycopy.find('H')

    # print("signs:", inputsigns)
    if(inputinequality.find('=') != -1):
        inputvaluesright.append(inputinequality[inputinequality.find('=')+1:len(inputinequality)])
    elif(inputinequality.find('>') != -1):
        inputvaluesright.append(inputinequality[inputinequality.find('>')+1:len(inputinequality)])
    elif(inputinequality.find('<') != -1):
        inputvaluesright.append(inputinequality[inputinequality.find('<')+1:len(inputinequality)])
    
    # print("inputvaluesright", inputvaluesright)

    for seg in inputvaluesparen:
        # inputvalues.append(seg[seg.find('(')+1:seg.find(')')])
        inputvalues.append(posiblecombosdict[int(seg[seg.find('(')+1:seg.find(')')])])
    # print("input signs:", inputsigns)
    
    print("\nYou want the following variable(s) to be conditioned: %s. "%inputvalues)
    correct = input("Is this correct (Y/n)?\n")
    if correct == "Y":
        return inputvalues
    else:
        return getUsserInequalityInput(posiblecombosdict)


# Story 14 method / function
posiblecombosdict = dict()                                      # initializing the variable "posiblecombosdict" as an empty dict
def genCombos(lenv: int) -> List[List[List[int]]]:                  # lenv = len(listofvar)
    iterable = list();
    for var in range(1, lenv + 1):
        iterable.append(var);
    
    def powerset(s):
        x = len(s)
        masks = [1 << i for i in range(x)]
        for i in range(1 << x):
            yield [ss for mask, ss in zip(masks, s) if i & mask]
    
    for i, combo in enumerate(powerset(iterable), 1):               # enumerate is useful for obtaining an indexed list:    (0, seq[0]), (1, seq[1]), (2, seq[2]), ...      (in our case index starts at 1)
        posiblecombosdict[i] = combo                                # obtains all possible combinations; i.e. for 2 variable -> [0], [1], [2], [1,2]
    print("Dictionary of all possible combinations:", end=" ")      # printing dict of possible combos
    print(posiblecombosdict)                                        # printing ^

    getUsserInequalityInput(posiblecombosdict)

    perm = list(permutations(list(posiblecombosdict), r = 3))       # obtains all possible permutations of the combinations obtained above
    print("\nList of permutations: ", end="")                       # printing list of all possible permutations of the combinations created some 4 lines above
    print(perm)                                                     # printing ^

    # print("=============\n========\n=======\nposiblecombosdic[1] =",posiblecombosdict[1])
    # print("posiblecombosdic[2] =",posiblecombosdict[2])
    # print("posiblecombosdic[3] =",posiblecombosdict[3])
    # print("posiblecombosdic[4] =",posiblecombosdict[4])


    ABCtemplist = [[],[],[]]
    # ABCtemplist[0] = [1,2]
    # ABCtemplist[2] = [1,2,3]
    ABCturn = 0
    ABCbreak = False
    print("ABCtemplist = ", ABCtemplist)
    print("\n\n|\tA\t\t|\tB\t\t|\tC\t\t")
    print("|=======================|=======================|=======================")
    for f in range(len(perm)):                                        # this code sets up the return array
        templf = list(perm[f]) 
        for g in range(len(perm[f])):
            # print("in g loop")
            # if (g == 1 and ABCturn != 2):                                                # ^
            #     # print("breaking due to first rule")
            #     templf = []
            #     break
            # if (ABCturn == 3):

            t = posiblecombosdict[perm[f][g]]                                                            # |
            # print("{} = {}".format(perm[f][g], t), end="")                                                # |
            templf[g] = t                                                                                 # |
            if len(t) == 3:                                                                              # |
                print('|\t{}\t'.format(t), end="")                                                      # |
            else:                                                                                       # |
                print('|\t{}\t\t'.format(t), end="")  
            ABCturn += 1                                                                                # |
        perm[f] = templf
        ABCturn = 0
        print()                                                                                         # \/
                                                                      # this code sets up the return array
    # for f in range(len(perm)):                                      # this code setes up the return array it is also a repeatably included in the code above for printing out a chart of the combinations
    #     for g in range(len(perm[f])):                               # this code is also a repeatably included in the code above for printing out a chart of the combinations ^
    #         t = posiblecombosdict[perm[f][g]]                       # this code is also a repeatably included in the code above for printing out a chart of the combinations ^
    #         templf = list(perm[f])                                  # this code is also a repeatably included in the code above for printing out a chart of the combinations ^
    #         templf[g] = t                                           # this code is also a repeatably included in the code above for printing out a chart of the combinations ^
    #         perm[f] = templf                                        # done setting up the return array ^

    print("\nprinting array that will be returned from story 14 method: Fromat for array [ [A1, B1, C1], [A2, B2, C2], ...., [Az, Bz, Cz] ] \n\twhere z is the length of this array, and A1,B1,C1, A2, ,B2, etc. are the combinations shown on the chart above ^^^\n")
    print(perm)
    print()


    # ==============to deletee===
    for i in perm:
        print("H({}{}) + H({}{}) - H({}{}{}) - H({}) >= 0".format(i[0],i[1],i[1],i[2],i[0],i[1],i[2],i[2]))
    #=====to delete ^^^^^========




    return perm


# Story 15 method / function

# Story 16 method / function

# method getting users preference for inputing variable names generate classical inequalities
def varinput() -> List[str]:
    varinputoption = int(input("Select one of two options...\n\n(1)\tInput the number of variables desired to generate classical inequalities\n(2)\tInput the desired names of the variables from which to generate classical inequalities\t\n\nPlease type an integer; either '1' or '2'\n"))
    if varinputoption == 1:
        numofvar = getNumOfVar()
        listofvar = intToVarList(numofvar)
        return listofvar
    elif varinputoption == 2:
        listofvar = getVarNames()
        return listofvar
    else:
        print("\nInvalid selection. Please", end=" ")
        return varinput()


# get variable input from user and saves it to
listofvar = varinput()

# print List of variables (for testing)
print("\nList of variables:")
for str in listofvar:
    print(str, end=", ")
print("\n                \n")

#testing
#========
permie = genCombos(len(listofvar))
#========


# A = np.array([[1,1,1],[1,1,-1],[1,-1,1],[-1,1,1],[-1,0,0], [0,-1,0], [0,0,-1]])     # would take this input from user
# b = np.array([[5,3,4,2,0,0,0]]).T                                                   # would take this input from user
# var_index= 0                                                                        # would take this input from user

def FMloop(A, b, var_index):
    # for loop to run FM recursively:
    fmcont = True
    while fmcont:
        (A_new,b_new)=fourier_motzkin_eliminate_single(var_index, A, b, atol=10**-8)
        A = A_new                       # A -> coefficientleft
        b = b_new                       # b -> coefficientright
        print("A_new: \n{}\n".format(A_new))         # printing
        print("b_new: \n{}\n".format(b_new))       # printing
        for q in A_new:
            # print("[", end="")          # printing for testing
            for z in q:
                # print(z, end=",")       # printing for testing
                if math.isnan(z):       # checks if a value in A_new is nan: if it is then it stop the recursive 'for loop' running FM by asigning 'fmcont' to equal False
                    fmcont = False
                    break    
            # print("]", end="")          # printing for testing
            if fmcont == False:
                break
        print()                         # printing for testing
        if len(A_new[0]) == 2:          #this breaks the code when there is one variable left ?
            break
        # add condition to stop when there is only one variable left ##########**********************


def Union(lst1, lst2):
    final_list = list(set(lst1) | set(lst2))
    return final_list

def Union3(lst1, lst2, lst3):
    final_list = list(set(lst1) | set(lst2) | set(lst3))
    return final_list

A = []
b = [[]]

# print(posiblecombosdict)
# p = [[3], [1,3], [2]]
for p in permie:
    print("\ncurrent p: ", p)

    Afinallen = len(posiblecombosdict.keys());
    Apart = [0]*Afinallen
    print("Apart before being filled: ",Apart)

    u = Union(p[0], p[2])
    print("union: {} #--# p[0], p[2] --> {},{}".format(u,p[1], p[2]))
    index = (list(posiblecombosdict.keys())[list(posiblecombosdict.values()).index(u)])-2
    print("index of union in dict; index: ", index)
    Apart[index] = -1

    u = Union(p[1], p[2])
    print("union: {} #--# p[1], p[2] --> {},{}".format(u,p[1], p[2]))
    index = (list(posiblecombosdict.keys())[list(posiblecombosdict.values()).index(u)])-2
    print("index of union in dict; index: ", index)
    Apart[index] = -1

    u = Union3(p[0], p[1],p[2])
    print("union: {} #--# union of p[1], p[2], p[3] --> {},{},{}".format(u,p[0], p[1], p[2]))
    index = (list(posiblecombosdict.keys())[list(posiblecombosdict.values()).index(u)])-2
    print("index of union in dict; index: ", index)
    Apart[index] = +1


    if p[2]:
        print("H[C]: ", p[2])
        index = (list(posiblecombosdict.keys())[list(posiblecombosdict.values()).index(p[2])])-2
        print("index of H[C] in dict; index: ", index)
        Apart[index] = +1

    print("Apart: ", Apart)
    A.append(Apart)
    b[0].append(0)


# Handleing user input now
print("Handleing user input now")
curr = 0
Afinallen = len(posiblecombosdict.keys());
Apart = [0]*Afinallen
for val in inputvalues:
    print("Apart before being filled: ",Apart)
    print("val:", val)
    index = (list(posiblecombosdict.keys())[list(posiblecombosdict.values()).index(val)])-2

    print("index: ", index)
    if inputsigns[curr] == "+":
        Apart[index] = +1
    elif inputsigns[curr] == "-":
        Apart[index] = -1
    curr += 1
    # print("sign: {}, index: {}".format(inputsigns[curr], index))
    print("Apart: ", Apart)
A.append(Apart)
b[0].append(int(inputvaluesright[0]))



Aformat = posiblecombosdict
Aformat.pop(1)
print("\nA format:", [list(Aformat.values())])
print("\nA: \n", A)
print("\n\nb: \n", b)

A = np.array(A)
b = np.array(b).T
FMloop(A,b,0)














