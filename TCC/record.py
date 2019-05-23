'''Here the file operations are done'''
import setup as su
from setup import *
import datetime

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

    return date + '.' + time + '.txt'

'''Opening file'''
def newFile():
	global file
	now = datetime.datetime.now()
	file = open(setName(now), "a") 

	if(su.saveHeader):
		'''Adding a heading to the file containing the setup chosen by the user'''
		write("##############Setup##############\n\n")

		write("Function: '{}'\n".format(su.function))
		write("Objective: '{}'\n\n".format(su.task))

		write("Maximum population size: {}\n".format(su.populationSize))
		write("Maximum number of generations: {}\n".format(su.maxGenerations))
		write("Plateau: {}\n\n".format(su.plateau))

		crossover = 'one point' if (su.crossover == 'onePoint') else 'two point'
		write("Crossover strategy: '{}'\n".format(su.crossover))
		write("Selection strategy: '{}'\n".format(su.selection))
		write("Mutation strategy: '{}'\n".format(su.mutation))
		write("Mutation rate: {}\n\n".format(su.mutationRate))

		write("#################################\n")

'''This function returns a ordinal number used on report of best simulation'''
def ordinal(number):
	number = str(number)

	print(number[-1])
	if(number[-1] == '0'):
		return number + 'st'
	if(number[-1] == '2'):
		return number + 'nd'
	if(number[-1] == '3'):
		return number + 'rd'
	else :
		return number + 'th'

'''Writing on file'''
def write(text):
	file.write(text)

'''Closing file'''
def close():
	file.close()
