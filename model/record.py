'''Here the file operations are done'''
import datetime
import time
import os
import struct
import math

def bin2float(binary):
    return struct.unpack('!f',struct.pack('!I', int(binary, 2)))[0]

def truncate(f, n = 3):
    return math.floor(f * 10 ** n) / 10 ** n

'''Each experiment is saved in a file which name is the moment of the experiment's execution'''
def setName(now):
    day = '{:02d}'.format(now.day)
    month = '{:02d}'.format(now.month)
    year = str(now.year)
    date = day + '-' + month + '-' + year

    hour = '{:02d}'.format(now.hour)
    minute = '{:02d}'.format(now.minute)
    second = '{:02d}'.format(now.second)
    time = hour + ':' + minute + ':' + second

    return date + '.' + time + ".txt"

'''Opening file'''
def newFile(setupName):
	#Getting the current script path
	parentDir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
	subDir = "Output"
	fileName = setupName + " | " + str(setName(datetime.datetime.now()))
	filePath = os.path.join(parentDir, subDir, fileName)

	#Creating subdirectory
	try:
		os.mkdir(os.path.join(parentDir, subDir))
	except Exception as e:
		pass

	file = open(filePath, 'w') 
	return file

'''Writing on file'''
def save(name, log):
	file = newFile(name)

	for line in log:
		file.write(line)

	file.close()

'''This function returns a ordinal number used on report of best simulation'''
def ordinal(number):
	number = str(number)

	if(number[-1] == '1'):
		return number + "st"
	if(number[-1] == '2'):
		return number + "nd"
	if(number[-1] == '3'):
		return number + "rd"
	else :
		return number + "th"
	

'''Closing file'''
def record(bestIndividual, log, su):
	'''Adding a heading to the file containing the setup chosen by the user'''
	su.log.append(" Function: {}\n".format(su.function.replace(" ", "")))
	su.log.append(" Domain: {}\n".format(su.varDomain))
	task = "Maximize" if su.task == "max" else "Minimize"
	su.log.append(" Objective: {}\n\n".format(task))

	su.log.append(" Maximum population size: {}\n".format(su.populationSize))
	su.log.append(" Maximum number of generations: {}\n".format(su.maxGenerations))
	su.log.append(" Plateau: {}\n".format(su.plateau))
	su.log.append(" Crossover probability: {}\n".format(su.crossoverProb))
	su.log.append(" Mutation rate: {}\n\n".format(su.mutationRate))

	su.log.append(" Selection strategy: {}\n".format(su.selection))
	su.log.append(" Crossover strategy: {}\n".format(su.crossover))
	su.log.append(" Mutation strategy: {}\n".format(su.mutation))
	su.log.append(' {:#<40}'.format("") + "\n")

	'''Simulation result'''
	if su.geneType == "Integer string":
		champion = [int(value) for value in bestIndividual['champion'][:-1]]
		champion.append(truncate(bestIndividual["champion"][-1]))
	elif su.geneType == "Float string":
		champion = bestIndividual["champion"]
		champion = [truncate(gene) for gene in champion]
	else:
		champion = []
		begin = 0

		for i in range(len(su.varLength)):           
        	#Replacing values
			end = begin + su.varLength[i]
			value = bin2float("".join(bestIndividual["champion"][begin:end]))
			champion.append(truncate(value))
			begin = end
		champion.append(truncate(bestIndividual["champion"][-1]))

	su.log.append("\n -> Best simulation: #{}.".format(bestIndividual["id"]))
	su.log.append("\n -> Champion: {}.".format(champion))
	su.log.append("\n -> Achieved in the {} generation.".format(ordinal(bestIndividual["last"])))
	su.log.append("\n -> Population average fitness: {0:.3f}\n\n".format(bestIndividual["average"]))
	su.log.append(' {:#<40}'.format("") + "\n")

	for entry in log:
		su.log.append(entry)
