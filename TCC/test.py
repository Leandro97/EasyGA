from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.bubble import Bubble
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty
from functools import partial
from kivy.clock import Clock
from kivy.uix.label import Label

KV = """
TestInput:
"""

class MyInput(TextInput):
    validated = BooleanProperty(False)

class ValidateLabel(Bubble):
    validated = False
    label = Label(text = "Must be a float", color = (1, 1, 1, 1))

    def __init__(self, **kwargs):
        super(ValidateLabel, self).__init__(**kwargs)
        self.add_widget(self.label)

class FloatInput(FloatLayout):
    bubble_showed = False

    def __init__(self, widget, minValue, maxValue, **kwargs):
        super(FloatInput, self).__init__(**kwargs)
        self.input = widget
        self.input.bind(text = partial(self.validate, minValue, maxValue))
        self.add_widget(self.input)
        self.bubble = ValidateLabel()
        self.bubble.size_hint_y = .1
        

    def validate(self, minValue, maxValue, input, value):
        self.bubble.label.text = "Number must be between {} and {}".format(minValue, maxValue)
        print(self.bubble.label)
        try:
            status = float(minValue) <= float(value) <= float(maxValue)
        except Exception as e:
            status = False
            self.bubble.label.text = "Input must be a number"

        if not status:
            if not self.bubble_showed:
                self.input.validated = False
                self.add_widget(self.bubble)
                self.bubble_showed = True
                print(self.bubble.text)
        else:
            self.input.validated = True
            self.remove_widget(self.bubble)
            self.bubble_showed = False


class TestInput(BoxLayout):
    newInput = MyInput(text = "2")
    floatInput = FloatInput(newInput, 1.5, 5.8)

    def __init__(self, **kwargs):
        super(TestInput, self).__init__(**kwargs)
        #Clock.schedule_once(self.load)
    #def load(self, dt):
        self.add_widget(self.floatInput)

class TestApp(App):
    def build(self):
        return Builder.load_string(KV)


TestApp().run()