#CREATE VIRTUAL ENVITONMENT IN NOAM COMPUTER: kivy_venv\Scripts\activate

from view.APP import AnomalabApp
from kivy.core.window import Window

if __name__ == '__main__':
    app = AnomalabApp()
    Window.fullscreen = False
    Window.minimum_height = 600
    Window.minimum_width = 800
    app.run()
    app.root_window.close()