'''

Federal University of Alagoas - UFAL
Author: Leandro Martins de Freitas

'''
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

log = [] #Progression of best individual. Its content is shown as a log file
plotFitnessLog = [] #Stores (generation, fitness) pairs for the best individual of each setup

'''Each time the user runs a scenario, this function is called'''
def simulation(tests, su):
    global plotFitnessLog
    global log

    log = []
    simList = []    
    bestIndividual = {}

    rd.seed(a = su.seed)
    np.random.seed(seed = su.seed)
    fitnessSum = 0

    for i in range(tests):
        log.append("\n --------- Simulation #{} ---------\n\n".format(i + 1))

        sim = {} #Auxiliar dictionary for simulations
        sim['id'] = i + 1 #Simulation number
        sim['last'], sim['champion'], sim['history'], sim['average'] = evolve(su) #Last generation achieved, simulation's best individual, progression of best individual

        #sim['last'] == False means that there was some problem in the evolution caused by a invalid function (1/0, for example) or bad domain ([-5, -1] for log(x1), for example) 
        if(sim['last'] == False):
            return False

        fitnessSum += float(str(sim['champion'][-1]))
        simList.append(sim)

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

    rec.record(bestIndividual, log, su) #Saving simulation report
    
    aux = []
    for entry in simList:
        aux.append([entry['last'], entry['champion'][-1]]) #Saving individual progression for graph plotting
    plotFitnessLog.append(aux) 

    return True

'''Saving progression on log file'''
def logWriter(su, champion):
    if(su.geneType != "Binary string"):
        log.append(" Generation " + str(su.currentGeneration) + " - Champion: " + str(champion) + "\n")
    else:
        champion2Int = [int(value) for value in champion[:-1]]
        champion2Int.append(champion[-1])

        begin = 0
        for i in range(len(su.varLength)):           
            #Replacing values
            champion2Int[begin] = '-' if (champion2Int[begin] == 1) else '+'
            end = begin + su.varLength[i]
            begin = end

        log.append(" Generation " + str(su.currentGeneration) + " - Champion: " + str(champion2Int) + "\n")

'''Here all the steps of the algorithm take place'''
def evolve(su):
    global log
    champion = []
    fitnessHistory = [] #Stores a (generation, fitness) pair. It will be used on plotting
    last = 1 #Last generation where the champion changed
    counter = 0 #Counts how many generations the champion remains the same
    check = init(su) #If False, there is some problem on function or domain

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

        #Verifying if plateau was reached 
        if(counter == su.plateau): break

    aux = [value[-1] for value in su.population]
    average = round(sum(aux)/su.populationSize, 3)
    return last, champion, fitnessHistory, average

'''
Population initialisation. The last position stores its fitness.
In binary strings, the first bit of each variable stores the signal: 1 if negative,
0 if positive
'''
def init(su):
    su.population = []
    su.varLength = []

    #Setting the variables boundaries
    for domain in su.varDomain:
        if(su.geneType == "Binary string"):
            minV = len(bin(abs(domain[0]))) - 1
            maxV = len(bin(abs(domain[1]))) - 1

            lengthAux = max(minV, maxV)
            su.varLength.append(lengthAux)
        else:
            su.varLength.append(1)

    i = 0 #Counter for population individuals
    counter = 0 #Validity counter

    '''Initial population starts the proccess with random values'''
    while True:
        #Checking if population number was reached
        if(i == su.populationSize) : 
            break


        if(counter == 2 * su.populationSize): #If the counter doubles the population size, tere is something wrong with the function or domain so the evolution stops
            return False

        su.population.append([])
        aux = 0
        for domain in su.varDomain:
            if(su.geneType == "Binary string"):
                #Generating new decimal individual 
                intVar = rd.randint(domain[0], domain[1])

                #Binary casting and formatting
                binaryVar = list(("{0:0" + str(su.varLength[aux]) + "b}").format(intVar))

                su.population[i].extend(binaryVar)
                aux += 1
            elif(su.geneType == "Integer string"):
                intVar = rd.randint(domain[0], domain[1])
                su.population[i].append(intVar)
            else:
                floatVar = rd.uniform(domain[0], domain[1])
                su.population[i].append(round(floatVar, 3))

        su.population[i].append(None) #Appending fitness value
    
        fit.getFitness(su.population[i], su) #Calculating fitness

        #If the fitness couldn't be calculated, the individual is eliminated and the validity counter is incremented
        if(su.population[i][-1] == None):
            del su.population[i]
            counter += 1
        else:
            counter = 0
            i += 1

    op.sort(su) #Sorting the individuals according to fitnessHistory
    su.currentGeneration = 1

    return True #All individuals were created and evaluated

def prepareForPlot():
    global plotFitnessLog #setup => simulation => generation
    aux = []
    auxDict = {}

    i = 0

    for setup in plotFitnessLog:
        if not i in auxDict:
            auxDict[i] = {}

        for pair in setup:
            if not pair[0] in auxDict[i]:
                auxDict[i][pair[0]] = []
            auxDict[i][pair[0]].append(pair[1])
        i += 1

    parameters = []
    for setup in auxDict:
        x = list(auxDict[setup].keys())
        mean = []
        std = []

        for generation in auxDict[setup]:
            array = auxDict[setup][generation]
            mean.append(np.mean(array))
            std.append(np.std(array))

        x2 = x.copy()

        x, mean = zip(*sorted(zip(x, mean)))
        x2, std = zip(*sorted(zip(x2, std)))

        newList = []
        newList.append((x, mean, std))
        print(newList)
        parameters.append(newList)

    plotFitnessLog = parameters

"""This function receives the parameters provided by the user, performs the evolutionary process and returns the results"""
def main(geneType, varList, func, task, bruteSetups, nameList, simulationNumber):
    global plotFitnessLog
    global log
    
    plotFitnessLog = []
    log = []

    setupList = suManager.createSetups(geneType, varList, func, task, bruteSetups)

    for entry in setupList:
        check = simulation(simulationNumber, entry)

        #If there is any problem the function returns False
        if not check:
            return False, False

    prepareForPlot()
    textLog = []
    i = 0

    #Setting up the text log that will be displayed at the GUI
    for entry in setupList:
        lineStr = " " + nameList[i] + "\n\n"

        for line in entry.log:
            lineStr += line 

        textLog.append(lineStr)
        i += 1

    print("Done!")

    return textLog, plotFitnessLog