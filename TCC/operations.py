import setup as su
import fitness as fit
import selection as sel
import numpy as np
import random as rd

'''Calculates the total fitness of population'''
def getTotalFitness():
	aux = 0

	for chrom in su.population:
		aux += chrom[-1]

	return aux

'''One point crossover'''
def onePoint(parent1, parent2):
	point = su.sliceBegin
	return np.concatenate([parent1[0:point], parent2[point:]])

'''Two point crossover'''
def twoPoint(parent1, parent2):
	begin = su.sliceBegin
	end = su.sliceEnd

	return np.concatenate([parent1[0:begin], parent2[begin:end+1], parent1[end+1:]])

'''Mutation operators'''
def mutation(chrom):
	for i in range(len(chrom)):
		k = rd.random()
		if(k <= su.mutationRate):
			num = min(su.geneMaxValue, max(su.geneMinValue, rd.gauss(0, 5)))

			if (su.geneType == 'int'): 
		   		chrom[i] = rd.randint(su.geneMinValue, su.geneMaxValue)
			else:
		   		chrom[i] = rd.uniform(su.geneMinValue, su.geneMaxValue)
	return chrom

'''Where the crossover is managed'''
def crossover(population):
	#Initializing roullete
	if(su.selection == "roulette"): sel.init(su.population)

	#New childs are born until the current size of the population is equal to two times the initial size
	while(su.currentPopulationSize <= 2 * su.populationSize - 1):
		#Choosing first parent
		index1 = sel.selectParent()
		parent1 = population[index1]

		#The loop is necessary to prevent the two parents of being the same
		while(True):
			#Choosing second parent
			index2 = sel.selectParent()

			if(index1 != index2): 
				parent2 = population[index2]
				break
		
		#print(su.population[index1], su.population[index2])

		'''First child being born and mutated (acording to mutation rate)'''
		child1 = onePoint(parent1, parent2) if su.sliceBegin == su.sliceEnd else twoPoint(parent1, parent2)
		child1 = mutation(child1)
		child1[-1] = fit.getFitness(child1) #Calculatin its fitness

		#Adding child to population 
		su.population = np.append(su.population, [child1], axis = 0)
		su.currentPopulationSize += 1

		#Verifying population size
		if(su.currentPopulationSize != 2 * su.populationSize):
			'''Second child being born and mutated (acording to mutation rate)'''
			child2 = onePoint(parent2, parent1) if su.sliceBegin == su.sliceEnd else twoPoint(parent2, parent1)
			child2 = mutation(child2)
			child2[-1] = fit.getFitness(child2)

			#Adding child to population
			su.population = np.append(su.population, [child2], axis = 0)
			su.currentPopulationSize += 1
			
	#print(su.population)
	#print('######')

'''Ordering population in decrescent order, acording to the object task'''
def order(population):
	if(su.task == 'max'):	
		return np.asarray(sorted(su.population, key=lambda x: x[-1], reverse=True))
	else:	 
		return np.asarray(sorted(su.population, key=lambda x: x[-1], reverse=False))