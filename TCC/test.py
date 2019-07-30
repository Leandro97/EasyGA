from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.bubble import Bubble
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty

KV = """

<ValidateLabel>:
    size_hint: (None, None)
    size: (280, 60)
    Label:
        id: label
        text: "Must be a float"


<MyInput>:
    foreground_color: (0,1,0,1) if root.validated else (1,0,0,1)


FloatInput:

"""


class MyInput(TextInput):
    validated = BooleanProperty(False)


class FloatInput(FloatLayout):
    bubble_showed = True

    def __init__(self, **kwargs):
        super(FloatInput, self).__init__(**kwargs)
        self.input = MyInput()
        self.input.bind(text=self.validate)
        self.add_widget(self.input)
        self.bubble = ValidateLabel()
        self.add_widget(self.bubble)

    def validate(self, input, value, min_value=15., max_value=25.):
        self.bubble.ids.label.text = "Number must be between {} and {}".format(min_value, max_value)
        try:
            print(min_value, max_value)
            status = float(min_value) <= float(value) <= float(max_value)
        except Exception as e:
            status = False
            self.bubble.ids.label.text = "Input must be a number"

        if not status:
            if not self.bubble_showed:
                self.input.validated = False
                self.add_widget(self.bubble)
                self.bubble_showed = True
        else:
            print("bubble removed")
            self.input.validated = True
            self.remove_widget(self.bubble)
            self.bubble_showed = False


class ValidateLabel(Bubble):
    validated = False


class TestApp(App):

    def build(self):
        return Builder.load_string(KV)


TestApp().run()