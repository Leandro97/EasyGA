import operations as op 
import numpy as np
import random as rd

'''Stores the selection roulette'''
probabilityArray = []
cumulativeProbability = 0

'''Selection interface'''
def selectParent(su):
	if(su.selection == "Roulette"):
		initSelection(su)
		return roulette(su)
	elif(su.selection == "Tournament"):
		return tournament(su)
	else:
		#initSelection(su)
		return rank(su)

'''Initialising probability array for roulette and rank selections'''
def initSelection(su):
	#This array stores the probability of choosing a individual 
	global probabilityArray
	global cumulativeProbability

	probabilityArray = []
	
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

		newValue = 0.01 if newValue == 0 else newValue
		#Calculating selection probability 
		probabilityArray.append(round(newValue, 2))

	cumulativeProbability = sum(probabilityArray)

'''Roulette selection'''
def roulette(su):
	global probabilityArray
	global cumulativeProbability

	probabilityArray = [value/cumulativeProbability for value in probabilityArray] if cumulativeProbability != 0 else [1/len(probabilityArray) for value in probabilityArray]
	chance = np.random.uniform(0, probabilityArray[-1])

	#If the random number is lesser than the probability, the chromosome is chosen 
	for i in range(su.populationSize):
		if chance < probabilityArray[i]:
			return i
	return 0

'''Rank selection'''
def rank(su):
	probabilityArray = []

	for i in range(len(su.population)):
		probabilityArray.append(su.population[i][-1] / (i + 1)) 

	chance = np.random.uniform(0, probabilityArray[0])

	#If the random number is lesser than the probability, the chromosome is chosen 
	for i in reversed(range(su.populationSize)):
		if chance < probabilityArray[i]:
			return i
	return 0

'''Tournament selection'''
def tournament(su):
	index1 = rd.randint(0, su.populationSize - 1)
	index2 = rd.randint(0, su.populationSize - 1)

	if(su.task == "max"):
		if(su.population[index1][-1] < su.population[index2][-1]):
			aux = index1
			index1 = index2
			index2 = aux
	else:
		if(su.population[index1][-1] > su.population[index2][-1]):
			aux = index1
			index1 = index2
			index2 = aux

	chance = rd.uniform(0, 1)

	if(chance <= .75):
		return index1
	else:
		return index2	
