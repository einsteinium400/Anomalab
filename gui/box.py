from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_file('box.kv')

class MyLayout(Widget):
    pass

class BoxApp(App):
    def build(self):
        return MyLayout()

if __name__ == '__main__':
    BoxApp().run()