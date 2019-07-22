import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import numpy as np

'''Returns the limits of x and y axis used on plotting'''
def getLimits(history):
	xb = xe = yb = ye = None

	for entry in history:
		x, y = zip(*entry)
		for xEntry in x:
			if xb == None or xEntry < xb:
				xb = xEntry

			if xe == None or xEntry > xe:
				xe = xEntry

		for yEntry in y:
			if yb == None or yEntry < yb:
				yb = yEntry

			if ye == None or yEntry > ye:
				ye = yEntry

	return xb, xe, yb, ye

'''Plotting the progression of best inidviual for each setup'''
def plotFitness(history, task, nameList):	
	#Creating panel
	fig, ax = plt.subplots(1,1)
	xTick = []
	yTick = []
	xb, xe, yb, ye = getLimits(history)
	marker = ['o', 's', '^', 'd', 'P']
	
	count = 0
	print(nameList)
	for entry in history:
		print(count)
		x, y = zip(*entry)
		ax.plot(x, y, marker = marker[count % 5], label = "{}".format(nameList[count]))
		count += 1

	#Setting grid for better visualization
	ax.yaxis.grid(True, which="major")

	#Setting title and subtitle
	plt.suptitle("Progression of best individual", x = 0.43)
	if(task == "min"):
		plt.title("Minimizing function", fontsize = 8)
	else:
		plt.title("Maximizing function", fontsize = 8)

	#Setting axis label	
	plt.xlabel("Generation")				
	plt.ylabel("Fitness of best individual")

	xMean = math.floor((xe - xb) / 4)
	yMean = math.floor((ye - yb) / 4)

	for i in range(4):
		xTick.append(xb + xMean * i)
		yTick.append(yb + yMean * i)

	xTick.append(xe)
	yTick.append(ye)

	#Setting legend position
	box = ax.get_position()
	ax.set_position([box.x0, box.y0, box.width 	* 0.75, box.height])
	plt.legend(loc = 'upper left', bbox_to_anchor=(1, 1))
	plt.xticks(xTick)
	plt.yticks(yTick)
	#plt.show()

'''Plotting generations reached for each setup'''
def plotGenerations(history, task, nameList):
	#Creating panel
	fig, ax = plt.subplots(1,1)
	xTick = []
	yTick = []
	xb, xe, yb, ye = getLimits(history)
	marker = ['o', 's', '^', 'd', 'P']
	count = 0

	for entry in history:
		x, y = zip(*entry)
		ax.plot(x, y, marker = marker[count % 5], label = "{}".format(nameList[count]))
		count += 1

	#setting grid for better visualization
	ax.yaxis.grid(True, which="major")

	#Setting title and subtitle
	plt.suptitle("Simulations x Reached generations", x = 0.43)
	if(task == "min"):
		plt.title("Minimizing function", fontsize = 8)
	else:
		plt.title("Maximizing function", fontsize = 8)

	#Setting axis label
	plt.xlabel("Simulation")				
	plt.ylabel("Number of generations")

	yMean = math.ceil((ye - yb) / 4)
	yTick = [yb, yb + yMean, yb + 2*yMean, yb + 3*yMean, ye]

	#Setting legend position
	box = ax.get_position()
	ax.set_position([box.x0, box.y0, box.width 	* 0.75, box.height])
	plt.legend(loc = 'upper left', bbox_to_anchor=(1, 1))
	plt.xticks(x)
	plt.yticks(yTick)
	plt.show()