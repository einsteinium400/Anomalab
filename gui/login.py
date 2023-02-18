from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition

class Login(Screen):
    def do_login(self, userNameText, passwordText):
        app = App.get_running_app()

        app.userName = userNameText
        app.password = passwordText

        ##here put Login function
               
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'connected'

    def resetForm(self):
        self.ids['userName'].text = ""
        self.ids['password'].text = ""

