from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import StringProperty, NumericProperty

##screen list
from gui.login import Login
from gui.connected import Connected
from gui.selectdataset import SelectDataset
from gui.insertquery import InsertQuery

class AnomalabApp(App):
    username = StringProperty(None)
    password = StringProperty(None)
    usertype = NumericProperty(None)
    datasetname = StringProperty(None)
    datasetID = NumericProperty(None)

    def build(self):
        manager = ScreenManager()

        manager.add_widget(Login(name='login'))
        manager.add_widget(Connected(name='connected'))
        manager.add_widget(SelectDataset(name='selectdataset'))
        manager.add_widget(InsertQuery(name='insertquery'))

         ##by default return the first widget to be added
        return manager

if __name__ == '__main__':
    AnomalabApp().run()
