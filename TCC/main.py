'''
Main file. here all the steps of the algorithm are done.
'''

import setup as su
from setup import *
import fitness as fit
import operations as op

import numpy as np

'''
Population initialization. The array representing a individual has
geneNumber + 1 genes because the last position stores its fitness
'''
def init():
    fit.init()

    if su.geneType == 'float':
        #'''Making the np.random.uniform includes the upper limit'''
        #maxValue = np.nextafter(su.geneMaxValue, su.geneMaxValue + 1)    
        su.population = np.random.uniform(su.geneMinValue, su.geneMinValue, (su.populationSize, su.geneNumber + 1))
    else:
        su.population = np.random.randint(su.geneMinValue, su.geneMaxValue + 1, (su.populationSize, su.geneNumber + 1))

    '''Calculating the fitness of the initial population'''
    for chrom in su.population:
        #Setting the user selected gene values
        for gene in su.geneInit:
            chrom[gene] = su.geneInit[gene]

        chrom[-1] = fit.getFitness(chrom)
        
'''Here all the steps of the algorithm take place'''
def evolve():
    init()
    #print(su.population)
    #print('###')
    op.crossover(su.population)
    print(su.population)
            
    #sel.init()
    #cross.nit()
    
evolve()
