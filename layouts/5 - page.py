import kivy 
kivy.require('1.11.0')

from kivy.app import App
from kivy.uix.pagelayout import PageLayout

class PagingApp(App):
    def build(self):
        return PageLayout()

app = PagingApp()
app.run()
