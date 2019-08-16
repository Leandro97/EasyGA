import math
import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import numpy as np
import io

'''Returns the limits of x and y axis used on plotting'''
def getLimits(history):
	xb = xe = None

	for entry in history:
		x, y = zip(*entry)

		for xEntry in x:
			if xb == None or xEntry < xb:
				xb = xEntry

			if xe == None or xEntry > xe:
				xe = xEntry
	return xb, xe

'''Plotting the progression of best inidviual for each setup'''
def plotFitness(history, task, nameList):	
	pyplot.close()

	#Creating panel
	xTick = []
	xb, xe = getLimits(history)
	marker = ['o', 's', '^', 'd', 'P']
	
	count = 0

	for entry in history:
		x, y = zip(*entry)
		pyplot.plot(x, y, marker = marker[count % 5], label = "{}".format(nameList[count]))
		count += 1

	#Setting grid for better visualization
	pyplot.gca().yaxis.grid(True, which="major")

	#Setting title and subtitle
	pyplot.suptitle("Progression of best individual", x = 0.43)
	if(task == "min"):
		pyplot.title("Minimizing function", fontsize = 8)
	else:
		pyplot.title("Maximizing function", fontsize = 8)

	#Setting axis label	
	pyplot.xlabel("Generation")				
	pyplot.ylabel("Fitness of best individual")

	#Setting x-axis marks
	xMean = math.floor((xe - xb) / 4)
	for i in range(4):
		xTick.append(xb + xMean * i)

	xTick.append(xe)

	#Setting legend position
	box = pyplot.gca().get_position()
	pyplot.gca().set_position([box.x0, box.y0, box.width * 0.8, box.height])
	pyplot.legend(loc = 'upper left', bbox_to_anchor = (1, 1), fancybox=True, shadow=True)
	pyplot.xticks(xTick)

'''Plotting generations reached for each setup'''
def plotGenerations(history, task, nameList):
	pyplot.close()

	#Creating panel
	xTick = []
	yTick = []
	xb, xe = getLimits(history)
	marker = ['o', 's', '^', 'd', 'P']
	count = 0

	for entry in history:
		x, y = zip(*entry)
		pyplot.plot(x, y, marker = marker[count % 5], label = "{}".format(nameList[count]))
		yTick.extend(y)
		count += 1

	#setting grid for better visualization
	pyplot.gca().yaxis.grid(True, which="major")

	#Setting title and subtitle
	pyplot.suptitle("Simulations x Generations reached", x = 0.43)
	if(task == "min"):
		pyplot.title("Minimizing function", fontsize = 8)
	else:
		pyplot.title("Maximizing function", fontsize = 8)

	#Setting axis label
	pyplot.xlabel("Simulation")				
	pyplot.ylabel("Number of generations")

	#Setting legend position
	box = pyplot.gca().get_position()
	pyplot.gca().set_position([box.x0, box.y0, box.width * 0.8, box.height])
	pyplot.legend(loc = 'upper left', bbox_to_anchor = (1, 1), fancybox=True, shadow=True)
	pyplot.xticks(x)