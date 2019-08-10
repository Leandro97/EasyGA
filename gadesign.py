# -*- coding: utf-8 -*-
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.bubble import Bubble
from kivy.clock import Clock
from kivy.config import Config
from kivy.properties import StringProperty, BooleanProperty, ListProperty
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.graphics import Rectangle, Color
from kivy.lang import Builder

'''
TODO
- Apêndice de instalação do docker ou bibliotecas
- Popup de ajuda mostrando sintaxe
'''

import time, threading
from functools import partial
import middle as mid
import fitness as fit
import record as rec
import plotter as plt  

TEXT_COLOR = (0, 0, 0, 1)

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'width', '700dp')
Config.set('graphics', 'height', '0dp')

varList = [] #Stores (minValue, maxValue) pairs
varCounter = 1

setupList = []
setupNumber = 0
currentSetup = 0

nameList = []

def warningPopup(message):
	box = BoxLayout(orientation = "vertical", spacing = "20dp")
	popup = Popup(title = "Warning!", content = box, size_hint = (.8, .28))
	popup.open()
	box.add_widget(Label(text = message))
	box.add_widget(Button(text = "Ok", on_press = lambda x : popup.dismiss()))

class TabPanel(TabbedPanel):
	global varList
	global varCounter
	mutationValues = ListProperty(["Flip"]) 

	def __init__(self, **kwargs):
		super(TabPanel, self).__init__(**kwargs)

		#Tab1
		newVar = MyLabel()
		newVar.setVar("x1")

		#bind to check values and swap if minValue > maxValue
		minValue = VarTextInput()
		minValue.setVar("-10")
		minValue.bind(text = partial(self.validateVars, varCounter - 1, 0))

		#bind to check values and swap if minValue > maxValue
		maxValue = VarTextInput()
		maxValue.setVar("10")
		maxValue.bind(text = partial(self.validateVars, varCounter - 1, 1))

		self.ids.varScrollView.add_widget(newVar)
		self.ids.varScrollView.add_widget(minValue)
		self.ids.varScrollView.add_widget(maxValue)
		varList.append((minValue, maxValue))

	def getParams(self):
		global nameList

		geneType = self.ids.geneType.text
		func = self.ids.fitnessFunction.text

		if(self.ids.minCheckBox.active):
			task = "min"
		else:
			task = "max"

		return geneType, func, task, nameList

	def syntaxHelper(self):
		text1 = (
		  f"""[size=20]Basic operations[/size]\n"""
		  f"""Addition: x1 + x2\n"""
		  f"""Subtraction: x1 - x2\n"""
		  f"""Multiplication: x1 * x2\n"""
		  f"""Division: x1 / x2\n\n"""

		  f"""[size=20]Especial functions[/size]\n"""
		  f"""Floor: floor(x1)\n"""
		  f"""Ceiling: ceil(x1)\n"""
		  f"""x1 to the power x2: pow(x1, x2) or x1**x2\n"""
		  f"""Natural logarithm: log(x1)\n"""
		  f"""Base-x2 logarithm: log(x1, x2)\n\n"""
		  )

		text2 = (
		  f"""[size=20]Constants[/size]\n"""
		  f"""Euler's number: e\n"""
		  f"""Pi: pi\n"""
		  f"""Tau: tau\n\n"""


		  f"""[size=20]Trigonometric functions[/size]\n"""
		  f"""Sine, arc sine: sin(x1), asin(x1)\n"""
		  f"""Cosine, arc cosine: cos(x1), acos(x1)\n"""
		  f"""Tangent, arc tangent: tan(x1), atan(x1)\n"""
		  f"""From radians to degrees: degrees(x1)\n"""
		  f"""From degrees to radians: radians(x1)\n\n"""
		)

		box = BoxLayout(orientation = "vertical", spacing = "20dp")
		insideBox = BoxLayout(spacing = "20dp")
		insideBox.add_widget(Label(text = text1, markup=True))
		insideBox.add_widget(Label(text = text2, markup=True))
		popup = Popup(title = "What can I do?", content = box, size_hint = (.8, .8))
		popup.open()

		box.add_widget(insideBox)
		box.add_widget(Button(text = "Ok", size_hint_y = 0.1, on_press = lambda x : popup.dismiss()))

	def updateType(self, text):
		global setupList
		global varList
		mutationArray = []

		if(text != "Binary string"):
			mutationArray = ["Uniform", "Non-uniform"]
		else:
			mutationArray = ["Flip"]

		self.ids.setupLayout.myScreen.mutation.text = mutationArray[0]
		self.ids.setupLayout.myScreen.mutation.values = mutationArray
		self.mutationValues = mutationArray

		for setup in setupList:
			setup[6] = mutationArray[0]

		if self.ids.geneType.text != "float":
			for var in varList:
				var[0].text = str(int(float(var[0].text)))
				var[1].text = str(int(float(var[1].text)))

	def validateVars(self, varIndex, valueIndex, aux, text):
		global varList
		try:
			if(self.ids.geneType.text != "Float string"):
				int(varList[varIndex][valueIndex].text)
			else:
				float(varList[varIndex][valueIndex].text)

			self.unlockInputs()
		except Exception as e:
			self.blockInputs(varIndex, valueIndex)

			geneType = "float" if(self.ids.geneType.text == "Float string") else "integer"

	def blockInputs(self, varIndex, valueIndex):
		self.validTab1 = False
		self.ids.geneType.disabled = True

		for i in range(len(varList)):
			if i == varIndex:
				if valueIndex == 0:
					varList[i][1].disabled = True
				else:
					varList[i][0].disabled = True 
			else:
				varList[i][0].disabled = True
				varList[i][1].disabled = True 

	def unlockInputs(self):
		self.validTab1 = True
		self.ids.geneType.disabled = False		

		for i in range(len(varList)):
			varList[i][0].disabled = False
			varList[i][1].disabled = False

class MyTab(BoxLayout):
	pass

class MyButton(Button):
	pass

class MyCheckBox(CheckBox):
	def __init__(self, **kwargs):
		super(MyCheckBox, self).__init__(**kwargs)
		self.size_hint_x = .1
		self.color = TEXT_COLOR
		self.pos_hint = {"x": .8}
		self.allow_no_selection = False

class MyLabel(Label):
	def setVar(self, text):
		self.size_hint_y =  None
		self.height = "35dp"
		self.text = text

class VarTextInput(TextInput):
	def __init__(self, **kwargs):
		super(VarTextInput, self).__init__(**kwargs)
		self.write_tab = False
		self.multiline = False

	def setVar(self, text):
		self.size_hint_y =  None
		self.height = "35dp"
		self.text = text

class SetupBar(BoxLayout):
	global setupList

	spinner = Spinner()
	editButton = MyButton()
	newSetupButton = MyButton()
	removeButton = MyButton()

	def __init__(self, **kwargs):
		super(SetupBar, self).__init__(**kwargs)
		Clock.schedule_once(self.load)
		
	def load(self, dt):
		global setupNumber
		global nameList

		self.spinner.bind(text = self.parent.updateScreen)
		self.spinner.text = "Setup 1"
		self.spinner.values = ["Setup 1"]
		nameList = self.spinner.values

		self.editButton.bind(on_press = lambda x : self.doPopUp())
		self.editButton.text = "Edit name"

		self.newSetupButton.bind(on_press = lambda x : self.createSetup("Setup " + str(setupNumber + 2)))
		self.newSetupButton.text = str("New setup")

		self.removeButton.bind(on_press = lambda x : self.deletePopup())
		self.removeButton.text = "Delete setup"

		self.add_widget(self.spinner)
		self.add_widget(self.editButton)
		self.add_widget(self.newSetupButton)
		self.add_widget(self.removeButton)

	def doPopUp(self):
		box = BoxLayout(orientation = "vertical", spacing = "20dp")
		insideBox = BoxLayout(spacing = "20dp", size_hint_y = .5)

		popup = Popup(title='New name for ' + self.spinner.text, content= box, size_hint = (.5, .3))
		popup.open()
		
		save = MyButton(text = "Save")
		save.bind(on_press = lambda x : self.changeName(newName.text, popup))

		cancel = MyButton(text = "Cancel")
		cancel.bind(on_press = lambda x : popup.dismiss())

		insideBox.add_widget(save)
		insideBox.add_widget(cancel)

		newName = TextInput(write_tab = False, multiline = False, size_hint_y = .55)

		box.add_widget(newName)
		box.add_widget(insideBox)

	def changeName(self, text, popup):
		global currentSetup
		global nameList

		if text.strip() == "":
			popup.dismiss()
			return

		self.spinner.values[currentSetup] = text
		nameList = self.spinner.values
		self.spinner.text = text
		popup.dismiss()

	def createSetup(self, text):
		global nameList
		target = self.parent

		target.myScreen.newSetup()	
		self.spinner.values.append(text)
		self.spinner.text = text
		target.myLabel.text = text

		nameList = self.spinner.values

	def deletePopup(self):
		global currentSetup
		global nameList
		if(len(setupList) == 1):
			return

		box = BoxLayout(spacing = "20dp")

		popup = Popup(title = "Are you sure you want to delete " + nameList[currentSetup] + "?", content = box, size_hint = (.5, .18))
		popup.open()
		
		delete = MyButton(text = "Delete")
		delete.bind(on_press = lambda x : self.deleteSetup(popup))

		cancel = MyButton(text = "Cancel")
		cancel.bind(on_press = lambda x : popup.dismiss())

		box.add_widget(delete)
		box.add_widget(cancel)

	def deleteSetup(self, popup):
		global setupNumber
		global currentSetup
		global nameList

		try:
			self.spinner.text = self.spinner.values[currentSetup - 1]
			del setupList[currentSetup + 1]
			del self.spinner.values[currentSetup + 1]	
		except:
			self.spinner.text = self.spinner.values[1]
			del setupList[0]
			del self.spinner.values[0]	

		setupNumber -= 1
		nameList = self.spinner.values
		popup.dismiss()

class ParamTextInput(TextInput):
	def __init__(self, **kwargs):
		super(ParamTextInput, self).__init__(**kwargs)
		self.write_tab = False
		self.multiline = False
		self.size_hint_y = .55

Builder.load_string('''
<ValidationLabel>:
    canvas:
        Color:
            rgba: self.rgba
        Rectangle:
            pos: self.pos
            size: self.size
''')

class ValidationLabel(Label):
	rgba = ListProperty([0, 0, 1, .15])
	
	def invalid(self, message):
		self.rgba = [1, 0, 0, .15]
		self.text = message
		App.get_running_app().root.validTab3 = False

	def valid(self):
		self.rgba = [0, 0, 1, .15]
		App.get_running_app().root.validTab3 = True

class MyScreen(Screen):
	global setupNumber
	global setupList

	inputNames = {0: "Population size", 1: "Number of generations", 2: "Plateau", 3: "Mutation rate"}
	
	populationSize = ParamTextInput(text = "10")
	maxGenerations = ParamTextInput(text = "50")
	plateau = ParamTextInput(text = "20")
	mutationRate = ParamTextInput(text = "0.01")

	selection = Spinner(text = "Roulette", size_hint_y = .7)
	selection.values = ["Roulette", "Tournament", "Rank"]

	crossover = Spinner(text = "One point", size_hint_y = .7)
	crossover.values = ["One point", "Two points", "Uniform"]

	mutation = Spinner(text = "Flip", size_hint_y = .7) 
	mutation.values = ["Flip"]

	validationLabel = ValidationLabel(text = "Parameters are valid!", color = (0, 0, 0, 1))

	def makeTextInput(self, layout, widget, labelText, minValue, maxValue, index):
		paramLayout = BoxLayout(orientation = "vertical")
		paramLabel = MyLabel(text = labelText, color = TEXT_COLOR)

		widget.bind(text = partial(self.updateFromTextInput, index, minValue, maxValue))

		paramLayout.add_widget(paramLabel)
		paramLayout.add_widget(widget)
		layout.add_widget(paramLayout)

	def makeSpinner(self, layout, widget, labelText, index):
		paramLayout = BoxLayout(orientation = "vertical")
		paramLabel = MyLabel(text = labelText, color = TEXT_COLOR)

		widget.bind(text = partial(self.updateFromSpinner, index))

		paramLayout.add_widget(paramLabel)
		paramLayout.add_widget(widget)
		layout.add_widget(paramLayout)

	def __init__(self, **kwargs):
		super(MyScreen, self).__init__(**kwargs)
		setupList.append(["10", "50", "20", "0.01", "Roulette", "One point", "Flip"])
		
		parentLayout = GridLayout(cols = 2, spacing = "10dp")

		self.add_widget(parentLayout)
		self.makeTextInput(parentLayout, self.populationSize, "Population size", 10, 1000, 0)
		self.makeTextInput(parentLayout, self.maxGenerations, "Number of generations", 1, 1000, 1)
		self.makeTextInput(parentLayout, self.plateau, "Plateau", 1, 1000, 2)
		self.makeTextInput(parentLayout, self.mutationRate, "Mutation rate", 0, 1, 3)
		self.makeSpinner(parentLayout, self.selection, "Selection strategy", 4)
		self.makeSpinner(parentLayout, self.crossover, "Crossover strategy", 5)
		self.makeSpinner(parentLayout, self.mutation, "Mutation strategy", 6)
		parentLayout.add_widget(self.validationLabel)

	def updateFromSpinner(self, attIndex, aux, text):
		setupList[currentSetup][attIndex] = text

	def updateFromTextInput(self, attIndex, minValue, maxValue, aux, text):
		global currentSetup

		try:
			if(attIndex != 3):
				status = int(minValue) <= int(text) <= int(maxValue)
			else:
				status = float(minValue) <= float(text) <= float(maxValue)

			if status:
				self.unlockInputs()
				self.validationLabel.text = "Parameters are valid!"
				self.validationLabel.valid()
				setupList[currentSetup][attIndex] = text
			else:
				self.blockInputs(attIndex)
				self.validationLabel.invalid("{} must be between {} and {}!".format(self.inputNames[attIndex], minValue, maxValue))
		except Exception as e:
			self.blockInputs(attIndex)
			if(attIndex != 3):
				self.validationLabel.invalid("{} must be a integer number!".format(self.inputNames[attIndex]))
			else:
				self.validationLabel.invalid("{} must be a float number!".format(self.inputNames[attIndex]))

	def blockInputs(self, index):
		if(index != 0):
			self.populationSize.disabled = True
		if(index != 1):
			self.maxGenerations.disabled = True
		if(index != 2):
			self.plateau.disabled = True
		if(index != 3):
			self.mutationRate.disabled = True

	def unlockInputs(self):
		self.populationSize.disabled = False
		self.maxGenerations.disabled = False
		self.plateau.disabled = False
		self.mutationRate.disabled = False
		self.mutation.disabled = False

	def newSetup(self):
		global setupNumber
		global currentSetup
		currentSetup += 1
		setupNumber += 1

		setupList.append(["10", "50", "20", "0.01", "Roulette", "One point", App.get_running_app().root.mutationValues[0]])

class SetupLayout(BoxLayout):
	global setupList

	setupBar = SetupBar(spacing = "20dp", size_hint_y = 0.15)
	myLabel = Label(size_hint_y = 0.2, font_size = "35sp", text = "Setup 1", color = TEXT_COLOR)
	myScreen = MyScreen()

	def __init__(self, **kwargs):
		super(SetupLayout, self).__init__(**kwargs)
		self.spacing = "20dp"
		self.orientation = "vertical"
		self.add_widget(self.setupBar)
		self.add_widget(self.myLabel)
		self.add_widget(self.myScreen)

	def updateScreen(self, instance, text):
		global currentSetup
		target = self.myScreen
		i = 0
		index = 0

		for entry in self.setupBar.spinner.values:
			if entry == text:
				index = i
				break
			i += 1

		currentSetup = index

		self.myLabel.text = self.setupBar.spinner.text
		target.populationSize.text = setupList[index][0]
		target.maxGenerations.text = setupList[index][1]
		target.plateau.text = setupList[index][2]
		target.mutationRate.text = setupList[index][3]
		target.selection.text = setupList[index][4]
		target.crossover.text = setupList[index][5]
		target.mutation.text = setupList[index][6]

class Tab1(MyTab):
	global varList

	def addVar(self):
		global varCounter
		varCounter += 1
		target = self.parent.parent
			
		newVar = MyLabel()
		newVar.setVar("x" + str(varCounter))

		minValue = VarTextInput()
		minValue.setVar("-10")
		minValue.bind(text = partial(self.parent.parent.validateVars, varCounter - 1, 0))

		maxValue = VarTextInput()
		maxValue.setVar("10")
		maxValue.bind(text = partial(self.parent.parent.validateVars, varCounter - 1, 1))

		target.ids.varScrollView.add_widget(newVar)
		target.ids.varScrollView.add_widget(minValue)
		target.ids.varScrollView.add_widget(maxValue)
		varList.append((minValue, maxValue))

		target.ids.varScrollView.height += 50

	def removeVar(self):
		global varCounter
		global varList

		target = self.parent.parent

		if(varCounter <= 1):
			return

		for child in target.ids.varScrollView.children[:3]:
			target.ids.varScrollView.remove_widget(child)
		
		varCounter -= 1
		del varList[-1]
		target.ids.varScrollView.height -= 50

class Tab2(MyTab):
	pass

class Tab3(MyTab):
	pass

class Tab4(MyTab):
	pass

class LogScrollView(ScrollView):
	text = StringProperty("")

class SimulationLayout(BoxLayout):
	global varList
	global setupList
	global func

	logIndex = 0
	finalLog = []
	nameList = []
	currentGraph = 1
	plotFitnessLog = None
	plotGenerationLog = None
	task = None

	def __init__(self, **kwargs):
		super(SimulationLayout, self).__init__(**kwargs)

	def evolvePopUp(self):
		box = BoxLayout()
		box.add_widget(Label(text = "Evolution in progress!"))
		self.popup = Popup(title = "Wait a moment", content = box, size_hint = (.5, .18))
		self.popup.open()

	def click(self):
		target = App.get_running_app().root
		target.ids.image.add_widget(FigureCanvasKivyAgg(plt.pyplot.gcf()))
		target.ids.image.clear_widgets()
		self.evolvePopUp()

		mythread = threading.Thread(target = self.evolve)
		mythread.start()

	def evolve(self):
		time.sleep(.5)
		target = App.get_running_app().root
		geneType, func, self.task, nameList = target.getParams()

		check = fit.checkFunction(func, len(varList))

		if not check[0]:
			target.ids.logScrollView.text = ""
			target.ids.image.clear_widgets()
			warningPopup(check[1])
			self.popup.dismiss()
			return

		self.finalLog, self.plotFitnessLog, self.plotGenerationLog = mid.main(geneType, varList, func, self.task, setupList, nameList, 10)

		if self.finalLog == False:
			target.ids.logScrollView.text = ""
			target.ids.image.clear_widgets()
			warningPopup("Function could not be evaluated. Verify your function and domain of the variables.")
			self.popup.dismiss()
			return

		target.ids.logScrollView.text = self.finalLog[self.logIndex]
		self.nameList = nameList

		if(self.currentGraph == 1):
			target.ids.graphButton1.state = "down"
			target.ids.graphButton2.state = "normal"
			self.makePlot1()
		else:
			target.ids.graphButton2.state = "down"
			target.ids.graphButton1.state = "normal"
			self.makePlot2()

		self.popup.dismiss()

	def nextLog(self):
		try:
			self.logIndex = 0 if(self.logIndex + 1 >= len(setupList)) else self.logIndex + 1
			target = App.get_running_app().root
			target.ids.logScrollView.text = self.finalLog[self.logIndex]
		except:
			pass

	def previousLog(self):
		try:
			self.logIndex = len(setupList) - 1 if(self.logIndex <= 0) else self.logIndex - 1
			target = App.get_running_app().root
			target.ids.logScrollView.text = self.finalLog[self.logIndex]
		except:
			pass

	def saveLog(self):
		if not self.finalLog:
			return

		rec.save(self.nameList[self.logIndex], self.finalLog[self.logIndex])
		box = BoxLayout(orientation = "vertical", spacing = "20dp")
		popup = Popup(title = "Log file saved in folder 'Output'", content = box, size_hint = (.5, .18))
		popup.open()
		box.add_widget(Button(text = "Ok", on_press = lambda x : popup.dismiss()))
		
	def makePlot1(self):
		self.currentGraph = 1
		if not self.plotFitnessLog:
			return

		plt.plotFitness(self.plotFitnessLog, self.task, self.nameList)
		target = App.get_running_app().root
		target.ids.image.clear_widgets()
		target.ids.image.add_widget(FigureCanvasKivyAgg(plt.pyplot.gcf()))

	def makePlot2(self):
		self.currentGraph = 2
		if not self.plotGenerationLog:
			return
			
		plt.plotGenerations(self.plotGenerationLog, self.task, self.nameList)
		target = App.get_running_app().root
		target.ids.image.clear_widgets()
		target.ids.image.add_widget(FigureCanvasKivyAgg(plt.pyplot.gcf()))

	def showPlot(self):
		if(self.currentGraph == 1):
			if not self.plotFitnessLog:
				return
			plt.plotFitness(self.plotFitnessLog, self.task, self.nameList) 
		else:
			plt.plotGenerations(self.plotGenerationLog, self.task, self.nameList)

		plt.pyplot.show()

class GADesign(App):
	def build(self):
		return TabPanel()

GADesign().run()