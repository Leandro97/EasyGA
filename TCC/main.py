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
import random as rd

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
        op.crossover(su.population)
        su.population = op.sort(su.population)

        if len(champion) == 0:
            champion = list(su.population[0])
            rec.write("Generation " + str(su.currentGeneration) + " - Champion: " + str(champion) + "\n")

        #Verifying if champion changed
        if(su.population[0][-1] == champion[-1]):
            counter += 1
        else:
            counter = 0
            champion = list(su.population[0])
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
    rd.seed(a = su.seed)
    np.random.seed(seed = su.seed)

    fitnessSum = 0
    simList = []    
    bestIndividual = {}

    rec.newFile()

    for i in range(tests):
        rec.write("\n--------- Simulation #{} ---------\n\n".format(i + 1))

        sim = {}
        sim['id'] = i + 1
        sim['last'], sim['champion'] = evolve()

        fitnessSum += sim['champion'][-1]
        simList.append(sim)

    simByChampion = sorted(simList, key=lambda sim: sim['champion'][-1])
    bestIndividual = simByChampion[0]

    rec.write('\n---------------------------------\n')

    #Verifying champion reached with less generations
    for i in range(1, tests):
        if(tests >= i + 1):
            if(bestIndividual['champion'][-1] == simByChampion[i]['champion'][-1]  and bestIndividual['last'] > simByChampion[i]['last']):
                bestIndividual = simByChampion[i]

    rec.write('\n-> Best simulation: #{}. Champion: {} <-'.format(bestIndividual['id'], bestIndividual['champion']))
    rec.write('\n-> Average fitness: {0:.2f} <-'.format(fitnessSum / tests))
    rec.close()

simulation(10)

print("Done!")