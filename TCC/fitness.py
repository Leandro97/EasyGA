import math as math
from math import *
import random as rd

def getFitness(chrom, su):
    if (su.geneType == "Binary string"):
        return binaryFitness(chrom, su)

    func = su.function
    
    for i in range(len(su.varLength)):  
        var = 'x' + str(i + 1)
        value = chrom[i]  


        if(su.geneType == "Integer string"):
            aux = int(value)
        else:
            aux = float(value)

        if(aux < su.varDomain[i][0] or aux > su.varDomain[i][1]):
            lower = su.varDomain[i][0]
            upper = su.varDomain[i][1]
            value = rd.randint(lower, upper) if (su.geneType == "Integer string") else rd.uniform(lower, upper)
            chrom[i] = value

        func = func.replace(var, '(' + str(value) + ')')
    
    try:
        result = eval(func)
    except NameError as e:
        return (False, e)
    except:
        return (False, False)

    chrom[-1] = result

    if su.geneType == "Float string":
        chrom = [round(float(value), 2) for value in chrom]

    return chrom

'''Calculating fitness for binary representation'''
def binaryFitness(chrom, su):   
    func = su.function
    begin = 0

    for i in range(len(su.varLength)):
        end = begin + su.varLength[i]

        aux = chrom[begin: end].copy()
        aux[0] = "-" if (aux[0] == "1") else "0"
        value = int(''.join(aux), 2)

        if(value < su.varDomain[i][0] or value > su.varDomain[i][1]):
            value = rd.randint(su.varDomain[i][0], su.varDomain[i][1])
            chrom[begin: end] = list(("{0:0" + str(su.varLength[i]) + "b}").format(value))

        #Replacing values
        chrom[begin] = '1' if (chrom[begin] == '-') else '0'

        var = 'x' + str(i + 1)
        func = func.replace(var, '(' + str(value) + ')')
        begin = end

    #result = eval(func)
    #SyntaxError
    try:
        result = eval(func)
    except NameError as e:
        return (False, e)
    except:
        return (False, False)

    chrom[-1] = result
    return chrom