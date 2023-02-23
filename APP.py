#CREATE VIRTUAL ENVITONMENT IN NOAM COMPUTER: kivy_venv\Scripts\activate

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import StringProperty, NumericProperty
from kivy.lang import Builder

#table imports
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
#forms imports
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivy.uix.spinner import Spinner

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
        app.usertype = password
        if (app.usertype > 0):
            self.manager.transition = SlideTransition(direction="left")
            if (app.usertype == 1):
                self.manager.current = 'choosedataset'
            elif (app.usertype == 2):
                self.manager.current = 'dataanalystmenu'
            elif (app.usertype == 3):
                pass
                self.manager.current = 'manageusers'
        else:
            self.resetForm()
            show_popup("Login failed")

    def resetForm(self):
        self.ids['user_name'].text = ""
        self.ids['user_pass'].text = ""
#---2---
class ChooseDataset(Screen):
    datasetsName = ["lymphography","adult"]
    
    def __init__(self, **kwargs):
        super(ChooseDataset, self).__init__(**kwargs)
        
    def on_choose(self, dataset):
        if (dataset == 'Choose Dataset'):
            show_popup("you must choose dataset")
            return
        app = MDApp.get_running_app()
        app.datasetname = dataset
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'query'

#---3---
class Query(Screen):
    attributesRefs=[]
    def __init__(self, **kwargs):
        super(Query, self).__init__(**kwargs)
        attributesNumber=3
        attributesNames=["attribute1","attribute2","attribute3"]
        attributeTypes=[0,0,1]
        attributeCategories=["cat1","cat2","cat3","cat4","cat5"]
        for i in range(attributesNumber):
            print (attributesNames[i] + attributeCategories[i])
            self.ids.attributes_box.add_widget(MDLabel(text=attributesNames[i]))
            if (attributeTypes[i]==0):
                self.attributesRefs.append(MDTextField(text='', multiline=False))
            else:
                self.attributesRefs.append(Spinner(text=attributesNames[i], values=attributeCategories))
            self.ids.attributes_box.add_widget(self.attributesRefs[i])

    def on_apply(self):
        print ("query:")
        for i in range(len(self.attributesRefs)):
            print (self.attributesRefs[i].text)
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'results'
        

    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'choosedataset'
#---4---
class Results(Screen):
    pass
#---5---
class DataAnalystMenu(Screen):
    def chooseScreen(self, screenName):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = screenName
    
#---6---
class ManageDatasets(Screen):
    ## LOAD FROM CONTROLLER
    def __init__(self, **kwargs):
        super(ManageDatasets, self).__init__(**kwargs)
        table = MDDataTable(
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            use_pagination = True,
            rows_num = 5,
            pagination_menu_height = '240dp',
            column_data = [
                ("ID", dp (20)),
                ("Name", dp (40)),
                ("Attributes", dp (30)),
                ("Instances", dp (30)),
                ("Time stamp", dp (50)),
            ],
            row_data = [
                ("1", "lymphography", "19", "148", "22-02-2023, 10:51:12"),
                ("2", "adult", "14", "32561", "22-02-2023, 10:50:32"),
            ]
        )
        self.ids['table_place'].add_widget(table)

    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'dataanalystmenu'
          
#---7---
class CrudDatasets(Screen):
    pass
#---8---
class ManageDistanceFunctions(Screen):
    ## LOAD FROM CONTROLLER
    def __init__(self, **kwargs):
        super(ManageDistanceFunctions, self).__init__(**kwargs)
        table = MDDataTable(
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            use_pagination = True,
            rows_num = 5,
            pagination_menu_height = '240dp',
            column_data = [
                ("ID", dp (20)),
                ("Name", dp (40)),
                ("Time stamp", dp (50)),
            ],
            row_data = [
                ("1", "Hamming", "22-02-2023, 10:51:12"),
                ("2", "Euclidian", "22-02-2023, 10:50:32"),
                ("3", "Mixed", "22-02-2023, 10:50:32"),
            ]
        )
        self.ids['table_place'].add_widget(table)

    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'dataanalystmenu'
#---9---
class CrudDistanceFunctions(Screen):
    pass
#---10---
class UpdateModels(Screen):
    ## LOAD FROM CONTROLLER
    def __init__(self, **kwargs):
        super(UpdateModels, self).__init__(**kwargs)
        table = MDDataTable(
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            check = True,
            use_pagination = True,
            rows_num = 5,
            pagination_menu_height = '240dp',
            column_data = [
                ("ID", dp (20)),
                ("Model Name", dp (40)),
                ("Dataset", dp (40)),
                ("Distance Function", dp (40)),
                ("SSE", dp (20)),
                ("Time stamp", dp (50)),
            ],
            row_data = [
                ("1-1", "ly-Ha", "lymphography", "Hamming", "5.2", "22-02-2023, 10:51:12"),
                ("1-2", "ly-Eu", "lymphography", "Euclidian", "4.7", "22-02-2023, 10:50:32"),
                ("1-3", "ly-Mi", "lymphography", "Mixed", "3.7", "22-02-2023, 10:50:32"),
                ("2-1", "ad-Ha", "adult", "Hamming", "14.2", "22-02-2023, 10:51:12"),
                ("2-2", "ad-Eu", "adult", "Euclidian", "5.5", "22-02-2023, 10:50:32"),
                ("2-3", "ad-Mi", "adult", "Mixed", "2.5", "22-02-2023, 10:50:32"),
            ]
        )
        table.bind(on_check_press=self.checked)
        table.bind(on_row_press=self.row_checked)
        self.ids['table_place'].add_widget(table)
    # Function for check presses
    def checked (self, instance_table, current_row):
        print(instance_table, current_row)
    # Function for row presses
    def row_checked(self, instance_table, instance_row):
        print(instance_table, instance_row)

    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'choosedataset'
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
    logo = StringProperty('gui/images/logo.jpg')
    icon = StringProperty('gui/images/icon.jpg')
    title = StringProperty('Anomalab')
    username = StringProperty(None)
    usertype = NumericProperty(None)
    datasetname = StringProperty(None)
    datasetID = NumericProperty(None)
    def build(self):
        self.theme_cls.theme_style = "Light"
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
