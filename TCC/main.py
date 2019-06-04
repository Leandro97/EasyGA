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

log = [] #this array will store the progression of best individual
'''
Population initialisation. The array representing a individual has
geneNumber + 1 genes because the last position stores its fitness
'''
def init():
    global simList

    '''Initial population starts the proccess with random values'''
    if su.geneType == 'float': 
        su.population = np.random.uniform(su.geneMinValue, su.geneMaxValue, (su.populationSize, su.geneNumber + 1))
    else:
        su.population = np.random.randint(su.geneMinValue, su.geneMaxValue + 1, (su.populationSize, su.geneNumber + 1))

    '''Calculating the fitness of the initial population'''
    for chrom in su.population:
        if  su.geneType == 'float':
            chrom = [round(value, 2) for value in chrom]

        chrom[-1] = fit.getFitness(chrom)

    su.population = op.sort(su.population) #Sorting the individuals according to fitness
    su.currentGeneration = 1

'''Here all the steps of the algorithm take place'''
def evolve():
    global log
    champion = []
    last = 1 #Last generation where the champion changed
    counter = 0 #Counts how many generations the champion remains the same
    init()

    while (su.currentGeneration <= su.maxGenerations):
        op.crossover(su.population)
        #print("---")
        su.population = op.sort(su.population)

        if len(champion) == 0:
            champion = list(su.population[0])
            log.append("Generation " + str(su.currentGeneration) + " - Champion: " + str(champion) + "\n")

        #Verifying if champion changed
        if(su.population[0][-1] == champion[-1]):
            counter += 1
        else:
            counter = 0
            champion = list(su.population[0])
            log.append("Generation " + str(su.currentGeneration) + " - Champion: " + str(champion) + "\n")
            last = su.currentGeneration
        
        #Population returns to its initial size
        su.currentPopulationSize = su.populationSize
        su.currentGeneration += 1

        #Verifying if max generation number was reached 
        if(counter == su.plateau ): break

        #print("###")
    return last, champion

'''Each time the user runs a scenario, this function is called'''
def simulation(tests):
    global log
    rd.seed(a = su.seed)
    np.random.seed(seed = su.seed)

    fitnessSum = 0
    simList = []    
    bestIndividual = {}

    fileName = rec.newFile()

    for i in range(tests):
        log.append("\n--------- Simulation #{} ---------\n\n".format(i + 1))

        sim = {}
        sim['id'] = i + 1
        sim['last'], sim['champion'] = evolve()

        fitnessSum += sim['champion'][-1]
        simList.append(sim)


    #Ordering the simulations by fitness
    reverse = True if(su.task == 'max') else False    
    simByChampion = sorted(simList, key=lambda sim: sim['champion'][-1], reverse = reverse)
    bestIndividual = simByChampion[0]

    #Verifying champion reached with less generations
    for i in range(1, tests):
        if(tests >= i + 1):
            if(bestIndividual['champion'][-1] == simByChampion[i]['champion'][-1] and bestIndividual['last'] > simByChampion[i]['last']):
                bestIndividual = simByChampion[i]

    rec.close(bestIndividual, fitnessSum, tests, log)

simulation(5)

print("Done!")
