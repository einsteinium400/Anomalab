from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_file('grid.kv')

class MyGridLayout(Widget):

    name = ObjectProperty(None)
    password = ObjectProperty(None)

    def press(self):
        name = self.name.text
        password = self.password.text

        print(f'Hello {name}, your password in {password}') #DEBUGGING
        #self.add_widget(Label(text=f'Name: {name}, password: {password}'))

        #Clear the input boxes
        self.name.text = ""
        self.password.text = ""


class LoginApp(App):
    def build(self):
        return MyGridLayout()

if __name__ == '__main__':
    LoginApp().run()