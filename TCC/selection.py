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
	probabilityArray = []
	aux = [] #Auxiliar array. It stores the fitness of the population
	newArray = []

	for chrom in population:
		aux.append(chrom[-1])
	
	minV, maxV = min(aux), max(aux)
	#Normalazing fitness
	for fit in aux:
		if(minV != maxV):
				newValue = (fit - minV) / (maxV- minV) if (su.task == "min") else (fit - maxV) / (minV- maxV)
		else:
			newValue = 1.0
		newArray.append(round(newValue, 2))

	#Calculating selection probability 
	probabilityArray.append(0.0)
	for i in range(1, su.populationSize):
		probabilityArray.append(round(newArray[i] + probabilityArray[i - 1], 2))

	minV, maxV = min(probabilityArray), max(probabilityArray)
	#Normalizing probabilities
	for i in range(su.populationSize):
		probabilityArray[i] = round((probabilityArray[i] - minV) / (maxV - minV), 2)
		probabilityArray[i] = 0.1 if (probabilityArray[i] == 0) else probabilityArray[i]

'''Roulette selection'''
def roulette():
	global probabilityArray
	chance = np.random.uniform(0,1)
	populationSize = len(probabilityArray)

	#If the random number is lesser than the probability, the chromosome is chosen 
	for i in range(populationSize):
		if chance < probabilityArray[i]:
			return populationSize - i - 1
	return 0

'''Tournament selection'''
def tournament():
	pass	