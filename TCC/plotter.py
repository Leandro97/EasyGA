import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

def plotFitness(history):
	xTick = []
	yTick = []
	x, y = zip(*history)

	fig, ax = plt.subplots(1,1)
	ax.plot(x, y, marker='o')

	#setting grid for better visualization
	ax.yaxis.grid(True, which='major')

	plt.title('Progressão do melhor indivíduo')
	plt.xlabel('Geração')				
	plt.ylabel('Aptidão do melhor indivíduo')

	xMean = math.floor((x[-1] - x[0]) / 4)
	yMean = math.floor((y[-1] - y[0]) / 4)

	for i in range(5):
		xTick.append(x[0] + xMean * i)
		yTick.append(y[0] + yMean * i)

	xTick.append(x[-1])
	yTick.append(y[-1])

	plt.xticks(xTick)
	plt.yticks(yTick)
	#plt.show()

def plotGenerations(history):
	xTick = []
	yTick = []
	x, y = zip(*history)

	fig, ax = plt.subplots(1,1)
	ax.plot(x, y, marker='o')

	#setting grid for better visualization
	ax.yaxis.grid(True, which='major')

	plt.title('Simulações x Gerações Alcançadas')
	plt.xlabel('Simulação')				
	plt.ylabel('Número de gerações')

	ya = min(y)
	yb = max(y)
	yMean = math.ceil((yb - ya) / 4)
	yTick = [ya, ya + yMean, ya + 2*yMean, ya + 3*yMean, yb]

	for i in range(4):
		yTick.append(ya + yMean * i)
	yTick.append(max(y))

	plt.xticks(x)
	plt.yticks(yTick)
	plt.show()