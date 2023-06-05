#python imports
from datetime import datetime
import traceback

#kivy imports
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
#table imports
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
# plots imports
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from matplotlib import pyplot as plt
import pandas as pd
#forms imports
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextFieldRect
from kivy.uix.spinner import Spinner

# Controllers import
from controller.DistanceFunctionController import DistanceFunctionController
from controller.DatasetController import DatasetController
from controller.ModelController import ModelController
from controller.UserController import UserController
from controller.AnomalyDetectionController import checkSampleForAnomaly
from controller.JobController import JobController

from view.popup import show_popup

#SCREENS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#---1---
class Login(Screen):
    def do_login(self, name, password):
        app = MDApp.get_running_app()
        try:
            if (name == '' or password == ''):
                raise Exception("Must enter user name and password")
            app.userType = app.userController.LoginUser(name, password)
        except Exception as e:
            self.resetForm()
            show_popup(str(e))
            return
        self.manager.transition = SlideTransition(direction="left")
        if (app.userType == 'regular'):
            self.manager.current = 'choosedataset'
        elif (app.userType == 'analyst'):
            self.manager.current = 'dataanalystmenu'
        elif (app.userType == 'admin'):
            self.manager.current = 'manageusers'
    
    def resetForm(self):
        self.ids['user_name'].text = ""
        self.ids['user_pass'].text = ""
    
    def close(self):
        app = MDApp.get_running_app()
        app.jobController.stop_all_running_jobs()
        MDApp.get_running_app().stop()
#---2---
class ChooseDataset(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()
        try:
            ##get datasets with atleast one models
            self.datasets = app.datasetController.GetListForQuery()
            ##check if there are models in the system
            if (self.datasets == []):
                raise Exception("There are no models in the system")
            ##fill options of datasets
            nameList = [self.datasets[i]['name'] for i in range(len(self.datasets))]
            self.ids['spinner_id'].values = nameList
        except Exception as e:
            show_popup(str(e))
            self.on_back()
           
    def on_choose(self, datasetName):
        app = MDApp.get_running_app()
        ##must choose dataset
        if (datasetName == 'Choose Dataset' or datasetName == ""):
            show_popup("you must choose dataset")
            return
        ##keep dataset name and dataset models
        for dataset in self.datasets:
            if dataset['name']==datasetName:
                app.dataSetName=datasetName
                app.modelsList=dataset['bestmodel']
        ##if user is reg go to query, if analyst go to choose models
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'query'

    def on_back(self):
        app = MDApp.get_running_app()
        if app.userType == 'regular':
            self.manager.transition = SlideTransition(direction="right")
            self.manager.current = 'login'
        else:
            self.manager.transition = SlideTransition(direction="right")
            self.manager.current = 'dataanalystmenu'

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
        try:
            app.attributesList=app.datasetController.GetAttributesList(app.dataSetName)
            for i in range(len(app.attributesList)):
                self.ids.attributes_box.add_widget(MDLabel(text='[size=20]'+str(app.attributesList[i]["name"])+':[/size]', halign="center", markup= True))
                if (app.attributesList[i]["type"] == 'numeric'):
                    ##NUMERIC ADD
                    self.attributesTypes.append(False)
                    self.attributesRefs.append(MDTextFieldRect(multiline=False, hint_text=f"insert here", input_filter = 'float'))
                    self.attributesRefs[i].bind(text=self.on_text)
                else:
                    ##CATEGORY ADD
                    self.attributesTypes.append(True)
                    options = []
                    for value in app.attributesList[i]["values"].values():
                        ##DEAL WITH NA
                        if str(value) != "nan":
                            options.append(str(value))
                    self.attributesRefs.append(Spinner(text="", values=options))
                    self.attributesRefs[i].bind(text=self.on_text)
                self.ids.attributes_box.add_widget(self.attributesRefs[i])
        except Exception as e:
            show_popup(str(e))
    
    def on_text(self, instance, value):
        if (value == ""):
            instance.background_color = (1,0,0,1)
        else:
            instance.background_color = (0,1,0,1)
    
    def on_apply(self):
        app = MDApp.get_running_app()
        app.numericQuery = []
        app.originalQuery = []

        for i in range(len(self.attributesRefs)):
            if (self.attributesRefs[i].text==""):
                show_popup(f'MUST FILL ALL FIELDS check field number {i+1}')
                return
            # keep the original query
            app.originalQuery.append(str(self.attributesRefs[i].text))
            if (self.attributesTypes.pop(0)):
                # get the numeric value for categorical attribute
                dict = app.attributesList[i]["values"]
                value = [k for k, v in dict.items() if v == self.attributesRefs[i].text][0]
                app.numericQuery.append(int(value))
            else:
                # numeric feature
                app.numericQuery.append(float(self.attributesRefs[i].text))
        print (f'query is {app.numericQuery}')
        if app.userType == 'regular':
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'results'
        else:
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'choosemodels'

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
        model = app.modelController.GetModel(app.modelsList[0]['name'])
        answer=checkSampleForAnomaly(model, app.numericQuery)
        string = ""
        if answer['anomaly']==True:
            string = '[color=ff3333][b]Anomaly[/b][/color]'
        else:
            string = '[color=00FF00][b]Not anomaly[/b][/color]'
        self.ids.result.text='Query is: '+string+ ' (Model: '+app.modelsList[0]["name"]+')'
        
        #TABLE
        table_width = dp(Window.size[0]*9/50)
        self.data=[]
        for i in range(len(answer['results'])):
            row = []
            row.append('[size=20]'+app.attributesList[i]['name']+'[/size]')
            row.append('[size=20]'+str(app.originalQuery[i])+'[/size]')
            row.append('[size=20]'+str(answer['results'][i])+'[/size]')
            row.append('[size=20]'+str(answer['stadarizedResults'][i])+'[/size]')
            self.data.append(row)
        dataRows = len(self.data)
        pagination = False
        self.table = MDDataTable(
            pos_hint = {'x': 0.05, 'top': 0.95},
            size_hint= (0.9, 0.9),
            use_pagination = pagination,
            rows_num = dataRows,
            column_data = [
                ("[size=32]Attribute[/size]", dp (table_width*0.25)),
                ("[size=32]Sample[/size]", dp (table_width*0.25)),
                ("[size=32]Distance[/size]", dp (table_width*0.25)),
                ("[size=32]StandarizeDistance[/size]", dp (table_width*0.25)),
            ],
            row_data = self.data
        )
        try: 
            self.ids['table_place'].clear_widgets()
            self.ids['table_place'].add_widget(self.table)
            self.table.bind(on_row_press=self.row_press)
        except Exception as e:
            print(str(e))
        
        #data for graph
        print ('densities:',answer['densities'])
        Xaxis = ['<AVG','AVG-1SD','1SD-2SD','2SD-3SD','3SD<']
        Yaxis = list(answer['densities'].values())
        colors = ['grey','grey','grey','grey','grey']
        colors[answer['sampleColumn']] = 'blue'
               
        #graph
        plt.bar(Xaxis,Yaxis, color=colors)
        plt.ylabel('samples')
        plt.title('Cluster Density')
        plt.text(answer['sampleColumn'],Yaxis[answer['sampleColumn']],'HERE', ha = 'center',bbox = dict(facecolor = 'blue', alpha =0.8))
        plt.legend()
        
        self.ids['plot_place'].add_widget(FigureCanvasKivyAgg(plt.gcf()))
        

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
        if (screenName=='updatemodels'):
            app = MDApp.get_running_app()    
            #check processes
            if (app.jobController.get_running_jobs()==[]):
                self.manager.current = screenName
            else:
                show_popup("process of create models still working")        
                return
        self.manager.current = screenName
    
    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
#---6---
class ManageDatasets(Screen):
    def on_enter(self):
        table_width = dp(Window.size[0]*9/50)
        app = MDApp.get_running_app()
        datasetsData = app.datasetController.GetListForManager()
        self.data=[]
        for dataset in datasetsData:
            row = []
            row.append(dataset['name'])
            row.append(dataset['featuresNumber'])
            row.append(dataset['instancesNumber'])
            row.append(str(datetime.fromtimestamp(dataset['timestamp']))[:16])
            self.data.append(row)
        self.table = MDDataTable(
            pos_hint = {'x': 0.05, 'top': 0.95},
            size_hint= (0.9, 0.9),
            use_pagination = False,
            rows_num = len(self.data),
            column_data = [
                ("Attribute", dp (table_width*0.25)),
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
        index = instance_row.index
        cols_num = len(instance_table.column_data)
        row_num = int(index/cols_num)
        app = MDApp.get_running_app()
        app.dictionary =  {
            "name": self.table.row_data[row_num][0],
            "featuresNumber": self.table.row_data[row_num][1],
            "instancesNumber": self.table.row_data[row_num][2],
            "timestamp": self.table.row_data[row_num][3],
        }
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'deletedataset'
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
        except:
            pass
    def on_add(self, name, path):
        app = MDApp.get_running_app()
        try:
            if (name == '' or path == ''):
                raise Exception(f"Must enter name & choose file")
            app.datasetController.CreateDataset(name, path)
            self.resetForm()
            show_popup(f"LOAD DATASET {name} SUCCESS")
        except Exception as e:
            self.resetForm()
            print (traceback.print_exc())
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
class DeleteDataset(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()
        self.ids['name'].text= 'name: '+str(app.dictionary['name'])
        self.ids['features'].text= 'number of features: '+str(app.dictionary['featuresNumber'])
        self.ids['instances'].text= 'number of instances: '+str(app.dictionary['instancesNumber'])
        self.ids['timestamp'].text= 'time stamp: '+str(app.dictionary['timestamp'])
    def on_delete(self):
        app = MDApp.get_running_app()
        print (f"delete dataset: {str(app.dictionary['name'])}")
        try:
            app.datasetController.DeleteDataset(str(app.dictionary['name']))
            show_popup(f"DELETE DATASET {str(app.dictionary['name'])} SUCCESS")
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
        distancesData = app.distanceController.getListForManager()
        self.data=[]
        for distanceFunction in distancesData:
            row = []
            row.append(distanceFunction)
            self.data.append(row)
        table_width = dp(Window.size[0]*9/50)
        self.table = MDDataTable(
            pos_hint = {'x': 0.05, 'top': 0.95},
            size_hint= (0.9, 0.9),
            use_pagination = False,
            rows_num = len(self.data),
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
        app = MDApp.get_running_app()
        app.dictionary =  {
            "name": self.table.row_data[row_num][0],
        }
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'deletedistancefunction'
        
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
class DeleteDistanceFunction(Screen):
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
        self.toUpdate = []
        app = MDApp.get_running_app()
        self.modelsList=app.modelController.GetModelsStatus()
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
        if (dataRows > 5):
            pagination = True
            dataRows = 5
        table_width = dp(Window.size[0]*9/50)
        try:
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
        except Exception as e:
            show_popup(str(e))

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
                try:
                    app.jobController.add_job(app.modelController.CreateModel, app.datasetController.GetDataset(model[0]), model[1])
                    print ('building model for ', model[0], '-', model[1])
                except Exception as e:
                    print (traceback.print_exc())
                    show_popup(str(e))
                    return
                self.manager.transition = SlideTransition(direction="right")
                self.manager.current = 'updatemodels'
            else:
                print (f'try to delete model {model[2]}')
                app.modelController.DeleteModel(model[2], app.datasetController.GetDataset(model[0]))
                show_popup(f'delete model {model[2]} success')
                self.manager.transition = SlideTransition(direction="right")
                self.manager.current = 'updatemodels'
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
        Allusers=app.userController.GetListForManager()
        self.data=[]
        for user in Allusers:
            row = []
            row.append(user['name'])
            row.append(user['type'])
            self.data.append(row)
        self.table = MDDataTable(
            pos_hint = {'x': 0.05, 'top': 0.95},
            size_hint= (0.9, 0.9),
            use_pagination = False,
            rows_num = len(self.data),
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
    def on_enter(self):
        app = MDApp.get_running_app()
        app.modelsApplyList=[]
        self.data=[]
        for model in app.modelsList:
            row = []
            row.append(model['name'])   #Name
            row.append(round(model['silhouette'],5))   #Silhouette
            row.append(round(model['wcss'],2))   #wcss
            self.data.append(row)
        dataRows = len(self.data)
        pagination = False
        if (dataRows > 5):
            pagination = True
            dataRows = 5
        table_width = dp(Window.size[0]*9/50)
        try:
            self.table = MDDataTable(
                pos_hint = {'x': 0.05, 'top': 0.95},
                size_hint= (0.9, 0.9),
                check = True,
                use_pagination = pagination,
                rows_num = dataRows,
                column_data = [
                    #HERE COME CHECK MARK width
                    ("Model Name", dp (table_width*0.32)),
                    ("Silhouette", dp (table_width*0.32)),
                    ("Wcss", dp (table_width*0.32)),
                ],
                row_data = self.data
            )
            self.ids['table_place'].clear_widgets()
            self.ids['table_place'].add_widget(self.table)
            self.table.bind(on_check_press=self.checked)
        except Exception as e:
            show_popup(str(e))

    # Function for check presses
    def checked (self, instance_table, current_row):
        app = MDApp.get_running_app()
        for model in app.modelsApplyList:
            if (model==current_row[0]):
                self.toApply.remove(model)
                return
        app.modelsApplyList.append(current_row[0])

    def on_choose(self):
        try:
            app = MDApp.get_running_app()
            print (app.modelsApplyList)
            if app.modelsApplyList == []:
                show_popup('Must choose at least one model')
                return
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'analystresults'
        except Exception as e:
            show_popup(str(e))
    
    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'choosedataset'

    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
#---17---
class AnalystResults(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()
        results = []
        modelsNum = len(app.modelsApplyList)
        try:
            for modelname in app.modelsApplyList:
                results.append(checkSampleForAnomaly(app.modelController.GetModel(modelname), app.numericQuery))
        except Exception as e:
            show_popup(str(e))
            return
        table_width = dp(Window.size[0]*9/50)
        self.data=[]
        row = []
        row.append('[size=20]Is anomaly[/size]')
        row.append('[size=20]-[/size]')
        for result in results:
            if result['anomaly']==True:
                row.append('[size=20][color=ff3333][b]'+str(result['anomaly'])+'[/b][/color][/size]')
            else:
                row.append('[size=20][color=00FF00][b]'+str(result['anomaly'])+'[/b][/color][/size]')
        self.data.append(row)
        for i in range(len(app.attributesList)):
            row = []
            row.append('[size=20]'+app.attributesList[i]['name']+'[/size]')
            row.append('[size=20]'+str(app.originalQuery[i])+'[/size]')
            for result in results:
                row.append('[size=20]'+str(round(result['stadarizedResults'][i],2))+'[/size]')
            self.data.append(row)
        dataRows = len(self.data)
        pagination = False
        columnSize = table_width*(1/(modelsNum+2))
        columnNames = []
        columnNames.append(("[size=32]Attribute[/size]", dp (columnSize)))
        columnNames.append(("[size=32]Sample[/size]", dp (columnSize)))
        for modelname in app.modelsApplyList:
            columnNames.append(("[size=32]"+modelname+"[/size]", dp (columnSize)),)
        self.table = MDDataTable(
            pos_hint = {'x': 0.05, 'top': 0.95},
            size_hint= (0.9, 0.9),
            use_pagination = pagination,
            rows_num = dataRows,
            column_data = columnNames,
            row_data = self.data
        )
        try: 
            self.ids['table_place'].clear_widgets()
            self.ids['table_place'].add_widget(self.table)
            self.table.bind(on_row_press=self.row_press)
        except Exception as e:
            print(str(e))

    def on_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'choosemodels'

    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
# WINDOW MANAGER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class AnomalabApp(MDApp):
    #GENERAL
    logo = StringProperty('view/images/logo.jpg')
    icon = StringProperty('view/images/icon.jpg')
    title = StringProperty('Anomalab')
    #CONTROLLERS
    userController=UserController()
    datasetController=DatasetController()
    modelController=ModelController()
    distanceController=DistanceFunctionController()
    jobController=JobController()
    #INNER VALUES
    dataSetName = StringProperty(None)
    modelsList = ObjectProperty(None)   #USED FOR QUERIES
    modelsApplyList = []                #USED FOR ANALYST QUERY
    userType = StringProperty(None)     #USED FOR SCREENS NAVIGATION
    attributesList = []
    numericQuery = []
    originalQuery = []
    dictionary = {}
    
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Gray"
        return Builder.load_file('view/App.kv')
