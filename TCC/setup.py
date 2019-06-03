'''
This file contains the informations about the algorithm such as chromosomes
list, population size, number of generations, etc. They will be used throughout 
the algorithm execution.
'''

population = []
seed = None
#####Chromosome structure#####
geneType = "int" #"float" | "int"
geneNumber = 6
geneMinValue = -10
geneMaxValue = 10

#####Fitness Function#####
#function = "x1**3 + (x2 + x3 + x4) * (x5 - x6 + 10)"
function = "x1 + x2 + x3 + x4 + x5 + x6"
task = "max" #"max" | "min"

#####Algorithm#####
currentGeneration = 1
populationSize = 20
#populationSize = 6
currentPopulationSize = populationSize
maxGenerations = 50
#maxGenerations = 20
plateau = 20
elitism = True

crossover = 'twoPoint' #'onePoint' | 'twoPoint'
sliceBegin = 2
sliceEnd = 4

selection = 'roulette' #'uniform' | 'roulette' | 'tournament'
mutation = 'uniform' #'uniform' | ??? | ???
mutationRate = 0.15

#####Results#####
saveHeader = False
saveGraphs = True
saveLog = True