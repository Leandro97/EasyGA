'''
Main file. here all the steps of the algorithm are done.
'''
import setup as su
from setup import *
import fitness as fit
import operations as op
import selection as sel 
import datetime

import numpy as np

file = []

def setName(now):
    day = '{:02d}'.format(now.day)
    month = '{:02d}'.format(now.month)
    year = str(now.year)
    date = day + '-' + month + '-' + year

    hour = '{:02d}'.format(now.hour)
    minute = '{:02d}'.format(now.minute)
    time = hour + ':' + minute


    return date + '.' + time + '.txt'

'''
Population initialization. The array representing a individual has
geneNumber + 1 genes because the last position stores its fitness
'''
def init():
    #Initializing fitness function
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

    su.population = op.order(su.population) #Ordering the individuals according to fitness
    su.totalFitness = op.getTotalFitness() #Getting the sum of population's fitness
    su.currentGeneration = 1
    su.champion = []

aux = 0

'''Here all the steps of the algorithm take place'''
def evolve():
    global aux
    last = 0 #Last generation where the champion changed
    counter = 0 #Counts how many generations the champion remains the same
    init()

    while (su.currentGeneration <= su.maxGenerations):
        if len(su.champion) == 0:
            su.champion = su.population[0]

        op.crossover(su.population)
        su.population = op.order(su.population)

        #Verifying if champion changed
        if(su.population[0][-1] == su.champion[-1]):
            counter += 1
        else:
            counter = 0
            su.champion = su.population[0]
            file.write("Generation " + str(su.currentGeneration) + " - Champion: " + str(su.champion) + "\n")
            last = su.currentGeneration
        
        #Population returns to its initial size
        su.population = su.population[:su.populationSize]
        su.currentPopulationSize = su.populationSize
        su.currentGeneration += 1

        #Verifying if max generation number was reached 
        if(counter == su.plateau ): break

        #print("###")
    file.write("\n")
    return last

'''Each time the user runs a scenario, this function is called'''
def simulation(tests):
    global aux
    global file
    now = datetime.datetime.now()
    file = open(setName(now), "a") 

    for i in range(tests):
        file.write("----- Simulation #{} -----\n".format(i + 1))
        aux += evolve()

simulation(1)

#file.write(str(aux/tests) + "\n")
print(su.population[0])