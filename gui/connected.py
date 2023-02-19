
from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.lang import Builder

Builder.load_file('connected.kv')

class Connected(Screen):
    def disconnect(self):
        
        app = App.get_running_app()
        print ('disconnect name and pass were: '+ app.username + ' ' + app.password)

        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()