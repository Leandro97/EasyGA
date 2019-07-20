import math as math
from math import *
import random as rd

'''Calculating fitness on multidimension functions'''
def getFitness(chrom, su):   
    func = su.function
    begin = 0

    for i in range(len(su.varLength)):
        end = begin + su.varLength[i]

        aux = chrom.copy()[begin: end]
        #print(aux)

        aux[0] = "-" if (aux[0] == "1") else "0"

        var = 'x' + str(i + 1)
        value = int(''.join(aux), 2)


        if(value < su.varDomain[i][0] or value > su.varDomain[i][1]):
            value = rd.randint(su.varDomain[i][0], su.varDomain[i][1])
            chrom[begin: end] = list(("{0:0" + str(su.varLength[i]) + "b}").format(value))
            chrom[0] = '1' if (chrom[0] == '-') else '0'

        #Replacing values
        func = func.replace(var, '(' + str(value) + ')')
        begin = end

    #chrom.tolist()
    result = eval(func)

    chrom[-1] = result

    return chrom

# def binaryFitness(chrom, su):
#     aux = su.function
#     binaryVal = ''

#     for i in range(1, su.geneNumber):
#         binaryVal += str(chrom[i])

#     value = int(binaryVal, 2)

#     if(chrom[0] == 1):
#         value *= -1

#     #Verifying limits of bit string
#     if(value < su.varMinValue or value > su.varMaxValue):
#         value = rd.randint(su.varMinValue, su.varMaxValue + 1)

#         bAux = bin(value)
#         signal = bAux[0]
#         bAux = bAux[3:] if(signal == '-') else bAux[2:]
#         chrom[0] = 1 if(signal == '-') else 0

#         #Now the chromossome is capped at one of the limits
#         counter = 0
#         for i in range(1, su.geneNumber):
#             if(i < su.geneNumber - len(bAux)):
#                 chrom[i] = 0
#             else:
#                 chrom[i] = bAux[counter]
#                 counter += 1

#     #Replacing values
#     aux = aux.replace('x1', '(' + str(value) + ')')

#     #Evaluating function
#     result = eval(aux)
#     chrom[-1] = result

#     return chrom