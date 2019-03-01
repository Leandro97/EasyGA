'''
This file contains the informations about the algorithm such as chromossomes
list, population size, number of generations, etc.
'''

population = []

#####Chromossome structure#####
geneType = "float" #"float" | "int"
geneNumber = 6
geneMinValue = 1
geneMaxValue = 2
geneInit = []

#####Fitness Function#####
function = "x1 + x2 + x3 + x4 + x5 + x6"
task = "max" #"max" | "min" | "target"
target = 0

#####Algorithm#####
currentGeneration = 0
populationSize = 4
maxGeneration = 50
plateau = 20

crossover = 'onePoint' #'onePoint' | 'twoPoints'
sliceBegin = 3
sliceEnd = 3

selection = 'roulette' #'roulette' | 'tournament' | ???
mutation = 'random' #'random' | ??? | ???
mutationRate = 0.2
reinsertParents = True

#####Results#####
experimentName = 'Test'
saveGenerations = True
saveGraphs = True

