import fitness as fit
import selection as sel
import numpy as np
import random as rd
	
'''Mutation operator'''
def mutation(chrom, su):
	if(su.mutation == "Flip"):
		return flipMutation(chrom, su)
	elif(su.mutation == "Uniform"):
		return uniformMutation(chrom, su)
	else:
		return nonUniformMutation(chrom, su)

'''Used only on binary representations'''
def flipMutation(chrom, su):
	for i in range(len(chrom) - 1):
		rand = rd.random()
		if(rand <= su.mutationRate):
			chrom[i] = '0' if chrom[i] == '1' else '1' #Bit inversion

	return fit.getFitness(chrom, su)

'''Used on float and integer representations'''
def uniformMutation(chrom, su):
	i = 0

	for domain in su.varDomain:
		rand = rd.random()
		if(rand <= su.mutationRate):
			if su.geneType == "Float string":
				if(rd.random() <= .5):
					chrom[i] += rd.uniform(domain[0], domain[1])
				else:
					chrom[i] -= rd.uniform(domain[0], domain[1])
			else:
				if(rd.random() <= .5):
					chrom[i] += rd.randint(domain[0], domain[1])
				else:
					chrom[i] -= rd.randint(domain[0], domain[1])
		i += 1

	return fit.getFitness(chrom, su)

'''Used on float and integer representations'''
def nonUniformMutation(chrom, su):
	i = 0

	for domain in su.varDomain:
		rand = rd.random()
		if(rand <= su.mutationRate):
			if su.geneType == "Float string":
				if(rd.random() <= .5):
					chrom[i] += delta(su.currentGeneration, su.maxGenerations, domain[1] - chrom[i])
				else:
					chrom[i] -= delta(su.currentGeneration, su.maxGenerations, chrom[i] - domain[0])
			else:
				if(rd.random() <= .5):
					chrom[i] += int(delta(su.currentGeneration, su.maxGenerations, domain[1] - chrom[i]))
				else:
					chrom[i] -= int(delta(su.currentGeneration, su.maxGenerations, chrom[i] - domain[0]))
		i += 1

	return fit.getFitness(chrom, su)

'''Auxiliar function for non-uniform mutation. The higher the generation, the lower the value added to the gene'''
def delta(currentGen, maxGen, value):
	rand = rd.random()
	result = value * (1 - rand**(1 - currentGen/maxGen)) 
	return result

'''Crossover management'''
def crossover(su):
	newPopulation = []
	sel.initSelection(su)

	#New childs are born until the current size of the population is equal to two times the initial size
	while(su.currentPopulationSize <= 2 * su.populationSize):
		#Choosing first parent
		index1 = sel.selectParent(su)
		parent1 = su.population[index1]

		#Choosing second parent
		index2 = sel.selectParent(su)

		#If index1 and index2 are the same, index2 assumes the previous (or next) index 
		if(index1 == index2): 
			if index2 == su.populationSize - 1:
				index2 -= 1
			else:
				index2 += 1
		
		parent2 = su.population[index2]

		#Childs being born and mutated
		if su.crossover == "One point":
			child1, child2 = onePointCrossover(parent1, parent2, su)
		elif su.crossover == "Two points":
			child1, child2 = twoPointCrossover(parent1, parent2, su)
		else:
			child1, child2 = uniformCrossover(parent1, parent2, su)

		aux1 = mutation(child1, su)
		aux2 = mutation(child2, su)

		if su.geneType == "Float string":
			if aux1[0]:
				child1 = [round(float(value), 3) for value in child1] #rounding values
			if aux2[0]:
				child2 = [round(float(value), 3) for value in child2] #rounding values

		counter = 0 

		while True:
			#Adding child to population 
			if aux1:
				newPopulation.append(child1)
				su.currentPopulationSize += 1
				break

			if aux2:
				newPopulation.append(child2)
				su.currentPopulationSize += 1
				break

			counter += 1

			if(counter == su.populationSize):
				return

	#Saving best individual of current generation
	best = su.population[0]
	su.population = newPopulation
	su.population.append(best)

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
	return child1, child2

'''Sorting population in decrescent order of fitness, acording to the object task'''
def sort(su):
	if(su.task == "max"):
		su.population.sort(key=lambda x: float(x[-1]), reverse = True)	
	else:	
		su.population.sort(key=lambda x: float(x[-1]), reverse = False)	
	
	return su.population[0:su.populationSize]