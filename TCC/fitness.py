import setup as su
from setup import geneNumber

import sympy as sp
from sympy import *

'''Formatting the user given function'''
def init():
    aux = ""

    for i in range(1, su.geneNumber):
        aux += "x" + str(i) + ", "

    aux += "x" + str(su.geneNumber)
    sym = aux + " = symbols('" + aux + "')"
    exec(sym)

'''Calculating fitness'''
def getFitness(chrom):
    values = []
    expr = sympify("x1")
    result = 0

    #Looking for sintax errors
    try:
        expr = sympify(su.function)
    except SympifyError:
        print("There is something wrong with the function '{}'. Type a new function: ".format(su.function))
        su.function = input()
        getFitness(chrom)

    for i in range(su.geneNumber):
        values.append(("x" + str(i + 1), chrom[i]))
      
    #Replacing values in function      
    expr =  expr.subs(values)

    #Looking for unknow variables
    try:
        #Evaluating function
        result = float(expr.evalf())
    except TypeError:
        print("There are unknow variables in the function '{}'.".format(su.function))
        print("The variables must be x1, x2, x3, ..., xn. Type a new function: ")
        su.function = input()
        getFitness(chrom)

    return result

'''Calculating error in the functions with defined target'''
def target(chrom):
    function = "Abs(" + str(su.target) + " - (" + su.function + "))"
    values = []

    #Looking for sintax errors
    try:
        expr = sympify(function)
    except SympifyError:
        print("There is something wrong with the function '{}'. Type a new function: ".format(su.function))
        su.function = input()
        getFitness(chrom)

    for i in range(su.geneNumber):
        values.append(("x" + str(i + 1), chrom[i]))
            
    expr =  expr.subs(values)
    
    #Looking for unknow variables
    try:
        #Evaluating function
        result = float(expr.evalf())
    except TypeError:
        print("There are unknow variables in the function '{}'.".format(su.function))
        print("The variables must be x1, x2, x3, ..., xn. Type a new function: ")
        su.function = input()
        getFitness(chrom)

    return result
