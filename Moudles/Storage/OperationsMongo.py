import json
import os
from pathlib import Path

from dotenv import load_dotenv
import pymongo

from Anomalab.Moudles.Storage.Operations import Operations

COLLECTION_DICT = {
    "FUNCTION": "functions",
    "DATASET": "datasets",
    "MODEL": "models",
    "USER": "users",
    "RAW_DATASET": "raw-dataset"
}
from Moudles.Storage import Operations


class OperationsMongo(Operations):
    def __init__(self):
        self._name = "Mongo"
        load_dotenv()
        self.MONGO = os.getenv('MONGODB')
        self.CLIENT = pymongo.MongoClient(self.MONGO)
        self.PROJECTDB = self.CLIENT["AnomaLab"]

    def Save(self, name, jsonData, type):
        collection = self.PROJECTDB[COLLECTION_DICT[type]]
        query = {"id": jsonData["id"]}
        if(collection.find_one(query) == None):
            collection.insert_one(jsonData)
        else:
            collection.update_one(query,jsonData)


    def Load(self, name, type):
        collection = self.PROJECTDB[COLLECTION_DICT[type]]
        query = {"name": name}
        return collection.find_one(query)

    def Delete(self, name, type):
        collection = self.PROJECTDB[COLLECTION_DICT[type]]
        query = {"name": name}
        collection.delete_one(query)

    def GetList(self, type):
        collection = self.PROJECTDB[COLLECTION_DICT[type]]
        mongoList = collection.find()

        finalNamesList = []
        for item in mongoList:
            finalNamesList.append(item['name'])
        return finalNamesList

    def GetFullItemsList(self, type):
        collection = self.PROJECTDB[COLLECTION_DICT[type]]
        mongoList = collection.find()

        finalNamesList = []
        for item in mongoList:
            finalNamesList.append(item)
        return finalNamesList
