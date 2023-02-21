from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import StringProperty, NumericProperty
from kivy.lang import Builder

from gui.popup import show_popup

Builder.load_file('App.kv')

#SCREENS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#---1---
class Login(Screen):
    def do_login(self, name, password):
        if (name == '' or password == ''):
            self.resetForm()
            show_popup("Must enter user name and password")
            return
    
        app = MDApp.get_running_app()
        app.username = name
        print (f'login: name-{name} pass-{password}')

        ##PUT LOGIN FUNCTION
        app.usertype = 2
        if (app.usertype > 0):
            self.manager.transition = SlideTransition(direction="left")
            if (app.usertype == 1):
                self.manager.current = 'selectdataset'
            elif (app.usertype == 2):
                self.manager.current = 'dataanalystmenu'
            elif (app.usertype == 3):
                pass
                ##HERE WILL COME MANAGE USERS SCREEN
        else:
            self.resetForm()
            show_popup("Login failed")

    def resetForm(self):
        self.ids['user_name'].text = ""
        self.ids['user_pass'].text = ""
#---2---
class ChooseDataset(Screen):
    pass
#---3---
class Query(Screen):
    pass
#---4---
class Results(Screen):
    pass
#---5---
class DataAnalystMenu(Screen):
    pass
#---6---
class ManageDatasets(Screen):
    pass
#---7---
class CrudDatasets(Screen):
    pass
#---8---
class ManageDistanceFunctions(Screen):
    pass
#---9---
class CrudDistanceFunctions(Screen):
    pass
#---10---
class UpdateModels(Screen):
    pass
#---11---
class ManageUsers(Screen):
    pass
#---12---
class CrudUser(Screen):
    pass
#---13---
class ChooseModels(Screen):
    pass
#---14---
class AnalystResults(Screen):
    pass
# WINDOW MANAGER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~``
class AnomalabApp(MDApp):
    icon = StringProperty('gui/images/logo.jpg')
    title = StringProperty('Anomalab')
    username = StringProperty(None)
    usertype = NumericProperty(None)
    datasetname = StringProperty(None)
    datasetID = NumericProperty(None)
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        WindowManager = ScreenManager()
        #---1---
        WindowManager.add_widget(Login(name='login'))
        #---2---
        WindowManager.add_widget(ChooseDataset(name='choosedataset'))
        #---3---
        WindowManager.add_widget(Query(name='query'))
        #---4---
        WindowManager.add_widget(Results(name='results'))
        #---5---
        WindowManager.add_widget(DataAnalystMenu(name='dataanalystmenu'))
        #---6---
        WindowManager.add_widget(ManageDatasets(name='managedatasets'))
        #---7---
        WindowManager.add_widget(CrudDatasets(name='cruddatasets'))
        #---8---
        WindowManager.add_widget(ManageDistanceFunctions(name='managedistancefunctions'))
        #---9---
        WindowManager.add_widget(CrudDistanceFunctions(name='cruddistancefunctions'))
        #---10---
        WindowManager.add_widget(UpdateModels(name='updatemodels'))
        #---11---
        WindowManager.add_widget(ManageUsers(name='manageusers'))
        #---12---
        WindowManager.add_widget(CrudUser(name='cruduser'))
        #---13---
        WindowManager.add_widget(ChooseModels(name='choosemodels'))
        #---14---
        WindowManager.add_widget(AnalystResults(name='analystresults'))
        
        return WindowManager

## MAIN
if __name__ == '__main__':
    app = AnomalabApp()
    app.run()
    app.root_window.close()
