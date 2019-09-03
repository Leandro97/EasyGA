import math as math
from math import *
import random as rd
import re
import struct

def float2bin(num):
    return format(struct.unpack('!I', struct.pack('!f', num))[0], '032b')

def bin2float(binary):
    return struct.unpack('!f',struct.pack('!I', int(binary, 2)))[0]

def truncate(f, n = 3):
    return math.floor(f * 10 ** n) / 10 ** n


'''Checking syntax errors or unknow variables'''
def checkFunction(func, varLength):
    aux = func
    for i in range(varLength):  
        var = 'x' + str(i + 1)
        aux = re.sub(r'\b' + var + r'\b', "(1)", aux)

    try:
        result = eval(aux)
    except NameError as e:
        var = str(e).split()[1]
        return (False, "Variable {} not defined! Verify your function.".format(var))
    except SyntaxError as e:
        return (False, "Syntax error! Verify your fucntion.")
    except:
        return (True, True)
         
    return (True, True)

'''Calculating fitness for integer and float representations'''
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

        #If the gene value exceed the defined boundaries it is replaced by a random number within the interval 
        if(aux < su.varDomain[i][0] or aux > su.varDomain[i][1]):
            lower = su.varDomain[i][0]
            upper = su.varDomain[i][1]
            value = rd.randint(lower, upper) if (su.geneType == "Integer string") else rd.uniform(lower, upper)
            chrom[i] = value


        func = re.sub(r"\b" + var + r"\b", '(' + str(value) + ')', func)
    
    #Trying to evaluate the function. If any errors surface the function returns False
    try:
        result = eval(func)
        float(result)
    except:
        return (False, False)

    chrom[-1] = truncate(result)

    return chrom

'''Calculating fitness for binary representation'''
def binaryFitness(chrom, su):   
    func = su.function
    begin = 0

    for i in range(len(su.varLength)):
        var = 'x' + str(i + 1)
        
        end = begin + su.varLength[i]

        aux = chrom[begin: end].copy()
        value = bin2float("".join(aux))

        if(value < su.varDomain[i][0] or value > su.varDomain[i][1] or isnan(value)):
            value = rd.uniform(su.varDomain[i][0], su.varDomain[i][1])
            binaryValue = float2bin(value)
            chrom[begin: end] = list(binaryValue)

        func = re.sub(r"\b" + var + r"\b", '(' + str(value) + ')', func)
        begin = end

    try:
        result = eval(func)
        float(result)
    except:
        return (False, False)

    chrom[-1] = truncate(result)

    return chrom