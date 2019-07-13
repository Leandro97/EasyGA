'''

Federal University of Alagoas - UFAL
Author: Leandro Martins de Freitas

'''
'''HISTÓRICO DE SIMULAÇÕES DEVE FAZER PARTE DA CLASSE SETUP'''

import setup
import fitness as fit
import operations as op
import selection as sel 
import record as rec  
import plotter as plt  
import setupManager as suManager
import datetime
import numpy as np
import random as rd

log = [] #this array will store the progression of best individual
plotFitnessLog = [] #stores best individual history of all setups
plotGenerationLog = [] #stores generation history of all setups

'''Each time the user runs a scenario, this function is called'''
def simulation(tests, su):
    global plotFitnessLog
    global plotGenerationLog
    global log

    if not su.enabled:
        return

    su.population = []
    log = []
    generationHistory = []
    simList = []    
    bestIndividual = {}

    rd.seed(a = su.seed)
    np.random.seed(seed = su.seed)
    fitnessSum = 0

    fileName = rec.newFile(su)

    for i in range(tests):
        log.append("\n--------- Simulation #{} ---------\n\n".format(i + 1))

        sim = {}
        sim['id'] = i + 1
        sim['last'], sim['champion'], sim['history'] = evolve(su)

        fitnessSum += sim['champion'][-1]
        simList.append(sim)
        generationHistory.append((sim['id'], sim['last']))

    #Ordering the simulations by fitness
    simByChampion = sorted(simList, key = lambda sim: sim['champion'][-1], reverse = True if(su.task == 'max') else False)
    bestIndividual = simByChampion[0]

    #Verifying champion reached with less generations
    for i in range(1, tests):
        if(tests >= i + 1):
            if(bestIndividual['champion'][-1] == simByChampion[i]['champion'][-1] and bestIndividual['last'] > simByChampion[i]['last']):
                bestIndividual = simByChampion[i]
            else:
                break

    average = fitnessSum / tests
    rec.close(bestIndividual, average, log, su) #saving simulation report
    plotFitnessLog.append(bestIndividual['history'])
    plotGenerationLog.append(generationHistory)

'''Here all the steps of the algorithm take place'''
def evolve(su):
    global log
    champion = []
    fitnessHistory = [] #stores a (generation, fitness) pair. Will be used on plotting
    last = 1 #Last generation where the champion changed
    counter = 0 #Counts how many generations the champion remains the same
    init(su)

    #Recording first generation
    champion = list(su.population[0])
    log.append("Generation " + str(su.currentGeneration) + " - Champion: " + str([round(value, 2) for value in champion]) + "\n")
    fitnessHistory.append((su.currentGeneration, champion[-1]))
    su.currentGeneration += 1

    while (su.currentGeneration <= su.maxGenerations):
        op.crossover(su)
        su.population = op.sort(su)

        #Verifying if champion changed
        if(su.population[0][-1] == champion[-1]):
            counter += 1
        else:
            counter = 0
            champion = list(su.population[0])
            log.append("Generation " + str(su.currentGeneration) + " - Champion: " + str(champion) + "\n")
            last = su.currentGeneration
            fitnessHistory.append((su.currentGeneration, champion[-1]))
      
        #Population returns to its initial size
        su.currentPopulationSize = su.populationSize
        su.currentGeneration += 1

        #Verifying if plateu was reached 
        if(counter == su.plateau): break

        #print("###")
    return last, champion, fitnessHistory

'''
Population initialisation. The array representing a individual has
geneNumber + 1 genes because the last position stores its fitness.
In binary strings, the first bit stores the signal: 1 if negative,
0 if positive
'''
def init(su):

    su.varDomain = [[0, 10], [1, 5], [1, 5], [-1, 3], [10, 50], [1, 5]]
    su.population = []
    '''Initial population starts the proccess with random values'''
    if su.geneType == 'float': 
        for i in range(su.populationSize):
            su.population.append([])
            for j in range(su.geneNumber):
                su.population[i].append(rd.uniform(su.varDomain[j][0], su.varDomain[j][1]))
            su.population[i].append(0)
        #su.population = np.random.uniform(su.varMinValue, su.varMaxValue, (su.populationSize, su.geneNumber + 1))
    elif su.geneType == 'int':
        for i in range(su.populationSize):
            su.population.append([])
            for j in range(su.geneNumber):
                su.population[i].append(rd.randint(su.varDomain[j][0], su.varDomain[j][1]))
            su.population[i].append(0)
        #su.population = np.random.randint(su.varMinValue, su.varMaxValue + 1, (su.populationSize, su.geneNumber + 1))
    else:
        minV = len(bin(abs(su.varMinValue))) - 1
        maxV = len(bin(abs(su.varMaxValue))) - 1
        su.geneNumber = max(minV, maxV)
        su.population = np.random.randint(0, 2, (su.populationSize, su.geneNumber + 1))


    '''Calculating the fitness of the initial population'''
    for chrom in su.population:
        if  su.geneType == 'float':
            chrom = [round(value, 2) for value in chrom]

        chrom = fit.getFitness(chrom, su)

    su.population = op.sort(su) #Sorting the individuals according to fitness
    su.currentGeneration = 1

def main():
    setupQuantity = 3 
    setupList = suManager.createSetups(setupQuantity)

    for entry in setupList:
        simulation(5, entry)

    plt.plotFitness(plotFitnessLog, setupList[0].task) #plotting graphs
    plt.plotGenerations(plotGenerationLog, setupList[0].task) #plotting graphs
    print("Done!")

main()