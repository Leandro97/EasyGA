'''
This file contains the informations about the algorithm such as chromosomes
list, population size, number of generations, etc. They will be used throughout 
the algorithm execution.
'''
class Setup():
	seed = None
	population = []
	varDomain = [] #This array stores the domain of each variable in the form [minValue, maxValue]. 
	varLength = [] #This array stores the maximum lenght of each variable 
	
	#####Chromosome structure#####
	geneType = "Binary srting" #"Binary string" | "Integer string" | "Float string"
	varDomain = None

	#####Fitness Function#####
	function = "x1"
	task = "max" #"max" | "min"

	#####Algorithm#####
	currentGeneration = 1
	populationSize = 10
	currentPopulationSize = 1
	maxGenerations = 50
	plateau = 20

	crossover = "Uniform" #"One point" | "Two Points" | "Uniform"
	selection = "Roulette" #"Roulette" | "Tournament" | "Rank"
	mutation = "Uniform" #"Flip" | "Uniform" | "Non-uniform"
	crossoverProb: float = 0.9
	mutationRate: float = 0.01