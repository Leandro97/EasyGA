import setup as su 
import operations as op 
import numpy as np
import random as rd

'''Stores the selection roulette'''
probabilityArray = []

'''Initialising selection roulette'''
def init(population):
	global probabilityArray
	previousProbability = 0
	probabilityArray = []
	totalFitness = op.getTotalFitness()

	if(su.selection == "roulette"):
		for chrom in list(reversed(population)):
			if (totalFitness != 0):
				previousProbability += (chrom[-1] / totalFitness) 
				probabilityArray.append(previousProbability)
			else:
				probabilityArray.append(0.5)

	#normalizing probabilities in the [0.0, 1.0] interval
	vmin, vmax = min(probabilityArray), max(probabilityArray)
	for i, val in enumerate(probabilityArray):
		if vmin != vmax:
			probabilityArray[i] = (val - vmin) / (vmax - vmin)
		else:
			probabilityArray[i] = 1.0

def selectParent():
	if(su.selection == "uniform"):
		return np.random.randint(0, su.populationSize)
	elif(su.selection == "tournament"):
		return tournament()
	elif(su.selection == "roulette"):
		return roulette()

'''Roulette selection'''
def roulette():
	global probabilityArray
	chance = np.random.uniform(0,1.1)
	
	print(probabilityArray)
	for i in range(len(probabilityArray)):
		if(probabilityArray[i] > chance):
			print(chance) 
			return i

	print(chance)
	return len(probabilityArray) - 1

'''Tournament selection'''
def tournament():
	pass	