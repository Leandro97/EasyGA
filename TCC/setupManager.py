import setup
import random as rd

def createSetups(geneType, varList, func, task, bruteSetups):
	setupList = []
	seed = rd.randint(0, 10000)

	for entry in bruteSetups:
		newSetup = setup.Setup()
		newSetup.seed = seed
		newSetup.varDomain = []
		newSetup.log = []
		newSetup.function = func
		newSetup.task = task
		newSetup.geneType = geneType

		for var in varList:
			if(geneType == "Float string"):
				minValue = min(float(var[0].text), float(var[1].text))
				maxValue = max(float(var[0].text), float(var[1].text))
			else:
				minValue = min(int(var[0].text), int(var[1].text))
				maxValue = max(int(var[0].text), int(var[1].text))	

			newSetup.varDomain.append([minValue, maxValue])

		newSetup.populationSize = int(entry[0])
		newSetup.maxGenerations = int(entry[1])
		newSetup.plateau = int(entry[2])
		newSetup.mutationRate = float(entry[3])
		newSetup.selection = entry[4]
		newSetup.crossover = entry[5]
		newSetup.mutation = entry[6]

		setupList.append(newSetup)
	return setupList

def deleteSetup(setupList, index):
    del setup
    return setupList