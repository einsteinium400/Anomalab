import json
import os
from pathlib import Path

from dotenv import load_dotenv
import pymongo


COLLECTION_DICT = {
    "FUNCTION": "functions",
    "DATASET": "datasets",
    "MODEL": "models",
    "USER":"users"
}
from Moudles.Storage import Operations


class OperationsMongo(Operations.Operations):
    def __init__(self):
        self._name="Mongo"
        load_dotenv()
        self.MONGO = os.getenv('MONGODB')
        self.CLIENT = pymongo.MongoClient(self.MONGO)
        self.PROJECTDB=self.CLIENT["AnomaLab"]


    def Save(self,name, jsonData, type):
        collection = self.PROJECTDB[COLLECTION_DICT[type]]
        collection.insert_one(jsonData)

    def Load(self, name, type):
        collection = self.PROJECTDB[COLLECTION_DICT[type]]
        query = {"name":name}
        return collection.find_one(query)

    def Delete(self, name, type):
        pass

    def GetList(self, type):
        pass
