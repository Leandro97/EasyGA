import fitness as fit
import selection as sel
import numpy as np
import random as rd

'''One point crossover'''
def onePoint(parent1, parent2, su):
	point = su.sliceBegin
	return np.concatenate([parent1[0:point], parent2[point:]]), np.concatenate([parent2[0:point], parent1[point:]])

'''Two point crossover'''
def twoPoint(parent1, parent2, su):
	begin = su.sliceBegin
	end = su.sliceEnd

	return np.concatenate([parent1[0:begin - 1], parent2[begin - 1:end], parent1[end:]]), np.concatenate([parent2[0:begin - 1], parent1[begin - 1:end], parent2[end:]])

'''Mutation operator'''
def mutation(chrom, su):
	for i in range(len(chrom)):
		k = rd.random()
		if(k <= su.mutationRate):
			num = min(su.varMaxValue, max(su.varMinValue, rd.gauss(0, 5)))

			if (su.geneType == "int"): 
		   		chrom[i] = rd.randint(su.varMinValue, su.varMaxValue)
			elif (su.geneType == "float"):
		   		chrom[i] = rd.uniform(su.varMinValue, su.varMaxValue)
			else:
		   		chrom[i] = 0 if chrom[i] == 1 else 1
	return chrom

'''Crossover management'''
def crossover(su):
	newPopulation = []

	#Initializing roullete
	if su.selection == "roulette": 
		sel.init(su)

	#print(su.population)
	#New childs are born until the current size of the population is equal to two times the initial size
	while(su.currentPopulationSize <= 2 * su.populationSize):
		#Choosing first parent
		index1 = sel.selectParent(su)
		parent1 = su.population[index1]
		#print("Parent #1: ", index1, parent1)

		#The loop is necessary to prevent the two parents of being the same
		while(True):
			#Choosing second parent
			index2 = sel.selectParent(su)

			if(index1 != index2): 
				parent2 = su.population[index2]
				break
		#print("Parent #2: ", index2, parent2)
		#print("***")
		#print(su.population[index1], su.population[index2])

		#Childs being born and mutated
		child1, child2 = onePoint(parent1, parent2, su) if su.sliceBegin == su.sliceEnd else twoPoint(parent1, parent2, su)
		child1, child2 = mutation(child1, su), mutation(child2, su)
		child1, child2 = fit.getFitness(child1, su), fit.getFitness(child2, su) #Calculating its fitness

		if su.geneType == "float":
			child1, child2 = [round(value, 2) for value in child1], [round(value, 2) for value in child2] #rounding values

		#Adding child to population 
		#su.population = np.append(su.population, [child1, child2], axis = 0)
		newPopulation.append(child1)
		newPopulation.append(child2)
		su.currentPopulationSize += 2
	
	#Saving best individual of current generation
	su.population = np.append(newPopulation, [su.population[0]], axis = 0)
	#print(su.population)
	#print('######')

'''Sorting population in decrescent order of fitness, acording to the object task'''
def sort(su):
	if(su.task == "max"):	
		return np.asarray(sorted(su.population, key=lambda x: x[-1], reverse=True))[0:su.populationSize]
	else:	 
		return np.asarray(sorted(su.population, key=lambda x: x[-1], reverse=False))[0:su.populationSize]