# functionality used by GUI
import json
import os
import modular_distance_utils
from Anomalab.Moudles.Storage.StorageFactory import StorageFactory
from Moudles.Storage.OperationsMongo import OperationsMongo
from Moudles.Storage.OperationsMongo import Operations

import base64

path = modular_distance_utils.DISTANCE_FUNCTIONS_PATH


class Distance_Functions_Controller:

    def __init__(self):
        #  self.mongo_operations = OperationsMongo()
        operationFactory = StorageFactory()
        self.mongo_operations = operationFactory.CreateOperationItem()

        # make sure the functions dir exists and create it if it doesnt
        if not os.path.exists(path):
            os.makedirs(path)

        # upload dynamically all functions from mongoDB
        functions = self.mongo_operations.GetFullItemsList("FUNCTION")

        file_content = ""

        # iterate all functions and input them to string
        for json_obj in functions:
            function_value = json_obj["function"]
            file_content += base64.b64decode(function_value).decode('utf-8')
            file_content+="\n\n"

        # copy the string content to a file
        with open(path, "w") as file:
            file.write(file_content)

    @staticmethod
    def view_all_functions():
        function_names = [t[0] for t in modular_distance_utils.function_list]
        return function_names

    def delete_function(self, name):
        # delete in mongoDB
        self.mongo_operations.Delete(name, "FUNCTION")
        # delete in functions list
        modular_distance_utils.delete_user_function(name)

    def add_function(self, file_dir, name):
        with open(file_dir, 'r') as source_file:
            contents = source_file.read()

        encoded_string = base64.b64encode(contents.encode('utf-8')).decode('utf-8')
        print(type(encoded_string))
        print(encoded_string)

        data = {
            "id": "y5",
            "function": encoded_string,
            "name": name
        }

        jsonData = data  # json.dumps(data)

        # update database
        self.mongo_operations.Save(name, jsonData, "FUNCTION")

        # update functions list
        print(dir)
        modular_distance_utils.load_user_distance_functions(file_dir)
