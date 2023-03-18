#CREATE VIRTUAL ENVITONMENT IN NOAM COMPUTER: kivy_venv\Scripts\activate

from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import StringProperty, ObjectProperty
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
from distance_functions_controller import Distance_Functions_Controller
from Moudles.Databases.DatasetsController import DatasetsController
from Moudles.Models.ModelController import ModelsController
from Moudles.Users.UsersController import UsersController
from Moudles.Anomaly.AnomalyPredict import checkSampleForAnomaly

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
        if (app.userObject.Type=="regular"):
            self.manager.current = 'query'
        else:
            self.manager.current = 'choosemodels'
    
    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
#---3---
class Query(Screen):
    def on_enter(self):
        self.attributesRefs=[]
        self.attributesTypes=[]
        self.ids.attributes_box.clear_widgets()
        app = MDApp.get_running_app()
        for i in range(len(app.dataSetObject.AttributesInfo)):
            print (app.dataSetObject.AttributesInfo[i])
            self.ids.attributes_box.add_widget(MDLabel(text=f'{app.dataSetObject.AttributesInfo[i]["name"]}:', halign="center"))
            if (app.dataSetObject.AttributesInfo[i]["type"] == 'numeric'):
                self.attributesTypes.append(False)
                self.attributesRefs.append(MDTextFieldRect(multiline=False, hint_text=f"insert here", input_filter = 'float'))
                self.attributesRefs[i].bind(text=self.on_text)
            else:
                self.attributesTypes.append(True)
                options = []
                for value in app.dataSetObject.AttributesInfo[i]["values"].values():
                    #BUG: Don't know to handle with NA
                    if str(value) != "nan":
                        options.append(str(value))
                self.attributesRefs.append(Spinner(text="", values=options))
                self.attributesRefs[i].bind(text=self.on_text)
            self.ids.attributes_box.add_widget(self.attributesRefs[i])
    def on_text(self, instance, value):
        if (value == ""):
            instance.background_color = (1,0,0,1)
        else:
            instance.background_color = (0,1,0,1)
    def on_apply(self):
        query = []
        app = MDApp.get_running_app()
        for i in range(len(self.attributesRefs)):
            if (self.attributesRefs[i].text==""):
                show_popup(f'MUST FILL ALL FIELDS check field number {i+1}')
                return
            if (self.attributesTypes.pop(0)):
                ## get the numeric value for categorical attribute
                dict = app.dataSetObject.AttributesInfo[i]["values"]
                value = [k for k, v in dict.items() if v == self.attributesRefs[i].text][0]
                query.append(int(value))
            else:
                # numeric feature
                query.append(int(self.attributesRefs[i].text))
        print (f'query is {query}')
        model = app.modelController.GetModel(app.dataSetObject.BestModel)
        x,y=checkSampleForAnomaly(model, query)
        app.dictionary =  {
            "results": x,
            "msg": y,
        }
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
    def on_enter(self):
        app = MDApp.get_running_app()
        self.ids.results.text=f'Is anomaly: {app.dictionary["results"]}\n\n{app.dictionary["msg"]}'

    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'query'
    
    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
#---5---
class DataAnalystMenu(Screen):
    def chooseScreen(self, screenName):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = screenName
    
    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
#---6---
class ManageDatasets(Screen):
    def on_enter(self):
        table_width = dp(Window.size[0]*9/50)
        app = MDApp.get_running_app()
        datasetsData = app.datasetController.GetAllInstances()
        self.data=[]
        for dataset in datasetsData:
            row = []
            row.append(dataset.Name)
            row.append(dataset.featuresNumber)
            row.append(dataset.instancesNumber)
            row.append(dataset.Timestamp)
            self.data.append(row)
        dataRows = len(self.data)
        pagination = False
        print (f'row of data = {dataRows}')
        if (dataRows > 5):
            pagination = True
            dataRows = 5
        self.table = MDDataTable(
            pos_hint = {'x': 0.05, 'top': 0.95},
            size_hint= (0.9, 0.9),
            use_pagination = pagination,
            rows_num = dataRows,
            column_data = [
                ("Name", dp (table_width*0.25)),
                ("Attributes", dp (table_width*0.25)),
                ("Instances", dp (table_width*0.25)),
                ("Time stamp", dp (table_width*0.25)),
            ],
            row_data = self.data
        )
        try: 
            self.ids['table_place'].clear_widgets()
            self.ids['table_place'].add_widget(self.table)
            self.table.bind(on_row_press=self.row_press)
        except Exception as e:
            print(str(e))
    def row_press(self, instance_table, instance_row):
        print(instance_row.children)
        print ("BLAH BLAH2")
        index = instance_row.index
        cols_num = len(instance_table.column_data)
        row_num = int(index/cols_num)
        print (f'press on row_num is: {row_num}')
        print (f'name of pressed line is: {self.table.row_data[row_num][0]}')
        app = MDApp.get_running_app()
        app.dictionary =  {
            "name": self.table.row_data[row_num][0],
            "featuresNumber": self.table.row_data[row_num][1],
            "instancesNumber": self.table.row_data[row_num][2],
            "timestamp": self.table.row_data[row_num][3],
        }
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'uddataset'
    def on_add(self):
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
    def selected(self, filename):
        try:
            self.ids.path.text = filename[0]
            #print(filename[0])
        except:
            pass
    def on_add(self, name, path):
        app = MDApp.get_running_app()
        try:
            if (name == '' or path == ''):
                raise Exception(f"Must enter name & choose file")
            app.datasetController.CreateDataset(name, path)
            show_popup(f"LOAD DATASET {name} SUCCESS")
        except Exception as e:
            self.resetForm()
            show_popup(str(e))
            return
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'managedatasets'
    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'managedatasets'
    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
    def resetForm(self):
        self.ids['name'].text = ""
        #self.ids['path'].text = ""
#---8---
class UDDataset(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()
        self.ids['name'].text= str(app.dictionary['name'])
        self.ids['features'].text= str(app.dictionary['featuresNumber'])
        self.ids['instances'].text= str(app.dictionary['instancesNumber'])
        self.ids['timestamp'].text= str(app.dictionary['timestamp'])
    def on_update(self, name):
        print (f"Update dataset: {name}")
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'managedatasets'
    def on_delete(self, name):
        print (f"delete dataset: {name}")
        app = MDApp.get_running_app()
        try:
            app.datasetController.DeleteDataset(name)
            show_popup(f"DELETE DATASET {name} SUCCESS")
        except Exception as e:
            show_popup(str(e))
            return
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'managedatasets'
    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'managedatasets'
    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
#---9---
class ManageDistanceFunctions(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()
        distancesData = app.distanceController.view_all_functions()
        self.data=[]
        for distanceFunction in distancesData:
            row = []
            row.append(distanceFunction)
            self.data.append(row)
        
        dataRows = len(self.data)
        pagination = False
        print (f'row of data = {dataRows}')
        if (dataRows > 5):
            pagination = True
            dataRows = 5
        table_width = dp(Window.size[0]*9/50)
        self.table = MDDataTable(
            pos_hint = {'x': 0.05, 'top': 0.95},
            size_hint= (0.9, 0.9),
            use_pagination = pagination,
            rows_num = dataRows,
            column_data = [
                ("Name", dp (table_width)),
            ],
            row_data = self.data
        )
        self.ids['table_place'].clear_widgets()
        self.ids['table_place'].add_widget(self.table)
        self.table.bind(on_row_press=self.row_press)

    def row_press(self, instance_table, instance_row):
        index = instance_row.index
        cols_num = len(instance_table.column_data)
        row_num = int(index/cols_num)
        print (f'press on row_num is: {row_num}')
        print (f'name of pressed line is: {self.table.row_data[row_num][0]}')
        app = MDApp.get_running_app()
        app.dictionary =  {
            "name": self.table.row_data[row_num][0],
        }
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'uddistancefunction'
        
    def on_add(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'adddistancefunction'

    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'dataanalystmenu'

    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
#---10---
class AddDistanceFunction(Screen):
    def selected(self, filename):
        try:
            self.ids.path.text = filename[0]
            #print(filename[0])
        except:
            pass
    def on_add(self, path):
        app = MDApp.get_running_app()
        try:
            if (path == ''):
                raise Exception(f"Must enter name & choose file")
            app.distanceController.add_function(path)
            show_popup(f"ADD DISTANCE FUCNTION SUCCESS")
        except Exception as e:
            self.resetForm()
            show_popup(str(e))
            return
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'managedistancefunctions'
    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'managedistancefunctions'
    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
    def resetForm(self):
        self.ids['path'].text = ""
#---11---
class UDDistanceFunction(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()
        self.ids['name'].text= str(app.dictionary['name'])
    def on_delete(self, name):
        print (f"delete distance function: {name}")
        app = MDApp.get_running_app()
        try:
            app.distanceController.delete_function(name)
            show_popup(f"DELETE DISTANCE FUNCTION {name} SUCCESS")
        except Exception as e:
            show_popup(str(e))
            return
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'managedistancefunctions'
    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'managedistancefunctions'
    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
#---12---
class UpdateModels(Screen):
    toUpdate = []
    def on_enter(self):
        app = MDApp.get_running_app()
        #modelsData = app.modelController.GetAllInstances()
        self.modelsList=app.modelController.GetModelsStatus()
        print (self.modelsList)
        self.data=[]
        for model in self.modelsList:
            for function in model[1]:
                row = []
                row.append(model[0])    #datasetName
                row.append(function[0]) #Name
                row.append(function[1])
                self.data.append(row)
        dataRows = len(self.data)
        pagination = False
        print (f'row of data = {dataRows}')
        if (dataRows > 5):
            pagination = True
            dataRows = 5
        table_width = dp(Window.size[0]*9/50)
        self.table = MDDataTable(
            pos_hint = {'x': 0.05, 'top': 0.95},
            size_hint= (0.9, 0.9),
            check = True,
            use_pagination = pagination,
            rows_num = dataRows,
            column_data = [
                #HERE COME CHECK MARK width
                ("Dataset", dp (table_width*0.32)),
                ("Distance Function", dp (table_width*0.32)),
                ("Exists", dp (table_width*0.32)),
            ],
            row_data = self.data
        )
        self.ids['table_place'].clear_widgets()
        self.ids['table_place'].add_widget(self.table)
        self.table.bind(on_check_press=self.checked)
        self.table.bind(on_row_press=self.row_checked)


    # Function for check presses
    def checked (self, instance_table, current_row):
        for model in self.toUpdate:
            if (model[0]==current_row[0] and model[1]==current_row[1]):
                self.toUpdate.remove(model)
                return
        self.toUpdate.append(current_row)
    # Function for row presses
    def row_checked(self, instance_table, instance_row):
        #print(instance_table, instance_row)
        pass

    def on_update(self):
        print (self.toUpdate)
        app = MDApp.get_running_app()
        for model in self.toUpdate:
            if model[2] == "":
                app.modelController.CreateModel(f'{model[0]}-{model[1]}',app.datasetController.GetDataset(model[0]), model[1])
            else:
                print (f'try to delete model {model[2]}')
                app.modelController.DeleteModel(model[2])
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'dataanalystmenu'
    
    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'dataanalystmenu'

    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
#---13---
class ManageUsers(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()
        table_width = dp(Window.size[0]*9/50)
        Allusers=app.userController.GetAllInstances()
        self.data=[]
        for user in Allusers:
            print(f'("{user.Name}","{user.Type}"),')
            row = []
            row.append(user.Name)
            row.append(user.Type)
            self.data.append(row)
        dataRows = len(self.data)
        pagination = False
        print (f'row of data = {dataRows}')
        if (dataRows > 5):
            pagination = True
            dataRows = 5
        self.table = MDDataTable(
            pos_hint = {'x': 0.05, 'top': 0.95},
            size_hint= (0.9, 0.9),
            use_pagination = pagination,
            rows_num = dataRows,
            column_data = [
                ("User-Name", dp (table_width*0.5)),
                ("User-Type", dp (table_width*0.5)),
            ],
            row_data = self.data
        )
        # bind function to row press
        self.ids['table_place'].clear_widgets()
        self.ids['table_place'].add_widget(self.table)
        self.table.bind(on_row_press=self.row_press)
    # Function for row presses
    def row_press(self, instance_table, instance_row):
        index = instance_row.index
        cols_num = len(instance_table.column_data)
        row_num = int(index/cols_num)
        print (f'press on row_num is: {row_num}')
        print (f'ID of pressed line is: {self.table.row_data[row_num][0]}')
        app = MDApp.get_running_app()
        app.dictionary =  {
            "name": self.table.row_data[row_num][0],
            "type": self.table.row_data[row_num][1],
        }
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'uduser'
    def on_add(self):
        app = MDApp.get_running_app()
        app.dictionary = {}
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'adduser'
    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
#---14---
class AddUser(Screen):
    def on_apply(self, name, password, type):
        app = MDApp.get_running_app()
        try:
            if (name == '' or password == '' or type == 'Type'):
                raise Exception(f"Must enter user name ,password and type")
            app.userController.RegisterUser(name, password, type)
            show_popup(f"REGISTER USER {name} SUCCESS")
        except Exception as e:
            self.resetForm()
            show_popup(str(e))
            return
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'manageusers'
    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'manageusers'
    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
    def resetForm(self):
        self.ids['name'].text = ""
        self.ids['password'].text = ""
        self.ids['type'].text = "Type"
#---15---
class UDUser(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()
        self.ids['name'].text= str(app.dictionary['name'])
        self.ids['type'].text= str(app.dictionary['type'])
    def on_delete(self, name):
        app = MDApp.get_running_app()
        try:
            app.userController.DeleteUser(name)
            show_popup(f"DELETE USER {name} SUCCESS")
        except Exception as e:
            self.resetForm()
            show_popup(str(e))
            return
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'manageusers'
    def on_apply(self, name, type):
        app = MDApp.get_running_app()
        try:
            app.userController.UpdateUserType(name, type)
            show_popup(f"UPDATE USER {name} SUCCESS")
        except Exception as e:
            self.resetForm()
            show_popup(str(e))
            return
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'manageusers'
    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'manageusers'
    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
    def resetForm(self):
        app = MDApp.get_running_app()
        self.ids['name'].text= str(app.dictionary['name'])
        self.ids['type'].text= str(app.dictionary['type'])
#---16---
class ChooseModels(Screen):
    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
#---17---
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
    distanceController=Distance_Functions_Controller()
    #INNER VALUES
    dataSetObject = ObjectProperty(None)
    distanceFunctionObject = ObjectProperty(None)
    modelObject = ObjectProperty(None)
    userObject = ObjectProperty(None)
    dictionary = {}
    
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Gray"
        return Builder.load_file('App.kv')
# MAIN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
    app = AnomalabApp()
    Window.fullscreen = False
    Window.minimum_height = 600
    Window.minimum_width = 800
    app.run()
    app.root_window.close()
