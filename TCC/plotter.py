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

	xa = x[0]
	xb = x[-1]
	xMean = math.floor((xb - xa) / 4)

	ya = y[0]
	yb = y[-1]
	yMean = math.floor((yb - ya) / 4)

	xTick = [xa, xa + xMean, xa + 2*xMean, xb - xMean, xb]
	yTick = [ya, ya + yMean, ya + 2*yMean, yb - yMean, yb]

	plt.xticks(xTick)
	plt.yticks(yTick)
	plt.show()

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

	xa = x[0]
	xb = x[-1]
	xMean = math.floor((xb - xa) / 4)

	ya = min(y)
	yb = max(y)
	yMean = math.floor((yb - ya) / 4)

	xTick = [xa, xa + xMean, xa + 2*xMean, xb - xMean, xb]
	yTick = [ya, ya + yMean, ya + 2*yMean, yb - yMean, yb]

	print(yTick)
	plt.xticks(xTick)
	plt.yticks(yTick)
	plt.show()