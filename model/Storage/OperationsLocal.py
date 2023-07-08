import json
import os
from pathlib import Path
import time

from dotenv import load_dotenv
from model.Storage import Operations

AbsolutePath = Path(os.path.abspath(__file__))


DATAPATH = str(AbsolutePath.parent.parent.parent) + "\Data"
FILEPATH_DICT = {
    "FUNCTION": "functions",
    "DATASET": "datasets",
    "MODEL": "models",
    "USER":"users",
    "RAW_DATASET":"raw-datasets"
}



class OperationsLocal(Operations.Operations):
    load_dotenv()
    CACHE_TIME_IN_SEC = int(os.getenv('CACHE_TIME_IN_SEC',7200))
    def __init__(self):
        self._name="Local"

    def getPath(self):
        return DATAPATH
    def __checkFileCacheTime(self,fileName):
        if os.path.exists(fileName):
            ctime = os.path.getmtime(fileName)
            if (time.time() - ctime) < self.CACHE_TIME_IN_SEC:
                return False
            return True
        return True

    def Save(self,name, jsonData, type):
        filename = f"{DATAPATH}\{FILEPATH_DICT[type]}\{name}.json"
        try:
            del jsonData['_id']
        except:
            pass
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as json_file:
            json.dump(jsonData, json_file,
                      indent=4,
                      separators=(',', ': '))

    def Load(self, name, type):
        filePath = f"{DATAPATH}\{FILEPATH_DICT[type]}\{name}.json"
        
        if (os.path.exists(filePath)):
            if (self.__checkFileCacheTime(filePath) is False): 
                f = open(filePath)
                data = json.load(f)
                return data
            raise Exception("Cache time limit")
        else:
            raise Exception("No File")

    def Delete(self, name, type):
        filePath = f"{DATAPATH}\{FILEPATH_DICT[type]}\{name}.json"
        if (os.path.exists(filePath)):
            os.remove(filePath)
            return 1
        return 0
    
    def GetNamesList(self, type):
        filePath = f"{DATAPATH}\{FILEPATH_DICT[type]}"
        if (os.path.exists(filePath)):
            itemsList = os.listdir(filePath)
            new_set = {x.removesuffix('.json') for x in itemsList}
            return new_set
        return []

    def GetFullItemsList(self, type):
        filePath = f"{DATAPATH}\{FILEPATH_DICT[type]}"
        if (os.path.exists(filePath)):
            # Initialize an empty list to hold the objects
            objects = []
            
            # Loop through each file in the data/datasets directory
            for filename in os.listdir(filePath):
                # Open the file and load its contents as a JSON object
                with open(os.path.join("data/datasets", filename), "r") as f:
                    json_obj = json.load(f)
                        
                    # Append the JSON object to the list of objects
                    objects.append(json_obj)
            # Return the list of objects
            return objects
        return []
    
    def GetListWithSpecificAttributes(self, type, attributeList):
        filePath = f"{DATAPATH}\{FILEPATH_DICT[type]}"
        if (os.path.exists(filePath)):
            # Initialize an empty list to hold the objects
            objects = []
            
            # Loop through each file in the data/datasets directory
            for filename in os.listdir(filePath):
                # Open the file and load its contents as a JSON object
                with open(os.path.join(filePath, filename), "r") as f:
                    json_obj = json.load(f)
                        
                    # Append the JSON object to the list of objects after filtering
                    filtered_json_obj = {key: json_obj[key] for key in json_obj if key in attributeList}
            # Return the list of objects
            return filtered_json_obj
        return []
    
    def GetListWithSpecificAttributesWithName(self, name, type, attributeList):
        filePath = f"{DATAPATH}\{FILEPATH_DICT[type]}"
            
        # Open the file and load its contents as a JSON object
        with open(os.path.join(filePath, name), "r") as f:
            json_obj = json.load(f)
                        
            # Append the JSON object to the list of objects after filtering
            filtered_json_obj = {key: json_obj[key] for key in json_obj if key in attributeList}
        # Return the list of objects
        return filtered_json_obj
    
    def DeleteItemsByTypeAndFilter(self,itemType,filter):
        filePath = f"{DATAPATH}\{FILEPATH_DICT[itemType]}"
                # Extract the filter key and value from the filter argument
        filter_key, filter_value = next(iter(filter.items())) if filter else (None, None)
        if (os.path.exists(filePath)):
            filesToDelete = []
            # Loop through each file in the data/datasets directory
            for filename in os.listdir(filePath):
                # Open the file and load its contents as a JSON object
                with open(os.path.join(filePath, filename), "r") as f:
                    json_obj = json.load(f)
                     # Check if the filter condition is met
                    if filter_key is not None and json_obj.get(filter_key) == filter_value:
                        # Add to delete file list
                        filesToDelete.append(os.path.join(filePath, filename))
                        
            for filename in filesToDelete:
                os.remove(filename)

    
