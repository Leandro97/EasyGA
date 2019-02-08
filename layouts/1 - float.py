import kivy 
kivy.require('1.11.0')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

class FloatingApp(App):
    def build(self):
        return FloatLayout()

app = FloatingApp()
app.run()
