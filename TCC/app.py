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


import time, threading
from functools import partial
import middle as mid
import record as rec
import plotter as plt  

TEXT_COLOR = (0, 0, 0, 1)

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'width', '700dp')
Config.set('graphics', 'height', '0dp')

varList = [] #Guarda pares (minValue, maxValue)
varCounter = 1

setupList = []
setupNumber = 0
currentSetup = 0

nameList = []

class TabPanel(TabbedPanel):
	global varList
	#validation_color = ListProperty([0, 1, 0, 1]) #study using properties to block spinners

	def __init__(self, **kwargs):
		super(TabPanel, self).__init__(**kwargs)
		self.validStatus = True

		#Tab1
		newVar = MyLabel()
		newVar.setVar("x1")

		minValue = VarTextInput()
		minValue.setVar("0")

		maxValue = VarTextInput()
		maxValue.setVar("10")

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
		#spinnerLayout = BoxLayout(spacing = "0dp")

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

	#colocar limite de caracteres
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
		App.get_running_app().root.validStatus = False

	def valid(self):
		self.rgba = [0, 0, 1, .15]
		App.get_running_app().root.validStatus = True

class MyScreen(Screen):
	global setupNumber
	global setupList

	inputNames = {0: "Population size", 1: "Number of generations", 2: "Plateau", 3: "Mutation rate"}
	
	populationSize = ParamTextInput(text = "10")
	maxGenerations = ParamTextInput(text = "50")
	plateau = ParamTextInput(text = "20")
	mutationRate = ParamTextInput(text = "0.15")

	selection = Spinner(text = "Roulette", size_hint_y = .7)
	selection.values = ["Roulette", "2", "3"]

	crossover = Spinner(text = "One point", size_hint_y = .7)
	crossover.values = ["One point", "Two points", "Uniform"]

	mutation = Spinner(text = "Flip", size_hint_y = .7) 
	mutation.values = ["Flip", "Uniform", "3"]

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
		setupList.append(["10", "50", "20", "0.15", "Roulette", "One point", "Flip"])
		
		parentLayout = GridLayout(cols = 2, spacing = "10dp")

		self.add_widget(parentLayout)
		self.makeTextInput(parentLayout, self.populationSize, "Population size", 4, 200, 0)
		self.makeTextInput(parentLayout, self.maxGenerations, "Number of generations", 1, 500, 1)
		self.makeTextInput(parentLayout, self.plateau, "Plateau", 1, 500, 2)
		self.makeTextInput(parentLayout, self.mutationRate, "Mutation rate", 0, 1, 3)
		self.makeSpinner(parentLayout, self.selection, "Selection strategy", 4)
		self.makeSpinner(parentLayout, self.crossover, "Crossover strategy", 5)
		self.makeSpinner(parentLayout, self.mutation, "Mutation strategy", 6)
		parentLayout.add_widget(self.validationLabel)

	def updateFromTextInput(self, attIndex, minValue, maxValue, aux, text):
		global currentSetup

		try:
			if(attIndex != 3):
				status = int(minValue) <= int(text) <= int(maxValue)
			else:
				status = float(minValue) <= float(text) <= float(maxValue)
				print(status)

			if status:
				self.unlockInputs()
				self.validationLabel.text = "Parameters are valid!"
				self.validationLabel.valid()
				setupList[currentSetup][attIndex] = text
			else:
				self.blockInputs(attIndex)
				self.validationLabel.invalid("{} must be between {} and {}".format(self.inputNames[attIndex], minValue, maxValue))
		except Exception as e:
			self.blockInputs(attIndex)
			if(attIndex != 3):
				self.validationLabel.invalid("{} must be a integer number".format(self.inputNames[attIndex]))
			else:
				self.validationLabel.invalid("{} must be a float number".format(self.inputNames[attIndex]))

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

	def updateFromSpinner(self, attIndex, aux, text):
		setupList[currentSetup][attIndex] = text

	def newSetup(self):
		global setupNumber
		global currentSetup
		currentSetup += 1

		setupNumber += 1
		setupList.append(["10", "50", "20", "0.15", "Roulette", "One point", "Flip"])

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
	def addVar(self, value):
		global varCounter
		varCounter += 1
		target = self.parent.parent
			
		newVar = MyLabel()
		newVar.setVar("x" + str(varCounter))

		minValue = VarTextInput()
		minValue.setVar("0")

		maxValue = VarTextInput()
		maxValue.setVar("10")

		target.ids.varScrollView.add_widget(newVar)
		target.ids.varScrollView.add_widget(minValue)
		target.ids.varScrollView.add_widget(maxValue)
		varList.append([minValue, maxValue])

		target.ids.varScrollView.height += value

	def removeVar(self, value):
		global varCounter
		global varList

		target = self.parent.parent

		if(varCounter <= 1):
			return

		for child in target.ids.varScrollView.children[:3]:
			target.ids.varScrollView.remove_widget(child)
		
		varCounter -= 1
		del varList[-1]
		target.ids.varScrollView.height -= value

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

	def evolve(self):
		target = App.get_running_app().root
		geneType, func, self.task, nameList = target.getParams()

		#self.finalLog, self.plotFitnessLog, self.plotGenerationLog = mid.main(geneType, varList, func, self.task, setupList, nameList, int(target.ids.simulationNumber.text))
		self.finalLog, self.plotFitnessLog, self.plotGenerationLog = mid.main(geneType, varList, func, self.task, setupList, nameList, 10)


		target.ids.logScrollView.text = self.finalLog[self.logIndex]
		self.nameList = nameList

		self.currentGraph = 1
		target.ids.graphButton1.state = "down"
		target.ids.graphButton2.state = "normal"
		self.makePlot1()

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
		popup = Popup(title = "Log file saved", content = box, size_hint = (.5, .18))
		popup.open()
		box.add_widget(Button(text = "Ok", on_press = lambda x : popup.dismiss()))
		
	def makePlot1(self):
		if not self.plotFitnessLog:
			return

		plt.plotFitness(self.plotFitnessLog, self.task, self.nameList)
		target = App.get_running_app().root
		target.ids.image.clear_widgets()
		target.ids.image.add_widget(FigureCanvasKivyAgg(plt.pyplot.gcf()))
		self.currentGraph = 1

	def makePlot2(self):
		if not self.plotGenerationLog:
			return
			
		plt.plotGenerations(self.plotGenerationLog, self.task, self.nameList)
		target = App.get_running_app().root
		target.ids.image.clear_widgets()
		target.ids.image.add_widget(FigureCanvasKivyAgg(plt.pyplot.gcf()))
		self.currentGraph = 2

	def showPlot(self):
		if(self.currentGraph == 1):
			if not self.plotFitnessLog:
				return
			plt.plotFitness(self.plotFitnessLog, self.task, self.nameList) 
		else:
			plt.plotGenerations(self.plotGenerationLog, self.task, self.nameList)

		plt.pyplot.show()

class APP(App):
	def build(self):
		return TabPanel()

APP().run()