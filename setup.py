'''
This file contains the informations about the algorithm such as chromosomes
list, population size, number of generations, etc. They will be used throughout 
the algorithm execution.
'''
class Setup():
	seed = None
	population = []
	varDomain = [] #this array stores the domain of each variable in the form [minValue, maxValue]. 
	varLength = [] #this array stores the maximum lenght of each variable 
	
	#####Chromosome structure#####
	geneType = "Binary srting" #"Float string" | "Integer string" | "Binary string"
	varDomain = None

	#####Fitness Function#####
	#function = "x1 - x2 + x3 - x4**2 + 3*(x5 - x6)"
	function = "x1"
	task = "max" #"max" | "min"

	#####Algorithm#####
	currentGeneration = 1
	populationSize = 10
	currentPopulationSize = 1
	maxGenerations = 50
	plateau = 20

	crossover = "Uniform" #"One point" | "Two Points" | "Uniform"
	selection = "Roulette" #"Roulette" | "Tournament" | ?
	mutation = "Uniform" #"Flip" | "Uniform" | "Non-uniform"
	mutationRate: float = 0.15

	#####Results#####
	bestFitness = 0
	saveLog = True
	log = []