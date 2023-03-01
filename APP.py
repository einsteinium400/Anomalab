#CREATE VIRTUAL ENVITONMENT IN NOAM COMPUTER: kivy_venv\Scripts\activate

from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
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
        print (f'login: name-{name} pass-{password}')
        app = MDApp.get_running_app()
        try:
            if (name == '' or password == ''):
                raise Exception(f"Must enter user name and password")
            app.userObject = app.userController.LoginUser(name, password)
        except Exception as e:
            self.resetForm()
            show_popup(str(e))
            return
        print (f'login successful: {str(app.userObject)} type is: {app.userObject.Type}')
        self.manager.transition = SlideTransition(direction="left")
        if (app.userObject.Type == 'regular'):
            self.manager.current = 'choosedataset'
        elif (app.userObject.Type == 'analyst'):
            self.manager.current = 'dataanalystmenu'
        elif (app.userObject.Type == 'admin'):
            self.manager.current = 'manageusers'
    def resetForm(self):
        self.ids['user_name'].text = ""
        self.ids['user_pass'].text = ""
    def close(self):
        MDApp.get_running_app().stop()
#---2---
class ChooseDataset(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()
        self.datasetsNames = app.datasetController.GetAllDatasetsNamesList()
        if (self.datasetsNames == []):
            show_popup("THERE ARE NO DATASETS IN THE SYSTEM")
            self.manager.transition = SlideTransition(direction="right")
            self.manager.current = 'login'
        self.ids['spinner_id'].values = self.datasetsNames
           
    def on_choose(self, dataset):
        if (dataset == 'Choose Dataset'or dataset == "THERE ARE NO DATASETS IN THE SYSTEM" or dataset == ""):
            print (f'choose dataset: {dataset}')
            show_popup("you must choose dataset")
            return
        app = MDApp.get_running_app()
        app.dataSetObject = app.datasetController.GetDataset(dataset)
        print (f'choose dataset name: {app.dataSetObject.Name}')
        #IF USER IS REG GO TO QUERY ELSE GO TO CHOOSE MODELS
        self.manager.transition = SlideTransition(direction="left")
        if (app.userObject.Type==1):
            self.manager.current = 'query'
        else:
            self.manager.current = 'choosemodels'
    
    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
#---3---
class Query(Screen):
    attributesRefs=[]
    def on_enter(self):
        app = MDApp.get_running_app()
        ## TODO: Need to find Name
        ## MICHEAL SEE THAT app.dataSetObject contain the choosen dataset object
        ## MICHAEL GET DATASET FEATURE DETAILS
        ## ATTRIBUTES NUMBER
        attributesNumber=3
        ## ATTRIBUTES NAMES
        attributesNames=["attribute1","attribute2","attribute3"]
        ## ATTRIBUTES TYPES (0 - NUMERIC, 1 - CATEGORIAL)
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

    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
#---4---
class Results(Screen):
    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'query'
    
    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
#---5---
class DataAnalystMenu(Screen):
    def chooseScreen(self, screenName):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = screenName
    
    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
#---6---
class ManageDatasets(Screen):
    def on_enter(self):
        table_width = dp(Window.size[0]*9/50)
        #print (app.datasetController.GetAllDatasetsInfoList())
        app = MDApp.get_running_app()
        datasetsData = app.datasetController.GetAllDatasetsInfoList()
        self.table = MDDataTable(
            pos_hint = {'x': 0.05, 'top': 0.95},
            size_hint= (0.9, 0.9),
            use_pagination = True,
            rows_num = 5,
            pagination_menu_height = '240dp',
            column_data = [
                ("Name", dp (table_width*0.25)),
                ("Attributes", dp (table_width*0.25)),
                ("Instances", dp (table_width*0.25)),
                ("Time stamp", dp (table_width*0.25)),
            ],
            row_data = [
                ("lymphography", "19", "148", "22-02-2023, 10:51:12"),
                ("adult", "14", "32561", "22-02-2023, 10:50:32"),
            ]
        )
        self.table.bind(on_row_press=self.row_press)
        self.ids['table_place'].add_widget(self.table)
    def row_press(self, instance_table, instance_row):
        index = instance_row.index
        cols_num = len(instance_table.column_data)
        row_num = int(index/cols_num)
        print (f'press on row_num is: {row_num}')
        print (f'name of pressed line is: {self.table.row_data[row_num][0]}')
        app = MDApp.get_running_app()
        app.dictionary =  {
            "name": self.table.row_data[row_num][1],
        }
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'uddataset'
    def on_add(self):
        app = MDApp.get_running_app()
        app.dictionary = {}
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'adddataset'
    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'dataanalystmenu'
    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
#---7---
class AddDataset(Screen):
    ##MICHAEL - GET ONE DATASET(dataset ID)
    ##MICHAEL - SAMPLE OF UPDATE DATASET METHOD
    ##MICHAEL - SAMPLE OF DELETE DATASET METHOd
    ##MICHAEL - SAMPLE OF CREATE DATASET METHOd
    mode = ""
    data = []
    def on_enter(self):
        app = MDApp.get_running_app()
        if (app.dictionary=={}):
            self.ids['header'].text= "New Dataset"
            self.mode = "add"
            self.data = []
        else:
            self.ids['header'].text= "dataset name: "+str(app.dictionary['name'])
            #self.idf[...].text= ...
            self.mode = "update"
            self.data = [
                ("name", "categorial", "Dana, Michael, Noam"),
                ("height", "numeric", ""),
                ("grade", "numeric", ""),
            ]
        
        table_width = dp(Window.size[0]*6/50)
        self.table = MDDataTable(
            pos_hint = {'x': 0.05, 'top': 0.95},
            size_hint= (0.9, 0.9),
            use_pagination = True,
            rows_num = 3,
            pagination_menu_height = '240dp',
            column_data = [
                ("Name", dp (table_width*0.25)),
                ("Type", dp (table_width*0.25)),
                ("Values", dp (table_width*0.5)),
            ],
            #row_data = attributes table
            ## MICHAEL - FIX GetDATASET INFO
            
    
            row_data = self.data
        )
        self.table.bind(on_row_press=self.row_press)
        self.ids['attributes_place'].add_widget(self.table)
        
    def row_press(self, instance_table, instance_row):
        index = instance_row.index
        cols_num = len(instance_table.column_data)
        row_num = int(index/cols_num)
        print (f'press on row_num is: {row_num}')
        print (f'ID of pressed line is: {self.table.row_data[row_num][0]}')

    def on_delete(self):
        ## MICHAEL - DELETE Dataset
        print (f"delete dataset: {self.ids['header']}")
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'managedatasets'
    def on_apply(self):
        if (self.mode=="add"):
            ## MICHAEL - CREATE Dataset
            print (f"add dataset: {self.ids['header']}")
        else:
            ## MICHAEL - UPDATE Dataset
            print (f"update dataset: {self.ids['header']}")
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'managedatasets'
    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'managedatasets'
    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
class UDDataset(Screen):
    ##MICHAEL - GET ONE DATASET(dataset ID)
    ##MICHAEL - SAMPLE OF UPDATE DATASET METHOD
    ##MICHAEL - SAMPLE OF DELETE DATASET METHOd
    ##MICHAEL - SAMPLE OF CREATE DATASET METHOd
    mode = ""
    data = []
    def on_enter(self):
        app = MDApp.get_running_app()
        if (app.dictionary=={}):
            self.ids['header'].text= "New Dataset"
            self.mode = "add"
            self.data = []
        else:
            self.ids['header'].text= "dataset name: "+str(app.dictionary['name'])
            #self.idf[...].text= ...
            self.mode = "update"
            self.data = [
                ("name", "categorial", "Dana, Michael, Noam"),
                ("height", "numeric", ""),
                ("grade", "numeric", ""),
            ]
        
        table_width = dp(Window.size[0]*6/50)
        self.table = MDDataTable(
            pos_hint = {'x': 0.05, 'top': 0.95},
            size_hint= (0.9, 0.9),
            use_pagination = True,
            rows_num = 3,
            pagination_menu_height = '240dp',
            column_data = [
                ("Name", dp (table_width*0.25)),
                ("Type", dp (table_width*0.25)),
                ("Values", dp (table_width*0.5)),
            ],
            #row_data = attributes table
            ## MICHAEL - FIX GetDATASET INFO
            
    
            row_data = self.data
        )
        self.table.bind(on_row_press=self.row_press)
        self.ids['attributes_place'].add_widget(self.table)
        
    def row_press(self, instance_table, instance_row):
        index = instance_row.index
        cols_num = len(instance_table.column_data)
        row_num = int(index/cols_num)
        print (f'press on row_num is: {row_num}')
        print (f'ID of pressed line is: {self.table.row_data[row_num][0]}')

    def on_delete(self):
        ## MICHAEL - DELETE Dataset
        print (f"delete dataset: {self.ids['header']}")
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'managedatasets'
    def on_apply(self):
        if (self.mode=="add"):
            ## MICHAEL - CREATE Dataset
            print (f"add dataset: {self.ids['header']}")
        else:
            ## MICHAEL - UPDATE Dataset
            print (f"update dataset: {self.ids['header']}")
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'managedatasets'
    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'managedatasets'
    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
#---8---
class ManageDistanceFunctions(Screen):
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
        self.table.bind(on_row_press=self.row_press)
        self.ids['table_place'].add_widget(table)

    def row_press(self, instance_table, instance_row):
        index = instance_row.index
        cols_num = len(instance_table.column_data)
        row_num = int(index/cols_num)
        print (f'press on row_num is: {row_num}')
        print (f'name of pressed line is: {self.table.row_data[row_num][0]}')
        app = MDApp.get_running_app()
        app.dictionary =  {
            "name": self.table.row_data[row_num][1],
        }
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'uddistancefunction'
        
    def on_add(self):
        app = MDApp.get_running_app()
        app.dictionary = {}
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'adddistancefunction'

    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'dataanalystmenu'

    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
#---9---
class AddDistanceFunction(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()
        if app.dictionary == {}:
            self.ids['apply'].text=f'Apply'
        else:
            self.ids['header'].text=f'Distance function: {app.dictionary.name}'
            self.ids['apply'].text=f'Delete'
    ##MICHAEL - GET ONE DISTANCE FUNCTION(dataset ID)
    ##MICHAEL - SAMPLE OF DELETE DISTANCE FUNCTION METHOd
    ##MICHAEL - SAMPLE OF CREATE DISTANCE FUNCTION METHOd
    def selected(self, filename):
        try:
            self.ids.path.text = filename[0]
            print(filename[0])
        except:
            pass
    def on_apply(self):
        app = MDApp.get_running_app()
        if app.dictionary == {}:
            print (f'add function for {self.ids.path.text}')
        pass
    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'managedistancefunctions'
    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
class UDDistanceFunction(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()
        if app.dictionary == {}:
            self.ids['apply'].text=f'Apply'
        else:
            self.ids['header'].text=f'Distance function: {app.dictionary.name}'
            self.ids['apply'].text=f'Delete'
    ##MICHAEL - GET ONE DISTANCE FUNCTION(dataset ID)
    ##MICHAEL - SAMPLE OF DELETE DISTANCE FUNCTION METHOd
    ##MICHAEL - SAMPLE OF CREATE DISTANCE FUNCTION METHOd
    def selected(self, filename):
        try:
            self.ids.path.text = filename[0]
            print(filename[0])
        except:
            pass
    def on_apply(self):
        app = MDApp.get_running_app()
        if app.dictionary == {}:
            print (f'add function for {self.ids.path.text}')
        pass
    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'managedistancefunctions'
    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
#---10---
class UpdateModels(Screen):
    ##MICHAEL - data=GET ALL MODELS FUNCTION()
    ##MICHAEL - datasetIDlist=ID's of ALL DATASETS FUNCTION()
    ##MICHAEL - distancefunctionsIDlist=ID's of ALL Distance functions FUNCTION()
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

    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'

    ##MICHAEL - SAMPLE OF UPDATE MODEL FUNCTION METHOD
    ##MICHAEL - SAMPLE OF DELETE DISTANCE FUNCTION METHOd
    ##MICHAEL - SAMPLE OF CREATE DISTANCE FUNCTION METHOd
#---11---
class ManageUsers(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()
        ##MICHAEL - GET ALL USERS data = [(id, name, attribute number, dataline, timestamp),(another one),(another one)]
        table_width = dp(Window.size[0]*9/50)
        print (app.userController.GetAllUsers())
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
        # bind function to row press
        self.table.bind(on_row_press=self.row_press)
        self.ids['table_place'].add_widget(self.table)
    # Function for row presses
    def row_press(self, instance_table, instance_row):
        index = instance_row.index
        cols_num = len(instance_table.column_data)
        row_num = int(index/cols_num)
        print (f'press on row_num is: {row_num}')
        print (f'ID of pressed line is: {self.table.row_data[row_num][0]}')
        app = MDApp.get_running_app()
        app.dictionary =  {
            "id": int(self.table.row_data[row_num][0]),
            "name": self.table.row_data[row_num][1],
            "password": self.table.row_data[row_num][2],
            "type": self.table.row_data[row_num][3],
        }
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'cruduser'
    def on_add(self):
        app = MDApp.get_running_app()
        app.dictionary = {}
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'cruduser'
    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
#---12---
class CrudUser(Screen):
    mode = ""
    def on_enter(self):
        app = MDApp.get_running_app()
        if (app.dictionary=={}):
            self.ids['header'].text= "New User"
            self.mode = "add"
        else:
            self.ids['header'].text= "user id: "+str(app.dictionary['id'])
            self.ids['name'].text= str(app.dictionary['name'])
            self.ids['password'].text= str(app.dictionary['password'])
            self.ids['type'].text= str(app.dictionary['type'])
            self.mode = "update"
    def on_delete(self):
        ## MICHAEL - DELETE USER
        print (f"id: {self.ids['header']}, name: {self.ids['name']}, password: {self.ids['password']}, type: {self.ids['type']}")
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'manageusers'
    def on_apply(self):
        if (self.mode=="add"):
            ## MICHAEL - CREATE USER
            print (f"add id: {self.ids['header']}, name: {self.ids['name']}, password: {self.ids['password']}, type: {self.ids['type']}")
        else:
            ## MICHAEL - UPDATE USER
            print (f"update id: {self.ids['header']}, name: {self.ids['name']}, password: {self.ids['password']}, type: {self.ids['type']}")
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'manageusers'
    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'manageusers'
    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
#---13---
class ChooseModels(Screen):
    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
#---14---
class AnalystResults(Screen):
    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
# WINDOW MANAGER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class AnomalabApp(MDApp):
    #GENERAL
    logo = StringProperty('gui/images/logo.jpg')
    icon = StringProperty('gui/images/icon.jpg')
    title = StringProperty('Anomalab')
    #CONTROLLERS
    userController=UsersController()
    datasetController=DatasetsController()
    modelController=ModelsController()
    #INNER VALUES
    dataSetObject = ObjectProperty(None)
    distanceFunctionObject = ObjectProperty(None)
    modelObject = ObjectProperty(None)
    userObject = ObjectProperty(None)
    dictionary = {}
    
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
