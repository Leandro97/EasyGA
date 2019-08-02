import fitness as fit
import selection as sel
import numpy as np
import random as rd
	
'''Mutation operator'''
def mutation(chrom, su):
	if(su.mutation == "flip"):
		return flipMutation(chrom, su)
	elif(su.mutation == "uniform"):
		return uniformMutation(chrom, su)

	fit.getFitness(chrom, su) #test
	return chrom #test

def flipMutation(chrom, su):
	for i in range(len(chrom) - 1):
		rand = rd.random()
		if(rand <= su.mutationRate):
			chrom[i] = '0' if chrom[i] == '1' else '1'

	fit.getFitness(chrom, su)
	return chrom

def uniformMutation(chrom, su):
	i = 0

	for domain in su.varDomain:
		rand = rd.random()
		if(rand <= su.mutationRate):
			if su.geneType == "float":
				chrom[i] = rd.uniform(domain[0], domain[1])
			else:
				chrom[i] = rd.randint(domain[0], domain[1])
		i += 1

	fit.getFitness(chrom, su)
	return chrom

'''Crossover management'''
def crossover(su):
	newPopulation = []

	#Initializing roullete
	if su.selection == "roulette": 
		sel.init(su)

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
		if su.crossover == "onePoint":
			child1, child2 = onePointCrossover(parent1, parent2, su)
		elif su.crossover == "twoPoint":
			child1, child2 = twoPointCrossover(parent1, parent2, su)
		else:
			child1, child2 = uniformCrossover(parent1, parent2, su)

		mutation(child1, su)
		mutation(child2, su)

		if su.geneType == "float":
			child1, child2 = [round(float(value), 2) for value in child1], [round(float(value), 2) for value in child2] #rounding values

		#Adding child to population 
		newPopulation.append(child1)
		newPopulation.append(child2)
		su.currentPopulationSize += 2

	#Saving best individual of current generation
	best = su.population[0]
	su.population = newPopulation
	su.population.append(best)
	#print('######')

'''One point crossover'''
def onePointCrossover(parent1, parent2, su):
	point = rd.randint(0, sum(su.varLength))
	
	child1 = parent1[0:point]
	child1.extend(parent2[point:])

	child2 = parent2[0:point]
	child2.extend(parent1[point:])

	return child1, child2

'''Two point crossover'''
def twoPointCrossover(parent1, parent2, su):
	a = rd.randint(0, sum(su.varLength))
	b = rd.randint(1, sum(su.varLength))

	begin, end = min(a, b), max(a, b)

	child1 = parent1[0:begin]
	child1.extend(parent2[begin:end])
	child1.extend(parent1[end:])

	child2 = parent2[0:begin]
	child2.extend(parent1[begin:end])
	child2.extend(parent2[end:])

	return child1, child2

def uniformCrossover(parent1, parent2, su):
	child1 = []
	child2 = []

	for i in range(len(parent1)):
		rand = rd.random()

		if(rand <= 0.5):
			child1.append(parent1[i])
			child2.append(parent2[i])
		else:
			child1.append(parent2[i])
			child2.append(parent1[i])

	#print(child1)
	#print(child2)
	#print("###")
	return child1, child2

'''Sorting population in decrescent order of fitness, acording to the object task'''
def sort(su):
	if(su.task == "max"):
		su.population.sort(key=lambda x: float(x[-1]), reverse = True)	
	else:	
		su.population.sort(key=lambda x: float(x[-1]), reverse = False)	
	
	return su.population[0:su.populationSize]