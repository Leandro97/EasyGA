import setup as su
from setup import *
import fitness as fit

import numpy as np
import random as rd

'''
Population initialization. The array representing a individual has
geneNumber + 1 genes because the last position stores its fitness
'''
def init():
    su.currentGeneration = 1

    if su.geneType == 'float':
        #'''Making the np.random.uniform inclusive'''
        #maxValue = np.nextafter(su.geneMaxValue, su.geneMaxValue + 1)
        
        su.population = np.random.uniform(su.geneMinValue, su.geneMaxValue, (su.populationSize, su.geneNumber + 1))
    else:
        su.population = np.random.randint(su.geneMinValue, su.geneMaxValue + 1, (su.populationSize, su.geneNumber + 1))

    '''Calculating the fitnes of the initial population'''
    fit.init()
    for chrom in su.population:
        chrom[su.geneNumber] = fit.getFitness(chrom)
        
'''Here all the steps of the algorithm take place'''
def evolve():
    init()
            
    #sel.init()
    #cross.nit()

#TODO
def mutation():
    if su.geneType == 'int':
        return rd.randint(su.geneMinValue, su.geneMaxValue + 1)
    else:
        return rd.unform(su.geneMinValue, su.geneMaxValue)
    
evolve()
print(su.population)

'''
for chrom in population:
    #fit.getFitness(function, chrom)
    fit.getFitness(function, chrom)
    print(chrom)
'''

