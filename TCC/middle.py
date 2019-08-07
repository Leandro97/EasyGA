'''

Federal University of Alagoas - UFAL
Author: Leandro Martins de Freitas

'''
import setup
import fitness as fit
import operations as op
import selection as sel 
import record as rec  
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

    log = []
    generationHistory = []
    simList = []    
    bestIndividual = {}

    rd.seed(a = su.seed)
    np.random.seed(seed = su.seed)
    fitnessSum = 0

    #fileName = rec.newFile(su)

    for i in range(tests):
        log.append("\n --------- Simulation #{} ---------\n\n".format(i + 1))

        sim = {}
        sim['id'] = i + 1
        sim['last'], sim['champion'], sim['history'] = evolve(su)

        if(sim['last'] == False):
            return False

        fitnessSum += float(str(sim['champion'][-1]))
        simList.append(sim)
        generationHistory.append((sim['id'], sim['last']))

    #Ordering the simulations by fitness
    simByChampion = sorted(simList, key = lambda sim: float(sim['champion'][-1]), reverse = True if(su.task == 'max') else False)
    bestIndividual = simByChampion[0]

    #Verifying champion reached with less generations
    for i in range(1, tests):
        if(tests >= i + 1):
            if(bestIndividual['champion'][-1] == simByChampion[i]['champion'][-1] and bestIndividual['last'] > simByChampion[i]['last']):
                bestIndividual = simByChampion[i]
            else:
                break

    average = fitnessSum / tests
    rec.record(bestIndividual, average, log, su) #saving simulation report
    plotFitnessLog.append(bestIndividual['history'])
    plotGenerationLog.append(generationHistory)
    return True

def logWriter(su, champion):
    if(su.geneType == "Float string"):
        log.append(" Generation " + str(su.currentGeneration) + " - Champion: " + str([round(value, 3) for value in champion]) + "\n")
    elif(su.geneType == "int"):
        log.append(" Generation " + str(su.currentGeneration) + " - Champion: " + str(champion) + "\n")
    else:
        champion2Int = [int(value) for value in champion[:-1]]
        champion2Int.append(champion[-1])
        log.append(" Generation " + str(su.currentGeneration) + " - Champion: " + str(champion2Int) + "\n")

'''Here all the steps of the algorithm take place'''
def evolve(su):
    global log
    champion = []
    fitnessHistory = [] #stores a (generation, fitness) pair. Will be used on plotting
    last = 1 #Last generation where the champion changed
    counter = 0 #Counts how many generations the champion remains the same
    check = init(su)

    if not check:
        return False, False, False

    #Recording first generation
    champion = list(su.population[0])
    logWriter(su, champion)

    fitnessHistory.append((su.currentGeneration, champion[-1]))
    su.currentGeneration += 1

    while (su.currentGeneration <= su.maxGenerations):
        op.crossover(su)
        op.sort(su)
        #print(su.population)

        #Verifying if champion changed
        if(su.population[0][-1] == champion[-1]):
            counter += 1
        else:
            counter = 0
            champion = list(su.population[0])
            logWriter(su, champion)
            last = su.currentGeneration
            fitnessHistory.append((su.currentGeneration, champion[-1]))
      
        #Population returns to its initial size
        su.currentPopulationSize = su.populationSize
        su.currentGeneration += 1

        #Verifying if plateu was reached 
        if(counter == su.plateau): break
    return last, champion, fitnessHistory

'''
Population initialisation. The array representing a individual has
geneNumber + 1 genes because the last position stores its fitness.
In binary strings, the first bit of each variable stores the signal: 1 if negative,
0 if positive
'''
def init(su):
    su.population = []
    su.varLength = []

    #setting the variables boundaries
    for domain in su.varDomain:
        if(su.geneType == "Binary string"):
            minV = len(bin(abs(domain[0]))) - 1
            maxV = len(bin(abs(domain[1]))) - 1

            lengthAux = max(minV, maxV)
            su.varLength.append(lengthAux)
        else:
            su.varLength.append(1)

    i = 0
    counter = 0 
    '''Initial population starts the proccess with random values'''
    while True:
        if(i == su.populationSize) : break
        if(counter == 2 * su.populationSize):
            return False

        su.population.append([])
        aux = 0
        for domain in su.varDomain:
            if(su.geneType == "Binary string"):
                #generating new decimal individual 
                intVar = rd.randint(domain[0], domain[1])

                #binary casting and formatting
                binaryVar = list(("{0:0" + str(su.varLength[aux]) + "b}").format(intVar))

                su.population[i].extend(binaryVar)
                aux += 1
            elif(su.geneType == "Integer string"):
                intVar = rd.randint(domain[0], domain[1])
                su.population[i].append(intVar)
            else:
                floatVar = rd.uniform(domain[0], domain[1])
                su.population[i].append(round(floatVar, 3))

        su.population[i].append(None)
    
        '''Calculating the fitness of the initial population'''
        fit.getFitness(su.population[i], su)

        if(su.population[i][-1] == None):
            del su.population[i]
            counter += 1
        else:
            counter = 0
            i += 1


    op.sort(su) #Sorting the individuals according to fitnessHistory
    su.currentGeneration = 1
    return True 

def main(geneType, bruteVars, func, task, bruteSetups, nameList, simulationNumber):
    global plotFitnessLog
    global plotGenerationLog
    global log
    
    plotFitnessLog = []
    plotGenerationLog = []
    log = []

    setupList = suManager.createSetups(geneType, bruteVars, func, task, bruteSetups)

    for entry in setupList:
        check = simulation(simulationNumber, entry)

        if not check:
            return False, False, False

    textLog = []
    i = 0
    for entry in setupList:
        lineStr = " " + nameList[i] + "\n\n"

        for line in entry.log:
            lineStr += line 

        textLog.append(lineStr)
        i += 1

    print("Done!")
    return textLog, plotFitnessLog, plotGenerationLog