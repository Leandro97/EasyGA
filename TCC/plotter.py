import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

def plot(history, type):
	x, y = zip(*history)

	fig, ax = plt.subplots(1,1)
	ax.plot(x, y, marker='o')

	#setting grid for better visualization
	ax.xaxis.grid(True, which='major')
	ax.yaxis.grid(True, which='major')

	if type == 'fit':
		plt.title('Progressão do melhor indivíduo')
		plt.xlabel('Geração')				
		plt.ylabel('Aptidão do melhor indivíduo')

		#formatting x axis
		ax.xaxis.set_major_locator(MultipleLocator(2))
		ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
		ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
	else:
		plt.title('Simulações x Gerações Alcançadas')
		plt.xlabel('Simulação')				
		plt.ylabel('Número de gerações')

		#formatting x axis
		ax.xaxis.set_major_locator(ticker.MultipleLocator(1))

	#formatting y axis
	ax.yaxis.set_major_locator(MultipleLocator(2))
	ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
	ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))

	ax.tick_params(which='major', length=7)
	ax.tick_params(which='minor', length=3)

	plt.show()

