'''
This file contains the informations about the algorithm such as chromosomes
list, population size, number of generations, etc. They will be used throughout 
the algorithm execution.
'''

population = []

#####Chromossome structure#####
geneType = "int" #"float" | "int"
geneNumber = 6
geneMinValue = 0
geneMaxValue = 5
geneInit = {}

#####Fitness Function#####
function = "x1 + x2 + x3 + x4 + x5 + x6"
task = "max" #"max" | "min" | "target"
target = 0
totalFitness = 0

#####Algorithm#####
currentGeneration = 1
populationSize = 4
currentPopulationSize = 4
maxGenerations = 50
plateau = 20
champion = 0

crossover = 'onePoint' #'onePoint' | 'twoPoints'
sliceBegin = 2
sliceEnd = 4

selection = 'roulette' #'roulette' | 'tournament' | ???
mutation = 'uniform' #'uniform' | ??? | ???
mutationRate = 0.25
reinsertParents = True

#####Results#####
experimentName = 'Test'
saveGenerations = False
saveGraphs = False