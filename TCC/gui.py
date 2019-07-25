# -*- coding: utf-8 -*-
import kivy
from kivy.app import App
from kivy import uix
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.config import Config
from functools import partial
from kivy.properties import StringProperty
from kivy.lang import Builder
import middle as mid

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

	def __init__(self, **kwargs):
		super(TabPanel, self).__init__(**kwargs)

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

class MyTextInput(TextInput):
	def __init__(self, **kwargs):
		super(MyTextInput, self).__init__(**kwargs)
		self.write_tab = False
		self.multiline = False
		self.size_hint_y = .55

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

		newName = MyTextInput()

		box.add_widget(newName)
		box.add_widget(insideBox)

	def changeName(self, text, popup):
		global currentSetup
		global nameList

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
		
		save = MyButton(text = "Delete")
		save.bind(on_press = lambda x : self.deleteSetup(popup))

		cancel = MyButton(text = "Cancel")
		cancel.bind(on_press = lambda x : popup.dismiss())

		box.add_widget(save)
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
			print("opa")
			self.spinner.text = self.spinner.values[1]
			del setupList[0]
			del self.spinner.values[0]	

		nameList = self.spinner.values
		popup.dismiss()

class MyScreen(Screen):
	global setupNumber
	global setupList
	
	populationSize = MyTextInput(text = "10")
	maxGenerations = MyTextInput(text = "50")
	plateau = MyTextInput(text = "20")
	mutationRate = MyTextInput(text = "0.15")

	selection = Spinner(text = "Roulette", size_hint_y = .7)
	selection.values = ["Roulette", "2", "3"]

	crossover = Spinner(text = "One point", size_hint_y = .7)
	crossover.values = ["One point", "Two points", "Uniform"]

	mutation = Spinner(text = "Flip", size_hint_y = .7) 
	mutation.values = ["Flip", "Uniform", "3"]


	def makeInput(self, layout, widget, labelText, index):
		paramLayout = BoxLayout(orientation = "vertical")
		paramLabel = MyLabel(text = labelText, color = TEXT_COLOR)

		widget.bind(text = partial(self.updateDict, index))

		paramLayout.add_widget(paramLabel)
		paramLayout.add_widget(widget)
		layout.add_widget(paramLayout)

	def __init__(self, **kwargs):
		super(MyScreen, self).__init__(**kwargs)
		setupList.append(["10", "50", "20", "0.15", "Roulette", "One point", "Flip"])
		
		parentLayout = GridLayout(cols = 2, spacing = "10dp")

		self.add_widget(parentLayout)
		self.makeInput(parentLayout, self.populationSize, "Population size", 0)
		self.makeInput(parentLayout, self.maxGenerations, "Maximum number of generations", 1)
		self.makeInput(parentLayout, self.plateau, "Plateau", 2)
		self.makeInput(parentLayout, self.mutationRate, "Mutation rate", 3)
		self.makeInput(parentLayout, self.selection, "Selection strategy", 4)
		self.makeInput(parentLayout, self.crossover, "Crossover strategy", 5)
		self.makeInput(parentLayout, self.mutation, "Mutation strategy", 6)
	
	def updateDict(self, attIndex, aux, text):
		global currentSetup
		#print("Setup atual", currentSetup, text)
		setupList[currentSetup][attIndex] = text
		#print(self.setupList)

	def newSetup(self):
		global setupNumber
		global currentSetup
		currentSetup += 1

		#print("Setup atual", currentSetup)

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
	global task
	logIndex = 0
	finalLog = []

	def __init__(self, **kwargs):
		super(SimulationLayout, self).__init__(**kwargs)

	def evolve(self):
		target = App.get_running_app().root
		geneType, func, task, nameList = target.getParams()

		self.finalLog = mid.main(geneType, varList, func, task, setupList, nameList, int(target.ids.simulationNumber.text))

		target.ids.logScrollView.text = self.finalLog[self.logIndex]

	def next(self):
		try:
			self.logIndex = 0 if(self.logIndex + 1 >= len(setupList)) else self.logIndex + 1
			target = App.get_running_app().root
			target.ids.logScrollView.text = self.finalLog[self.logIndex]
		except:
			pass

	def previous(self):
		try:
			self.logIndex = len(setupList) - 1 if(self.logIndex <= 0) else self.logIndex - 1
			target = App.get_running_app().root
			target.ids.logScrollView.text = self.finalLog[self.logIndex]
		except:
			pass


class GUI(App):
	def build(self):
		return TabPanel()

GUI().run()