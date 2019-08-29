import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import numpy as np
import io

'''Returns the limits of x and y axis used on plotting'''
def getLimits(history):
	xb = xe = None

	for entry in history:
		x, y, e = zip(*entry)

		for xEntry in x[0]:
			if xb == None or xEntry < xb:
				xb = xEntry

			if xe == None or xEntry > xe:
				xe = xEntry
	return xb, xe

'''Plotting the progression of best inidviual for each setup'''
def plotFitness(history, task, nameList, errorbar):	
	pyplot.close()
	aux = {}

	#Creating panel
	xTick = []
	xb, xe = getLimits(history)
	marker = ['d', 's', '^', 'o', 'P']
	
	count = 0

	for entry in history:
		x, y, e = zip(*entry)
		if(errorbar):
			pyplot.errorbar(x[0], y[0], e[0], capsize = 5, marker = marker[count % 5], label = "{}".format(nameList[count]))
		else:
			pyplot.errorbar(x[0], y[0], marker = marker[count % 5], label = "{}".format(nameList[count]))

		count += 1

	#Setting grid for better visualization
	pyplot.gca().yaxis.grid(True, which="major")

	#Setting title and subtitle
	pyplot.suptitle("Average progression of best individual", x = 0.5)
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
	#box = pyplot.gca().get_position()
	#pyplot.gca().set_position([box.x0, box.y0, box.width * 0.8, box.height])

	if(task == "max"):
		pyplot.legend(loc = 'lower center', fancybox=True, shadow=True)
	else:
		pyplot.legend(loc = 'upper center', fancybox=True, shadow=True)

	pyplot.xticks(xTick)