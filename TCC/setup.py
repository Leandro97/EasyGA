'''
This file contains the informations about the algorithm such as chromosomes
list, population size, number of generations, etc. They will be used throughout 
the algorithm execution.
'''
from dataclasses import dataclass

@dataclass
class Setup:
	seed: int = None
	population = None
	varDomain = None #this array stores the domain of each variable in the form [minValue, maxValue]. 
	varLength = None #this array stores the maximum lenght of each variable 
	
	#####Chromosome structure#####
	geneType: str = "int" #"float" | "int" | "bin"
	varDomain = None

	#####Fitness Function#####
	#function: str = "x1 - x2 + x3 - x4**2 + 3*(x5 - x6)"
	function: str = "x1"
	task: str = "max" #"max" | "min"

	#####Algorithm#####
	currentGeneration: int = 1
	populationSize: int = 50
	currentPopulationSize: int = 1
	maxGenerations: int = 100
	plateau: int = 20

	crossover: str = "uniform" #"onePoint" | "twoPoint" | "uniform"
	selection: str = "roulette" #"roulette" |     "uniform" | "tournament"
	mutation: str = "uniform" #"flip" | ??? | ???
	mutationRate: float = 0.15

	#####Results#####
	bestFitness: float = 0
	saveLog: bool = False