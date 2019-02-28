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

def getFitness(function, chrom):
    values = []
    expr = sympify(function)

    for i in range(su.geneNumber):
        values.append(("x" + str(i + 1), chrom[i]))
        
    expr =  expr.subs(values)
    result = float(expr.evalf())
    return result

