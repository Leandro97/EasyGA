'''
This file contains the informations about the algorithm such as chromosomes
list, population size, number of generations, etc. They will be used throughout 
the algorithm execution.
'''

population = []

#####Chromosome structure#####
geneType = "int" #"float" | "int"
geneNumber = 6
geneMinValue = -5
geneMaxValue = 5
geneInit = {}

#####Fitness Function#####
function = "x1 + x2 + x3 + x4 + x5 + x6"
task = "min" #"max" | "min"

#####Algorithm#####
currentGeneration = 1
populationSize = 20
currentPopulationSize = populationSize
maxGenerations = 50
plateau = 10

crossover = 'onePoint' #'onePoint' | 'twoPoints'
sliceBegin = 2
sliceEnd = 4

selection = 'roulette' #'uniform' | 'roulette' | 'tournament'
mutation = 'uniform' #'uniform' | ??? | ???
mutationRate = 0.25

#####Results#####
saveHeader = True
saveGraphs = True