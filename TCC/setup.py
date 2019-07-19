'''
This file contains the informations about the algorithm such as chromosomes
list, population size, number of generations, etc. They will be used throughout 
the algorithm execution.
'''
from dataclasses import dataclass

@dataclass
class Setup:
	seed: int = None
	enabled: bool = True
	population = None
	varDomain = None #this array stores the domain of each variable in the form [minValue, maxValue]. 
	varLength = None #this array stores the maximum lenght of the variable binary representation 
	
	#####Chromosome structure#####
	geneType: str = "int" #"float" | "int" | "bin"
	varMinValue: int = -10
	varMaxValue: int = 20
	varDomain = None

	#####Fitness Function#####
	#function: str = "x1 + (2*x1 - 25)**2"
	#function: str = "x1 - x2 + x3 - x4**2 + 3*(x5 - x6)"
	function: str = "x1 - x2"

	task: str = "max" #"max" | "min"

	#####Algorithm#####
	currentGeneration: int = 1
	populationSize: int = 6
	currentPopulationSize: int = populationSize
	maxGenerations: int = 20
	plateau: int = 20

	crossover: str = "twoPoint" #"onePoint" | "twoPoint"
	sliceBegin: int = 2
	sliceEnd: int = 4

	selection: str = "roulette" #"uniform" | "roulette" | "tournament"
	mutation: str = "uniform" #"uniform" | ??? | ???
	mutationRate: float = 0.15

	#####Results#####
	bestFitness: float = 0
	saveLog: bool = False