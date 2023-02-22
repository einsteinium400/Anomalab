from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

def show_popup(msg):
    Box=BoxLayout(orientation= "vertical", padding = 10, spacing = 10)
    Label1=Label(text = msg, bold = True, font_size = 32)
    Label2=Label(text = "click outside box to close", font_size = 20)
    Box.add_widget(Label1)
    Box.add_widget(Label2)

    popupWindow = Popup(title ="Alert", content = Box, size_hint =(None, None), size =(400, 200), auto_dismiss=True)
    # open popup window
    popupWindow.open()