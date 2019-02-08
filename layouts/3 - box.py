import kivy 
kivy.require('1.11.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class BoxingApp(App):
    def build(self):
        return BoxLayout()

app = BoxingApp()
app.run()
