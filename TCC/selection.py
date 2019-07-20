import operations as op 
import numpy as np
import random as rd

'''Stores the selection roulette'''
probabilityArray = []

'''Selection interface'''
def selectParent(su):
	if(su.selection == "uniform"):
		return np.random.randint(0, su.populationSize)
	elif(su.selection == "roulette"):
		return roulette(su)
	elif(su.selection == "tournament"):
		return tournament()

'''Initialising selection roulette'''
def init(su):
	#This array stores the probability of choosing a individual 
	global probabilityArray
	probabilityArray = [0.1]
	
	if su.task == "min":
		minV, maxV = int(su.population[0][-1]), int(su.population[-1][-1])
	else:
		minV, maxV = int(su.population[-1][-1]), int(su.population[0][-1])

	#Normalizing fitness
	for i in range(1, su.populationSize):
		value = int(su.population[i][-1])

		if(minV != maxV):
			newValue = (value - minV) / (maxV - minV) if (su.task == "min") else (value - maxV) / (minV - maxV)
		else:
			newValue = 1.0
		#Calculating selection probability 
		probabilityArray.append(round(newValue + probabilityArray[i - 1], 2))

	#Normalizing probabilities
	minV, maxV = probabilityArray[0], probabilityArray[-1]

	for i in range(su.populationSize):
		if(minV == maxV):
			probabilityArray[i] = 0.5
		else:	
			probabilityArray[i] = round((probabilityArray[i] - minV) / (maxV - minV), 2)
			probabilityArray[i] = 0.001 if (probabilityArray[i] == 0) else probabilityArray[i]

'''Roulette selection'''
def roulette(su):
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