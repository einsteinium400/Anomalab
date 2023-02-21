from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition

from gui.popup import show_popup

from kivy.lang import Builder

## IMPORT USERS CONTROLLER

Builder.load_file('gui/login.kv')

class Login(Screen):

    def do_login(self, loginText, passwordText):
        if (loginText == '' or passwordText == ''):
            self.resetForm()
            show_popup("Must enter user name and password")
            return
        
        app = App.get_running_app()
        app.username = loginText
        app.password = passwordText

        ##PUT LOGIN FUNCTION
        ## TRY AND CATCH
        app.usertype = 2
        if (app.usertype > 0):
            self.manager.transition = SlideTransition(direction="left")
            if (app.usertype == 1):
                self.manager.current = 'selectdataset'
            elif (app.usertype == 2):
                self.manager.current = 'dataanalystmenu'
            elif (app.usertype == 3):
                self.manager.current = 'connected'
        else:
            self.resetForm()
            show_popup("Login failed")

    def resetForm(self):
        self.ids['userName'].text = ""
        self.ids['password'].text = ""

