from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

def show_popup(msg):
    Box=BoxLayout(orientation= "vertical", padding = 10, spacing = 10)
    label=Label(text = msg, bold = True, font_size = 24)
    button=Button(text = "Close Me!", font_size = 16)
    Box.add_widget(label)
    Box.add_widget(button)

    popupWindow = Popup(title ="Alert",
                        content = Box,
                        size_hint=(None, None), size=(600, 200),
                        auto_dismiss=True)
    button.bind(on_press=popupWindow.dismiss)
    # open popup window
    popupWindow.open()