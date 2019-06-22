import math as math
from math import *

'''Calculating fitness on multidimension functions'''
def getFitness(chrom, su):
    if su.geneType == "bin":
        return binaryFitness(chrom, su)     

    aux = su.function
    for i in range(su.geneNumber):
        var = 'x' + str(i + 1)
        value = '(' + str(chrom[i]) + ')'

        #Replacing values
        aux = aux.replace(var, value)

    #Evaluating function
    result = eval(aux)
    chrom[-1] = result
    return chrom

def binaryFitness(chrom, su):
    aux = su.function
    binaryVal = ''

    for i in range(1, su.geneNumber):
        binaryVal += str(chrom[i])

    value = int(binaryVal, 2)

    if(chrom[0] == 1):
        value *= -1

    #Verifying limits of bit string
    if(value < su.varMinValue or value > su.varMaxValue):

        if(value < su.varMinValue):
            value = su.varMinValue
        else:
            value = su.varMaxValue

        bAux = bin(value)
        signal = bAux[0]
        bAux = bAux[3:] if(signal == '-') else bAux[2:]
        chrom[0] = 1 if(signal == '-') else 0

        #Now the chromossome is capped at one of the limits
        counter = 0
        for i in range(1, su.geneNumber):
            if(i < su.geneNumber - len(bAux)):
                chrom[i] = 0
            else:
                chrom[i] = bAux[counter]
                counter += 1

    #Replacing values
    aux = aux.replace('x1', '(' + str(value) + ')')

    #Evaluating function
    result = eval(aux)
    chrom[-1] = result

    return chrom

        