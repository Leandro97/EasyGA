import setup as su
import fitness as fit
from setup import currentPopulationSize, sliceBegin, sliceEnd
import numpy as np
import random as rd

def onePoint(parent1, parent2):
	point = su.sliceBegin
	return np.concatenate([parent1[0:point], parent2[point:]])

def twoPoint(parent1, parent2):
	begin = su.sliceBegin
	end = su.sliceEnd
	return np.concatenate([parent1[0:begin], parent2[begin:end+1], parent1[end+1:]])

def crossover(population):
	while(su.currentPopulationSize <= 2 * su.populationSize - 1):
		index1 = rd.randint(0, su.populationSize - 1)
		parent1 = population[index1]

		while(True):
			index2 = rd.randint(0, su.populationSize - 1)
			if(index1 != index2): 
				parent2 = population[index2]
				break
		
		child1 = onePoint(parent1, parent2) if su.sliceBegin == su.sliceEnd else twoPoint(parent1, parent2)
		child1 = mutation(child1)
		child1[-1] = fit.getFitness(child1)

		su.population = np.append(su.population, [child1], axis = 0)
		su.currentPopulationSize += 1

		if(su.currentPopulationSize != 2 * su.populationSize):
			child2 = onePoint(parent2, parent1) if su.sliceBegin == su.sliceEnd else twoPoint(parent2, parent1)
			child2 = mutation(child2)
			child2[-1] = fit.getFitness(child2)

			su.population = np.append(su.population, [child2], axis = 0)
			su.currentPopulationSize += 1

def mutation(chrom):
	for i in range(len(chrom)):
		k = rd.random()
		if(k <= su.mutationRate):
			if (su.geneType == 'int'): 
		   		chrom[i] = rd.randint(su.geneMinValue, su.geneMaxValue + 1)
			else:
		   		chrom[i] = rd.unform(su.geneMinValue, su.geneMaxValue)
	return chrom