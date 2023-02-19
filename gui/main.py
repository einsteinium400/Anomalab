from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import StringProperty
import os

##screen list
from login import Login
from connected import Connected

class AnomalabApp(App):
    username = StringProperty(None)
    password = StringProperty(None)

    def build(self):
        manager = ScreenManager()

        manager.add_widget(Login(name='login'))
        manager.add_widget(Connected(name='connected'))

         ##by default return the first widget to be added
        return manager

if __name__ == '__main__':
    AnomalabApp().run()
