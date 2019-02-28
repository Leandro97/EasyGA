'''
This file contains the informations about the algorithm such as chromossomes
list, population size, number of generations, etc.
'''

population = [[1,1,1,1,1,1], [2,2,2,2,2,2], [3,3,3,3,3,3], [4,4,4,4,4,4]]

#####Chromossome structure#####
geneType = "binaryChain" #"binaryChain" | "floatChain" | "intChain"
geneNumber = 6
geneMinValue = 0
geneMaxValue = 1
geneInit = []

#####Fitness Function#####
function = "x1 + x2 + x3 + x4 + x5 + x6"
task = "max" #"max" | "min" | "target"
target = 0

#####Algorithm#####
populationSize = 4
maxGeneration = 50
currentgeneration = 1
