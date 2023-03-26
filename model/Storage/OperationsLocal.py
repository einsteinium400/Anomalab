import json
import os
from pathlib import Path
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
    def __init__(self):
        self._name="Local"

    def getPath(self):
        return DATAPATH

    def Save(self,name, jsonData, type):
        filename = f"{DATAPATH}\{FILEPATH_DICT[type]}\{name}.json"
        print(f"saving in {DATAPATH}\{FILEPATH_DICT[type]}\{name}.json")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as json_file:
            json.dump(jsonData, json_file,
                      indent=4,
                      separators=(',', ': '))

    def Load(self, name, type):
        filePath = f"{DATAPATH}\{FILEPATH_DICT[type]}\{name}.json"
        print(f"Path Load  {filePath}")
        if (os.path.exists(filePath)):
            f = open(filePath)
            data = json.load(f)
            return data
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
        pass
    def GetListWithSpecificAttributes(self, type, attributeList):
        pass
