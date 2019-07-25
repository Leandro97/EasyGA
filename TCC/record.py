'''Here the file operations are done'''
import datetime
import time

file = []

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
def newFile(su):
	if not su.saveLog:
		return

	global file
	name = datetime.datetime.now()
	file = open(setName(name), 'w') 

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

'''Writing on file'''
def write(su, log):
	for entry in log:
		su.log.append(entry)

'''Closing file'''
def close(bestIndividual, average, log, su):
	'''Adding a heading to the file containing the setup chosen by the user'''
	su.log.append("Function: '{}'\n".format(su.function))
	su.log.append("Objective: '{}'\n\n".format(su.task))

	su.log.append("Maximum population size: {}\n".format(su.populationSize))
	su.log.append("Maximum number of generations: {}\n".format(su.maxGenerations))
	su.log.append("Plateau: {}\n\n".format(su.plateau))

	crossover = 'one point' if (su.crossover == 'onePoint') else 'two point'
	su.log.append("Crossover strategy: '{}'\n".format(su.crossover))
	su.log.append("Selection strategy: '{}'\n".format(su.selection))
	su.log.append("Mutation strategy: '{}'\n".format(su.mutation))
	su.log.append("Mutation rate: {}\n\n".format(su.mutationRate))
	su.log.append('{:#<40}'.format("") + "\n")

	'''Simulation result'''
	su.log.append("\n-> Best simulation: #{}.".format(bestIndividual['id']))
	su.log.append("\n-> Champion: {}. Achieved in the {} generation.".format(bestIndividual['champion'], ordinal(bestIndividual['last'])))
	su.log.append("\n-> Average fitness: {0:.2f}\n\n".format(average))
	su.log.append('{:#<40}'.format("") + "\n")

	for entry in log:
		su.log.append(entry)