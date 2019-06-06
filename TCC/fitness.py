import setup as su
from setup import geneNumber, function
from math import *

'''Calculating fitness'''
def getFitness(chrom):
    aux = su.function

    for i in range(su.geneNumber):
        var = "x" + str(i + 1)
        value = str(chrom[i])

        #Replacing values
        aux = aux.replace(var, value)

    #Evaluating function
    result = eval(aux)
    return result