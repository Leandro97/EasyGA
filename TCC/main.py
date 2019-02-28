import setup as su
from setup import *

import fitness as fit

def evolve():
    fit.init()
    #sel.init()
    #cross.nit()
    
evolve()
for chrom in population:
    #fit.getFitness(function, chrom)
    print(fit.getFitness(function, chrom))

function = "x1 + x2 + x3"
su.geneNumber = 3
chroms = [[1,2,3], [3,4,5]]
evolve()
for chrom in population:
    #fit.getFitness(function, chrom)
    print(fit.getFitness(function, chrom))

