import setup as su
from setup import geneNumber

import sympy as sp
from sympy import *

def init():
    aux = ""

    for i in range(1, su.geneNumber):
        aux += "x" + str(i) + ", "

    aux += "x" + str(su.geneNumber)
    sym = aux + " = symbols('" + aux + "')"
    exec(sym)

def getFitness(chrom):
    values = []
    expr = sympify(su.function)

    geneNumber = len(chrom) - 1

    for i in range(su.geneNumber):
        values.append(("x" + str(i + 1), chrom[i]))
            
    expr =  expr.subs(values)
    result = float(expr.evalf())
    return result

def target(chrom):
    function = "Abs(" + str(su.target) + " - (" + su.function + "))"
    values = []
    expr = sympify(function)

    geneNumber = len(chrom) - 1

    for i in range(su.geneNumber):
        values.append(("x" + str(i + 1), chrom[i]))
            
    expr =  expr.subs(values)
    result = float(expr.evalf())
    return result
