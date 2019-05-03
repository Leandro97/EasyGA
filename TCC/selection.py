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
				previousProbability += (chrom[-1] / totalFitness) #TODO: PROBLEM IF TOTALFITNESS == 0
				probabilityArray.append(previousProbability)
			else:
				probabilityArray.append(0.5)

	print(probabilityArray)
	#print(su.population)

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
	number = np.random.uniform(0,1.1)
	
	for i in range(len(probabilityArray)):
		if(number < probabilityArray[i]): 
			return i

	return len(probabilityArray) - 1

'''Tournament selection'''
def tournament():
	pass	