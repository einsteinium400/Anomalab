from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.lang import Builder

Builder.load_file('login.kv')

class Login(Screen):

    def do_login(self, loginText, passwordText):
        app = App.get_running_app()
        app.username = loginText
        app.password = passwordText

        print ('name: '+ app.username+' ,pass: '+ app.password)

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'connected'

    def resetForm(self):
        self.ids['userName'].text = ""
        self.ids['password'].text = ""

