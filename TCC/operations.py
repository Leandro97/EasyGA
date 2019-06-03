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
	return np.concatenate([parent1[0:point], parent2[point:]]), np.concatenate([parent2[0:point], parent1[point:]])

'''Two point crossover'''
def twoPoint(parent1, parent2):
	begin = su.sliceBegin
	end = su.sliceEnd

	return np.concatenate([parent1[0:begin - 1], parent2[begin - 1:end], parent1[end:]]), np.concatenate([parent2[0:begin - 1], parent1[begin - 1:end], parent2[end:]])

'''Mutation operator'''
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
	newPopulation = []

	#Initialising roullete
	if su.selection == 'roulette': 
		sel.init(su.population)

	#print(su.population)
	#New childs are born until the current size of the population is equal to two times the initial size
	while(su.currentPopulationSize <= 2 * su.populationSize):
		#Choosing first parent
		index1 = sel.selectParent()
		parent1 = population[index1]
		#print("Parent #1: ", index1, parent1)

		#The loop is necessary to prevent the two parents of being the same
		while(True):
			#Choosing second parent
			index2 = sel.selectParent()

			if(index1 != index2): 
				parent2 = population[index2]
				break
		#print("Parent #2: ", index2, parent2)
		#print("***")
		#print(su.population[index1], su.population[index2])

		'''Childs being born and mutated'''
		child1, child2 = onePoint(parent1, parent2) if su.sliceBegin == su.sliceEnd else twoPoint(parent1, parent2)
		child1, child2 = mutation(child1), mutation(child2)
		child1[-1], child2[-1] = fit.getFitness(child1), fit.getFitness(child2) #Calculatin its fitness

		if su.geneType == 'float':
			child1, child2 = [round(value, 2) for value in child1], [round(value, 2) for value in child2] #rounding values

		#Adding child to population 
		#su.population = np.append(su.population, [child1, child2], axis = 0)
		newPopulation.append(child1)
		newPopulation.append(child2)
		su.currentPopulationSize += 2
	
	#saving best individual of current generation
	if(su.elitism):
		su.population = np.append(newPopulation, [su.population[0]], axis = 0)
	#print(su.population)
	#print('######')

'''Sorting population in decrescent order, acording to the object task'''
def sort(population):
	if(su.task == 'max'):	
		return np.asarray(sorted(su.population, key=lambda x: x[-1], reverse=True))[0:su.populationSize]
	else:	 
		return np.asarray(sorted(su.population, key=lambda x: x[-1], reverse=False))[0:su.populationSize]