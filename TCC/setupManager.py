import setup
import random as rd

def createSetups(geneType, bruteVars, func, task, bruteSetups):
	setupList = []
	seed = rd.randint(0, 10000)

	i = 0
	for entry in bruteSetups:
		newSetup = setup.Setup()
		newSetup.seed = seed
		newSetup.varDomain = []
		newSetup.log = []
		newSetup.function = func
		newSetup.task = task

		if(geneType == "Binary string"):
			newSetup.geneType = "bin"
		elif(geneType == "Integer string"):
			newSetup.geneType = "int"
		else:
			newSetup.geneType = "float"

		for var in bruteVars:
			newSetup.varDomain.append([int(var[0].text), int(var[1].text)])

		newSetup.populationSize = int(entry[0])
		newSetup.maxGenerations = int(entry[1])
		newSetup.plateau = int(entry[2])
		newSetup.mutationRate = float(entry[3])

		if(entry[4] == "Roulette"):
			newSetup.selection = "roulette"

		if(entry[5] == "One Point"):
			newSetup.crossover = "onePoint"
		elif(entry[5] == "Two Points"):
			newSetup.crossover = "twoPoint"
		else:
			newSetup.crossover ="uniform"

		if(entry[6] == "Flip"):
			newSetup.mutation = "flip"
	
		setupList.append(newSetup)
		i += 1
	return setupList

def deleteSetup(setupList, index):
    del setup
    return setupList