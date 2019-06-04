import setup as su 
import operations as op 
import numpy as np
import random as rd

'''Stores the selection roulette'''
probabilityArray = []

def selectParent():
	if(su.selection == "uniform"):
		return np.random.randint(0, su.populationSize)
	elif(su.selection == "roulette"):
		return roulette()
	elif(su.selection == "tournament"):
		return tournament()

'''Initialising selection roulette'''
def init(population):
	#This array stores the probability of choosing a individual 
	global probabilityArray
	probabilityArray = [0.1]
	
	if su.task == 'min':
		minV, maxV = population[0][-1], population[-1][-1]
	else:
		minV, maxV = population[-1][-1], population[0][-1]

	#Normalizing fitness
	for i in range(1, su.populationSize):
		if(minV != maxV):
			newValue = (population[i][-1] - minV) / (maxV - minV) if (su.task == "min") else (population[i][-1] - maxV) / (minV - maxV)
		else:
			newValue = 1.0
		#Calculating selection probability 
		probabilityArray.append(round(newValue + probabilityArray[i - 1], 2))

	#Normalizing probabilities
	minV, maxV = probabilityArray[0], probabilityArray[-1]
	for i in range(su.populationSize):
		probabilityArray[i] = round((probabilityArray[i] - minV) / (maxV - minV), 2)
		probabilityArray[i] = 0.1 if (probabilityArray[i] == 0) else probabilityArray[i]
		
'''Roulette selection'''
def roulette():
	global probabilityArray
	chance = np.random.uniform(0,1)

	#If the random number is lesser than the probability, the chromosome is chosen 
	for i in range(su.populationSize):
		if chance < probabilityArray[i]:
			return su.populationSize - i - 1
	return 0

'''Tournament selection'''
def tournament():
	pass	