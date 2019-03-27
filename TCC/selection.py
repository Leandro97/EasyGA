import setup as su 
import operations as op 
import numpy as np

'''Stores the selection roulette'''
probabilityArray = []

'''Initializing selection roulette'''
def init(population):
	global probabilityArray
	previousProbability = 0
	probabilityArray = []
	su.totalFitness = op.getTotalFitness()

	if(su.selection == "roulette"):
		for chrom in list(reversed(population)):
			previousProbability += (chrom[-1] / su.totalFitness) #TODO: PROBLEM IF TOTALfITNESS == 0
			probabilityArray.append(previousProbability)

	#print(probabilityArray)
	#print(su.population)

def selectParent():
	if(su.selection == "roulette"):
		return roulette()

'''Roulette selection'''
def roulette():
	global probabilityArray
	number = np.random.uniform(0,1)
	
	for i in range(len(probabilityArray)):
		if(number < probabilityArray[i]): 
			return i

def tournament():
	pass	