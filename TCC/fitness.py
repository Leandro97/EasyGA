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
    return result

def binaryFitness(chrom, su):
    aux = su.function
    binaryVal = ''

    for i in range(1, su.geneNumber):
        binaryVal += str(chrom[i])

    value = int(binaryVal, 2)

    if(chrom[0] == 1):
        value *= -1

    #Replacing values
    aux = aux.replace('x1', '(' + str(value) + ')')

    #Evaluating function
    result = eval(aux)

    #
    if(value > su.varMaxValue or value < su.varMinValue):
        if su.task == "max":
            result = -10000000000
        else:
            result = 10000000000

    return result

        