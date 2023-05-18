#CREATE VIRTUAL ENVITONMENT IN NOAM COMPUTER: kivy_venv\Scripts\activate
if __name__ == '__main__':
    from multiprocessing import freeze_support
    from view.APP import AnomalabApp
    from kivy.core.window import Window


    freeze_support()
    app = AnomalabApp()
    Window.fullscreen = False
    Window.minimum_height = 600
    Window.minimum_width = 800
    app.run()
    app.root_window.close()