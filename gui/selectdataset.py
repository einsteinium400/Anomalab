from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition

from gui.popup import show_popup

from kivy.lang import Builder

## IMPORT DATASET CONTROLLER

Builder.load_file('gui/selectdataset.kv')

class SelectDataset(Screen):
    
    
    ##HERE GET DATASETS NAME
    datasetsName=["dataset1","dataset2"]
    
    def on_apply(self, choosenDataset):
        if (choosenDataset=="Choose Dataset"):
            show_popup("No dataset choose")
        else:
            app = App.get_running_app()
            app.datasetname = choosenDataset
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'insertquery'

