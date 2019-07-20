import fitness as fit
import selection as sel
import numpy as np
import random as rd

#COMO LIDAR COM INDIVÍDUOS INVÁLIDOS?!?!

'''One point crossover'''
def onePoint(parent1, parent2, su):
	point = rd.randint(0, sum(su.varLength))

	child1 = parent1[0:point]
	child1.extend(parent2[point:])

	child2 = parent2[0:point]
	child2.extend(parent1[point:])
	return child1, child2

'''Two point crossover'''
def twoPoint(parent1, parent2, su):
	a = rd.randint(0, sum(su.varLength))
	b = rd.randint(0, sum(su.varLength))

	begin = min(a, b)
	end = max(a, b)

	return np.concatenate([parent1[0:begin - 1], parent2[begin - 1:end], parent1[end:]]), np.concatenate([parent2[0:begin - 1], parent1[begin - 1:end], parent2[end:]])
	
'''Mutation operator'''
def mutation(chrom, su):
	for i in range(len(chrom) - 1):
		k = rd.random()
		if(k <= su.mutationRate):
			chrom[i] = '0' if chrom[i] == '1' else '1'

	fit.getFitness(chrom, su)
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

		#Choosing second parent
		index2 = sel.selectParent(su)

		if(index1 == index2): 
			index2 += 1
			
		parent2 = su.population[index2]

		#Childs being born and mutated
		child1, child2 = onePoint(parent1, parent2, su) if su.crossover == "onePoint" else twoPoint(parent1, parent2, su)

		mutation(child1, su)
		mutation(child2, su)
		#child1, child2 = fit.getFitness(child1, su), fit.getFitness(child2, su) #Calculating its fitness

		if su.geneType == "float":
			child1, child2 = [round(value, 2) for value in child1], [round(value, 2) for value in child2] #rounding values

		#Adding child to population 
		#su.population = np.append(su.population, [child1, child2], axis = 0)
		newPopulation.append(child1)
		newPopulation.append(child2)
		su.currentPopulationSize += 2
	
	#Saving best individual of current generation
	best = su.population[0]
	su.population = newPopulation
	su.population.append(best)
	#print('######')

'''Sorting population in decrescent order of fitness, acording to the object task'''
def sort(su):
	if(su.task == "max"):
		su.population.sort(key=lambda x: int(x[-1]), reverse = True)	
	else:	
		su.population.sort(key=lambda x: x[-1], reverse = False)	
	
	return su.population[0:su.populationSize]