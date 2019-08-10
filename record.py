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
def newFile(setupName):
	global file
	name = datetime.datetime.now()
	file = open(setupName + " | " + str(setName(name)), 'w') 

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
def record(bestIndividual, average, log, su):
	'''Adding a heading to the file containing the setup chosen by the user'''
	su.log.append(" Function: {}\n".format(su.function.replace(" ", "")))
	su.log.append(" Domain: {}\n".format(su.varDomain))
	task = "Maximize" if su.task == "max" else "Minimize"
	su.log.append(" Objective: {}\n\n".format(task))

	su.log.append(" Maximum population size: {}\n".format(su.populationSize))
	su.log.append(" Maximum number of generations: {}\n".format(su.maxGenerations))
	su.log.append(" Plateau: {}\n\n".format(su.plateau))

	su.log.append(" Crossover strategy: {}\n".format(su.crossover))
	su.log.append(" Selection strategy: {}\n".format(su.selection))
	su.log.append(" Mutation strategy: {}\n".format(su.mutation))
	su.log.append(" Mutation rate: {}\n\n".format(su.mutationRate))
	su.log.append(' {:#<40}'.format("") + "\n")

	'''Simulation result'''
	if su.geneType != "Float string":
		champion = [int(value) for value in bestIndividual['champion'][:-1]]
		champion.append(round(bestIndividual["champion"][-1], 3))
	else:
		champion = bestIndividual["champion"]
		champion[-1] = round(champion[-1], 3)

	su.log.append("\n -> Best simulation: #{}.".format(bestIndividual["id"]))
	su.log.append("\n -> Champion: {}. Achieved in the {} generation.".format(champion, ordinal(bestIndividual["last"])))
	su.log.append("\n -> Average fitness: {0:.2f}\n\n".format(average))
	su.log.append(' {:#<40}'.format("") + "\n")

	for entry in log:
		su.log.append(entry)