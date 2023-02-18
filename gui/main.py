import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import StringProperty
import os

from login import Login
from connected import Connected
from firstWin import firstWin
from secondWin import secondWin

class screenManager(ScreenManager):
    pass

class AnomalabApp(App):
    ##GLOBAL VARS FOR APP
    title = 'anomalab'
    logo = 'images/logo.jpg'
    userName = ''
    password = ''
    

    ##SCREEN MANAGER
    def build(self):
        screenManager = ScreenManager()
        screenManager.add_widget(Login(name='login'))
        screenManager.add_widget(Connected(name='connected'))

        return screenManager
    
if __name__ == '__main__':
    print('kivy version is: '+kivy.__version__)
    app = AnomalabApp()
    app.run()
    app.root_window.close()









##NOT IN USE FOR NOW
def get_application_config(self):
    if(not self.username):
        return super(AnomalabApp, self).get_application_config()

    conf_directory = self.user_data_dir + '/' + self.username

    if(not os.path.exists(conf_directory)):
        os.makedirs(conf_directory)

    return super(AnomalabApp, self).get_application_config(
        '%s/config.cfg' % (conf_directory)
    )
