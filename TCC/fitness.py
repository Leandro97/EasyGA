import sympy as sp
from sympy import *
import setup
from setup import chrom as chrom
aux = ""

for i in range(1, len(chrom)):
    aux += "x" + str(i) + ", "

aux += "x" + str(len(chrom))
sym = aux + " = symbols('" + aux + "')"
exec(sym)

def getFitness(function, chrom):
    values = []
    expr = sympify(function)

    for i in range(len(chrom)):
        values.append(("x" + str(i + 1), chrom[i]))
    
    result =  expr.subs(values)
    #print(expr)
    #print(result)
    return result

