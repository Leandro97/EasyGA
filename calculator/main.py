import kivy
kivy.require("1.11.0")

from kivy.app import App
from kivy.uix.gridlayout import GridLayout

class GridLayout(GridLayout):
    def calculate(self, expression):
        if expression:
            try:
                self.display.text = str(eval(expression))
            except Exception:
                self.display.text = "Error"

class CalculatorApp(App):
    def build(self):
        return  GridLayout()

app = CalculatorApp()

app.run()
