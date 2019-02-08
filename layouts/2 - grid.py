import kivy 
kivy.require('1.11.0')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout

class GridingApp(App):
    def build(self):
        return GridLayout()

app = GridingApp()
app.run()
