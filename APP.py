#CREATE VIRTUAL ENVITONMENT IN NOAM COMPUTER: kivy_venv\Scripts\activate

from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import StringProperty, NumericProperty
from kivy.lang import Builder
from kivy.core.window import Window
import json
#table imports
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
#forms imports
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextFieldRect
from kivy.uix.spinner import Spinner

# Controllers import
from Moudles.Databases.DatasetsController import DatasetsController
from Moudles.Models.ModelController import ModelsController
from Moudles.Users.UsersController import UsersController

from gui.popup import show_popup

#SCREENS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#---1---
class Login(Screen):
    def do_login(self, name, password):
        app = MDApp.get_running_app()
        ##MICHAEL PART
        """attemptedLoginUser = None
        try:
            if (name == '' or password == ''):
                raise Exception(f"Must enter user name and password")
            attemptedLoginUser = app.userController.GetUser(name)
            if attemptedLoginUser.VerifyPassword(password) == False:
                raise Exception(f"Incorrect Password")
            app.usertype = attemptedLoginUser.TypeNum()
        except Exception as e:
            self.resetForm()
            show_popup(str(e))
            return
        app.usertype = attemptedLoginUser.TypeNum()
        """
        ##
        app.username = name
        app.usertype = password
        print (f'login: name-{name} pass-{password}')
        self.manager.transition = SlideTransition(direction="left")
        if (app.usertype == 1):
            self.manager.current = 'choosedataset'
        elif (app.usertype == 2):
            self.manager.current = 'dataanalystmenu'
        elif (app.usertype == 3):
            self.manager.current = 'manageusers'
        
    def resetForm(self):
        self.ids['user_name'].text = ""
        self.ids['user_pass'].text = ""
#---2---
class ChooseDataset(Screen):

    ## MICHAEL - PUT get datasets
    ## MICHAEL - datasetsNames = only array of names)
    ## NOAM - DONE
    # datasetsNames = ["lymphography","adult"]
    datasetsController = DatasetsController()
    datasetsNames = datasetsController.GetAllDatasetsNamesList()
    def __init__(self, **kwargs):
        super(ChooseDataset, self).__init__(**kwargs)
        
    def on_choose(self, dataset):
        if (dataset == 'Choose Dataset'):
            show_popup("you must choose dataset")
            return
        app = MDApp.get_running_app()
        
        ## MICHAEL - app.datasetname = dataset name
        # app.datasetname = dataset
        dataSetObject = self.datasetsController.GetDataset(dataset)
        app.datasetname = dataSetObject.Name
        ## MICHAEL - app.datasetID = dataset ID
        app.datasetID = dataSetObject.Id

        ## NOAM - Done

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'query'
#---3---
class Query(Screen):
    attributesRefs=[]
    def __init__(self, **kwargs):
        super(Query, self).__init__(**kwargs)
    def on_enter(self):
        self.datasetsController = DatasetsController()
        self.datasetsNames = self.datasetsController.GetAllDatasetsNamesList()
        ## TODO: Need to find Name
        # self.dataSetObject = self.datasetsController.GetDataset()

        ## NOAM - Need clarification what is the name of the dataset???
        ## It will be for all this class

        ## MICHAEL GET DATASET FEATURE DETAILS
        ## MICHAEL ATTRIBUTES NUMBER
        attributesNumber=3
        ## MICHAEL ATTRIBUTES NAMES
        attributesNames=["attribute1","attribute2","attribute3"]
        ## MICHAEL ATTRIBUTES TYPES (0 - NUMERIC, 1 - CATEGORIAL)
        attributeTypes=[0,0,1]
        ## MICHAEL CATEGORIES FOR EACH CATEGORICAL ATTRIBUTE -- TODO:Add caterogries availble for each item and types
        attributeCategories=["cat1","cat2","cat3","cat4","cat5"]

        for i in range(attributesNumber):
            #print (attributesNames[i] + attributeCategories[i])
            print(self.ids)
            self.ids.attributes_box.add_widget(MDLabel(text=f'{attributesNames[i]}:', halign="center"))
            if (attributeTypes[i]==0):
                self.attributesRefs.append(MDTextFieldRect(multiline=False, hint_text=f"insert here"))
            else:
                self.attributesRefs.append(Spinner(text=attributesNames[i], values=attributeCategories))
            self.ids.attributes_box.add_widget(self.attributesRefs[i])

    def on_apply(self):
        query = []
        for i in range(len(self.attributesRefs)):
            query.append(self.attributesRefs[i].text)
        print (f'query is {query}')
        
        app = MDApp.get_running_app()
        ## MICHAEL - TODO: Work on model controller yet to be done sorry
        ## MICHAEL- get BEST MODEL ID for model ID in app.DatasetID ,if no model return 0
        app.model = 1

        
        ## DANA- SEND QUERY (query - arr of values, ModelID) get answer to app.results=PREDICT(query)
        app.results= {}
        
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'results'

    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'choosedataset'
#---4---
class Results(Screen):
    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'query'
#---5---
class DataAnalystMenu(Screen):
    def chooseScreen(self, screenName):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = screenName
#---6---
class ManageDatasets(Screen):
    def __init__(self, **kwargs):
        super(ManageDatasets, self).__init__(**kwargs)
    def on_enter(self):
        self.datasetsController = DatasetsController()
        ##MICHAEL - GET ALL DATASETS data = [(id, name, attribute number, dataline, timestamp),(another one),(another one)]
        ## NOAM - DONE
        table_width = dp(Window.size[0]*9/50)
        table = MDDataTable(
            pos_hint = {'x': 0.05, 'top': 0.95},
            size_hint= (0.9, 0.9),
            use_pagination = True,
            rows_num = 5,
            pagination_menu_height = '240dp',
            column_data = [
                ("ID", dp (table_width*0.1)),
                ("Name", dp (table_width*0.25)),
                ("Attributes", dp (table_width*0.20)),
                ("Instances", dp (table_width*0.20)),
                ("Time stamp", dp (table_width*0.25)),
            ],
            row_data = self.datasetsController.GetAllDatasetsInfoList()
            # row_data = [
            #     ("1", "lymphography", "19", "148", "22-02-2023, 10:51:12"),
            #     ("2", "adult", "14", "32561", "22-02-2023, 10:50:32"),
            # ]
        )
        self.ids['table_place'].add_widget(table)

    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'dataanalystmenu'        
#---7---
class CrudDatasets(Screen):
    ##MICHAEL - GET ONE DATASET(dataset ID)
    ##MICHAEL - SAMPLE OF UPDATE DATASET METHOD
    ##MICHAEL - SAMPLE OF DELETE DATASET METHOd
    ##MICHAEL - SAMPLE OF CREATE DATASET METHOd
    pass
#---8---
class ManageDistanceFunctions(Screen):
    def __init__(self, **kwargs):
        super(ManageDistanceFunctions, self).__init__(**kwargs)
    def on_enter(self):
        table_width = dp(Window.size[0]*9/50)
        table = MDDataTable(
            pos_hint = {'x': 0.05, 'top': 0.95},
            size_hint= (0.9, 0.9),
            use_pagination = True,
            rows_num = 5,
            pagination_menu_height = '240dp',
            column_data = [
                ("ID", dp (table_width*0.2)),
                ("Name", dp (table_width*0.35)),
                ("Time stamp", dp (table_width*0.45)),
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
    ##MICHAEL - GET ONE DISTANCE FUNCTION(dataset ID)
    ##MICHAEL - SAMPLE OF UPDATE DISTANCE FUNCTION METHOD
    ##MICHAEL - SAMPLE OF DELETE DISTANCE FUNCTION METHOd
    ##MICHAEL - SAMPLE OF CREATE DISTANCE FUNCTION METHOd
    pass
#---10---
class UpdateModels(Screen):
    def __init__(self, **kwargs):
        ##MICHAEL - data=GET ALL MODELS FUNCTION()
        ##MICHAEL - datasetIDlist=ID's of ALL DATASETS FUNCTION()
        ##MICHAEL - distancefunctionsIDlist=ID's of ALL Distance functions FUNCTION()
        super(UpdateModels, self).__init__(**kwargs)
    def on_enter(self):
        table_width = dp(Window.size[0]*9/50)
        table = MDDataTable(
            pos_hint = {'x': 0.05, 'top': 0.95},
            size_hint= (0.9, 0.9),
            check = True,
            use_pagination = True,
            rows_num = 5,
            pagination_menu_height = '240dp',
            column_data = [
                #HERE COME CHECK MARK width
                ("ID", dp (table_width*0.1)),
                ("Model Name", dp (table_width*0.18)),
                ("Dataset", dp (table_width*0.18)),
                ("Distance Function", dp (table_width*0.18)),
                ("SSE", dp (table_width*0.1)),
                ("Time stamp", dp (table_width*0.23)),
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
        self.manager.current = 'dataanalystmenu'

    ##MICHAEL - SAMPLE OF UPDATE MODEL FUNCTION METHOD
    ##MICHAEL - SAMPLE OF DELETE DISTANCE FUNCTION METHOd
    ##MICHAEL - SAMPLE OF CREATE DISTANCE FUNCTION METHOd
#---11---
class ManageUsers(Screen):
    def __init__(self, **kwargs):
        super(ManageUsers, self).__init__(**kwargs)
    def on_enter(self):
        ##MICHAEL - GET ALL USERS data = [(id, name, attribute number, dataline, timestamp),(another one),(another one)]
        table_width = dp(Window.size[0]*9/50)
        self.table = MDDataTable(
            pos_hint = {'x': 0.05, 'top': 0.95},
            size_hint= (0.9, 0.9),
            use_pagination = True,
            rows_num = 5,
            pagination_menu_height = '240dp',
            column_data = [
                ("User-ID", dp (table_width*0.2)),
                ("User-Name", dp (table_width*0.3)),
                ("User-Password", dp (table_width*0.3)),
                ("User-Type", dp (table_width*0.2)),
            ],
            row_data = [
                ("1", "reg", "reg", "regular"),
                ("2", "data", "data", "analyst"),
                ("3", "admin", "admin", "admin"),
            ]
        )
        self.table.bind(on_row_press=self.row_press)
        self.ids['table_place'].add_widget(self.table)
    # Function for row presses
    def row_press(self, instance_table, instance_row):
        #Called when a table row is clicked
        print(instance_table, instance_row)
        index = instance_row.index
        cols_num = len(instance_table.column_data)
        row_num = int(index/cols_num)
        print (f'press on row_num is: {row_num}')
        print (f'ID of pressed line is: {self.table.row_data[row_num][0]}')
        app = MDApp.get_running_app()
        app.user_id = int(self.table.row_data[row_num][0])
        app.jsonItem = {'id':int(self.table.row_data[row_num][0]),
                        'name':self.table.row_data[row_num][1],
                        'password':self.table.row_data[row_num][2],
                        'type':self.table.row_data[row_num][3],
                        }
        print (app.jsonItem)
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'cruduser'
    # Function for add user
    def on_add(self):
        app = MDApp.get_running_app()
        app.jsonItem = {}
        
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'cruduser'
    # Function for go back to login page
    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
#---12---
class CrudUser(Screen):
    def __init__(self, **kwargs):
        super(CrudUser, self).__init__(**kwargs)
    def on_enter(self):
        if (app.jsonItem=={}):
            self.ids['header'].text= "New User"
            self.ids['name'].hint_text= "Name"
            self.ids['password'].hint_text= "Password"
            self.ids['type'].hint_text= "type"
        else:
            self.ids['header'].text= app.jsonItem.id
            self.ids['name'].hint_text= app.jsonItem.name
            self.ids['password'].hint_text= app.jsonItem.password
            self.ids['type'].hint_text= app.jsonItem.type
    ##MICHAEL - SAMPLE OF CREATE USER METHOd
    def on_delete(self):
        ## MICHAEL - DELETE USER
        print (f"id: {self.ids['header']}, name: {self.ids['name']}, password: {self.ids['password']}, type: {self.ids['type']}")
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'manageusers'
    def on_update(self):
        ## MICHAEL - UPDATE USER
        print (f"id: {self.ids['header']}, name: {self.ids['name']}, password: {self.ids['password']}, type: {self.ids['type']}")
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'manageusers'
    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'manageusers'
#---13---
class ChooseModels(Screen):
    pass
#---14---
class AnalystResults(Screen):
    pass
# WINDOW MANAGER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class AnomalabApp(MDApp):
    logo = StringProperty('gui/images/logo.jpg')
    icon = StringProperty('gui/images/icon.jpg')
    title = StringProperty('Anomalab')
    userController=UsersController()
    datasetController=DatasetsController()
    modelController=ModelsController()
    #PUT DISTANCE FUNCTION CONTROLLER
    username = StringProperty(None)
    usertype = NumericProperty(None)
    datasetname = StringProperty(None)
    datasetID = NumericProperty(None)
    modelID = NumericProperty(None)
    userID = NumericProperty(None)
    distancefunctionID = NumericProperty(None)
    jsonItem = {}
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file('App.kv')
# MAIN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
    app = AnomalabApp()
    Window.fullscreen = False
    Window.minimum_height = 600
    Window.minimum_width = 800
    app.run()
    app.root_window.close()
