import kivy
kivy.require("1.11.0")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton

class StudentListButton(ListItemButton):
    pass    

class StudentDB(BoxLayout):
    first_name_input = ObjectProperty()
    last_name_input = ObjectProperty()
    student_list = ObjectProperty()

    def submit(self):
        pass

    def delete(self):
        pass

    def replace(self):
        pass
    
class StudentDBApp(App):
    def build(self):
        return StudentDB()

app = StudentDBApp()
app.run()
