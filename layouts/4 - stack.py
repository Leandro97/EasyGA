import kivy 
kivy.require('1.11.0')

from kivy.app import App
from kivy.uix.stacklayout import StackLayout

class StackingApp(App):
    def build(self):
        return StackLayout()

app = StackingApp()
app.run()
