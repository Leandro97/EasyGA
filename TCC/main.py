'''
Main file. here all the steps of the algorithm are done.
'''

import setup as su
from setup import *
import fitness as fit
import operations as op

import numpy as np

file = open("output.txt", "a") 

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
    
    su.currentGeneration = 1
    su.champion = 0

'''Here all the steps of the algorithm take place'''
def evolve():
    init()
    counter = 0

    while (su.currentGeneration <= su.maxGenerations):
        su.champion = su.population[0][-1]
        op.crossover(su.population)

        if(su.population[0][-1] == su.champion):
            counter += 1
        else:
            counter = 0
            su.champion = su.population[0][-1]
            file.write("Generation " + str(su.currentGeneration) + " - Champion: " + str(su.champion) + "\n")

        print(su.population)
        print("###")

        if(counter == su.plateau or su.champion == su.target) : break
        su.population = su.population[:su.populationSize]
        su.currentGeneration += 1

    file.write("Last generation: " + str(su.currentGeneration - 1) + "\n\n")

evolve()
