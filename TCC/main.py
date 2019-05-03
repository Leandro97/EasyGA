'''

Federal University of Alagoas - UFAL
Author: Leandro Martins de Freitas

'''
import setup as su
from setup import *
import fitness as fit
import operations as op
import selection as sel 
import record as rec  
import datetime
import numpy as np


'''
Population initialisation. The array representing a individual has
geneNumber + 1 genes because the last position stores its fitness
'''
def init():
    global simList
    #Initialising fitness function
    fit.init()

    '''Initial population starts the eproccess with random values'''
    if su.geneType == 'float': 
        su.population = np.random.uniform(su.geneMinValue, su.geneMinValue, (su.populationSize, su.geneNumber + 1))
    else:
        su.population = np.random.randint(su.geneMinValue, su.geneMaxValue + 1, (su.populationSize, su.geneNumber + 1))

    '''Calculating the fitness of the initial population'''
    for chrom in su.population:
        #Setting the user selected gene values
        for gene in su.geneInit:
            chrom[gene] = su.geneInit[gene]

        chrom[-1] = fit.getFitness(chrom)

    su.population = op.sort(su.population) #Sorting the individuals according to fitness
    su.totalFitness = op.getTotalFitness() #Getting the sum of population's fitness
    su.currentGeneration = 1

'''Here all the steps of the algorithm take place'''
def evolve():
    champion = []
    last = 0 #Last generation where the champion changed
    counter = 0 #Counts how many generations the champion remains the same
    init()

    while (su.currentGeneration <= su.maxGenerations):
        if len(champion) == 0:
            champion = su.population[0]

        op.crossover(su.population)
        su.population = op.sort(su.population)

        #Verifying if champion changed
        if(su.population[0][-1] == champion[-1]):
            counter += 1
        else:
            counter = 0
            champion = su.population[0]
            rec.write("Generation " + str(su.currentGeneration) + " - Champion: " + str(champion) + "\n")
            last = su.currentGeneration
        
        #Population returns to its initial size
        su.population = su.population[:su.populationSize]
        su.currentPopulationSize = su.populationSize
        su.currentGeneration += 1

        #Verifying if max generation number was reached 
        if(counter == su.plateau ): break

        #print("###")
    return last, champion
    rec.write("\n")

def key(val):
    return val['last']

'''Each time the user runs a scenario, this function is called'''
def simulation(tests):
    simList = []
    bestIndividual = []
    bestSimulation = 0

    rec.newFile()

    for i in range(tests):
        rec.write("\n--------- Simulation #{} ---------\n\n".format(i + 1))
        
        sim = {}
        sim['id'] = i + 1
        sim['last'], sim['champion'] = evolve()
        simList.append(sim)

    simList = sorted(simList, key=lambda sim: sim['last'])

    rec.write('\n---------------------------------\n')
    rec.write('\n-> Best simulation: #{}. Champion: {} <-'.format(simList[0]['id'], simList[0]['champion']))
    rec.close()

simulation(50)

print(su.population[0])