from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition

from kivy.lang import Builder

Builder.load_file('gui/dataanalystmenu.kv')

class DataAnalystMenu(Screen):
    
    def on_query(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'selectdataset'

    def on_datasets(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'datasetsmanager'

    def on_distancefunctions(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'connected'

    def on_models(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'connected'
