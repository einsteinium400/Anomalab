# functionality used by GUI
import json
import os
import uuid

from model.Storage.StorageFactory import StorageFactory
from model import modular_distance_utils
#from model.Storage.OperationsMongo import OperationsMongo
#from model.Storage.OperationsMongo import Operations

import base64
#import inspect

# path = modular_distance_utils.DISTANCE_FUNCTIONS_PATH


class DistanceFunctionController:

    def __init__(self):
        #  self.mongo_operations = OperationsMongo()
        operationFactory = StorageFactory()
        self.mongo_operations = operationFactory.CreateOperationItem()

        # make sure the functions dir exists and create it if it doesnt
        if not os.path.exists(modular_distance_utils.DISTANCE_FUNCTIONS_PATH):
            os.makedirs(modular_distance_utils.DISTANCE_FUNCTIONS_PATH)
        else:
            file_to_delete = open(modular_distance_utils.DISTANCE_FUNCTIONS_PATH, 'w')
            file_to_delete.close()

        self.reload_functions_from_mongo()

        # # upload dynamically all functions from mongoDB
        # functions = self.mongo_operations.GetFullItemsList("FUNCTION")
        #
        # file_content = ""
        #
        # # iterate all functions and input them to string
        # for json_obj in functions:
        #     function_value = json_obj["function"]
        #     file_content += base64.b64decode(function_value).decode('utf-8')
        #     file_content+="\n\n"
        #
        # # copy the string content to a file
        # with open(modular_distance_utils.DISTANCE_FUNCTIONS_PATH, "w") as file:
        #     file.write(file_content)
        #
        # modular_distance_utils.refresh_functions_list()

    def reload_functions_from_mongo(self):
        # upload dynamically all functions from mongoDB
        functions = self.mongo_operations.GetFullItemsList("FUNCTION")

        file_content = ""

        # iterate all functions and input them to string
        for json_obj in functions:
            function_value = json_obj["function"]
            file_content += base64.b64decode(function_value).decode('utf-8')
            file_content += "\n\n"

        # copy the string content to a file
        with open(modular_distance_utils.DISTANCE_FUNCTIONS_PATH, "w") as file:
            file.write(file_content)

        modular_distance_utils.refresh_functions_list()

    @staticmethod
    def view_all_functions():
        function_names = [t[0] for t in modular_distance_utils.function_list]
        return function_names

    def delete_function(self, name):
        # delete in mongoDB
        self.mongo_operations.Delete(name, "FUNCTION")
        self.mongo_operations.DeleteItemsByTypeAndFilter("FUNCTION",{"function":name})
        self.reload_functions_from_mongo()
        # delete in functions list
        #modular_distance_utils.delete_user_function(name)

    def add_function(self, file_dir):
        try:

            with open(file_dir, 'r') as source_file:
                contents = source_file.read()
        except :   
            return FileNotFoundError


        encoded_string = base64.b64encode(contents.encode('utf-8')).decode('utf-8')
        new_func_name=modular_distance_utils.load_user_distance_functions(contents)


        data = {
            "id": str(uuid.uuid1()),
            "function": encoded_string,
            "name": new_func_name
        }

        jsonData = data  # json.dumps(data)

        # update database
        self.mongo_operations.Save(new_func_name, jsonData, "FUNCTION")

        # update functions list
        print(dir)
