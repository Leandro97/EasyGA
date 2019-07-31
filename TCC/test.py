from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.bubble import Bubble
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty
from functools import partial
from kivy.clock import Clock

KV = """

<ValidateLabel>:
    size_hint: (None, None)
    size: (100, 10)
    Label:
        text: "Must be a float"
        color: 1, 1, 1, 1


<MyInput>:
    foreground_color: (0,1,0,1) if self.validated else (1,0,0,1)


TestInput:

"""


class MyInput(TextInput):
    validated = BooleanProperty(False)

class ValidateLabel(Bubble):
    validated = False

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
        self.bubble.text = "Number must be between {} and {}".format(minValue, maxValue)

        try:
            status = float(minValue) <= float(value) <= float(maxValue)
        except Exception as e:
            status = False
            self.bubble.text = "Input must be a number"

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
        Clock.schedule_once(self.load)
        
    def load(self, dt):
        self.add_widget(self.floatInput)

class TestApp(App):
    def build(self):
        return Builder.load_string(KV)


TestApp().run()