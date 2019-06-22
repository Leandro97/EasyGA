import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import setup as su
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
def plotFitness(history, su):	
	if not su.saveGraphs:
		return 

	#Creating panel
	fig, ax = plt.subplots(1,1)
	xTick = []
	yTick = []
	xb, xe, yb, ye = getLimits(history)
	count = 1

	for entry in history:
		x, y = zip(*entry)
		ax.plot(x, y, marker = 'o', label = "Configuração {}".format(count))
		count += 1

	#Setting grid for better visualization
	ax.yaxis.grid(True, which="major")

	#Setting title and subtitle
	plt.suptitle("Progressão do melhor indivíduo", x = 0.43)
	if(su.task == "min"):
		plt.title("Minimizando função", fontsize = 8)
	else:
		plt.title("Maximizando função", fontsize = 8)

	#Setting axis label	
	plt.xlabel("Geração")				
	plt.ylabel("Aptidão do melhor indivíduo")

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
	plt.show()

'''Plotting generations reached for each setup'''
def plotGenerations(history, su):
	if not su.saveGraphs:
		return 

	#Creating panel
	fig, ax = plt.subplots(1,1)
	xTick = []
	yTick = []
	xb, xe, yb, ye = getLimits(history)
	count = 1

	for entry in history:
		x, y = zip(*entry)
		ax.plot(x, y, marker = 'o', label = "Configuração {}".format(count))
		count += 1

	#setting grid for better visualization
	ax.yaxis.grid(True, which="major")

	#Setting title and subtitle
	plt.suptitle("Simulações x Gerações Alcançadas", x = 0.43)
	if(su.task == "min"):
		plt.title("Minimizando função", fontsize = 8)
	else:
		plt.title("Maximizando função", fontsize = 8)

	#Setting axis label
	plt.xlabel("Simulação")				
	plt.ylabel("Número de gerações")

	yMean = math.ceil((ye - yb) / 4)
	yTick = [yb, yb + yMean, yb + 2*yMean, yb + 3*yMean, ye]

	#Setting legend position
	box = ax.get_position()
	ax.set_position([box.x0, box.y0, box.width 	* 0.75, box.height])
	plt.legend(loc = 'upper left', bbox_to_anchor=(1, 1))
	plt.xticks(x)
	plt.yticks(yTick)
	plt.show()