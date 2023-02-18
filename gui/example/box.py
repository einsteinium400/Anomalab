from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
#from kivy.uix.image import Image

Builder.load_file('box.kv')

class MyLayout(Widget):
    def press(self):
        #Create vars for widgets
        name = self.ids.name_input.text
        password = self.ids.pass_input.text
        
        #update the label
        self.ids.name_label.text=f'Hello {name}'
        self.ids.pass_label.text=password

        #clear input boxes
        self.ids.name_input.text=''
        self.ids.pass_input.text=''


class inheritApp(App):
    def build(self):
        Window.clearcolor = (1,1,1,1)
        return MyLayout()

if __name__ == '__main__':
    inheritApp().run()