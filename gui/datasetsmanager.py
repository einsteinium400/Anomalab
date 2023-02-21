from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.lang import Builder
from kivy.uix.widget import Widget

from gui.popup import show_popup

## IMPORT DATASET CONTROLLER

Builder.load_file('gui/datasetsmanager.kv')

class DatasetsManager(Screen):
    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'dataanalystmenu'



