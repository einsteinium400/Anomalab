from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition

from kivy.lang import Builder



Builder.load_file('gui/regularresults.kv')

class RegularResults(Screen):
    
    def on_apply(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'insertquery'

    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'selectdataset'

