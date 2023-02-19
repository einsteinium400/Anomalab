from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.lang import Builder
from kivy.uix.widget import Widget

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner

from gui.popup import show_popup



## IMPORT DATASET CONTROLLER

Builder.load_file('gui/insertquery.kv')

class InsertQuery(Screen):
    attributesRefs = []
    def create_attributes_form(self):
        ##HERE NEED TO READ ATTRIBUTES TABLE
        attributesNumber=3
        attributesNames=["attribute1","attribute2","attribute3"]
        attributeTypes=[0,0,1]
        attributeCategories=["cat1","cat2","cat3","cat4","cat5"]
        for i in range(attributesNumber):
            print (attributesNames[i] + attributeCategories[i])
            self.ids.attributes_box.add_widget(Label(text=attributesNames[i]))
            if (attributeTypes[i]==0):
                self.attributesRefs.append(TextInput(text='', multiline=False))
            else:
                self.attributesRefs.append(Spinner(text=attributesNames[i], values=attributeCategories))
            self.ids.attributes_box.add_widget(self.attributesRefs[i])
    
    def on_apply(self):
        print ("query:")
        for i in range(len(self.attributesRefs)):
            print (self.attributesRefs[i].text),
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'connected'
        

    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'selectdataset'



