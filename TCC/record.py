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
    time = hour + ':' + minute

    return date + '.' + time + '.txt'

'''Opening file'''
def newFile():
	global file
	now = datetime.datetime.now()
	file = open(setName(now), "a") 

	'''Adding a heading to the file containing the setup chosen by the user'''
	write("##########Setup##########\n\n")

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

	write("#########################\n\n")

def write(text):
	file.write(text)

def close():
	file.close()
