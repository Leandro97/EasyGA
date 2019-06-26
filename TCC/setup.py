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
	
	#####Chromosome structure#####
	geneType: str = "int" #"float" | "int" | "bin"
	geneNumber: int = 6
	varMinValue: int = -10
	varMaxValue: int = 20

	#####Fitness Function#####
	#function: str = "x1 + (2*x1 - 25)**2"
	function: str = "x1 - x2 + x3 - x4**2 + 3*(x5 - x6)"
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
	showGraphs: bool = True
	saveLog: bool = False