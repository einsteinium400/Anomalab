# functionality used by GUI
import modular_distance_utils
from Moudles.Storage.OperationsMongo import OperationsMongo

class Controller:

    def __init__(self):
        self.mongo_operations=OperationsMongo()

    def view_all_functions(self):
        function_names = [t[0] for t in modular_distance_utils.function_list]
        return function_names


    def delete_function(self, name):
        # delete in mongoDB
        self.mongo_operations.Delete(name, "FUNCTION")

        #delete in functions list



    def add_function(dir):
        pass


    # functionality used by model

    def upload_function_to_mongo(function_object):
        # call
        pass
