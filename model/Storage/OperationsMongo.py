import json
import os
from pathlib import Path

from dotenv import load_dotenv
import pymongo

from model.Storage import Operations

COLLECTION_DICT = {
    "FUNCTION": "functions",
    "DATASET": "datasets",
    "MODEL": "models",
    "USER": "users",
    "RAW_DATASET": "raw-dataset"
}



class OperationsMongo(Operations.Operations):
    def __init__(self):
        self._name = "Mongo"
        load_dotenv()
        self.MONGO = os.getenv('MONGODB')
        self.CLIENT = pymongo.MongoClient(self.MONGO)
        self.PROJECTDB = self.CLIENT["AnomaLab"]

    def Save(self, name, jsonData, type):
        collection = self.PROJECTDB[COLLECTION_DICT[type]]
        query = {"name": name}
        print ('~~~~~~~~~~~~~')
        print (jsonData)
        if(collection.find_one(query) == None):
            collection.insert_one(jsonData)
        else:
            collection.update_one(query,{"$set":jsonData})


    def Load(self, name, type):
        collection = self.PROJECTDB[COLLECTION_DICT[type]]
        query = {"name": name}
        return collection.find_one(query)

    def Delete(self, name, type):
        collection = self.PROJECTDB[COLLECTION_DICT[type]]
        query = {"name": name}
        collection.delete_one(query)

    def GetNamesList(self, type):
        collection = self.PROJECTDB[COLLECTION_DICT[type]]
        projection = { 'name': 1 }
        mongoList = collection.find({},projection)

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

    def GetListWithSpecificAttributes(self, type, attributeList):
        collection = self.PROJECTDB[COLLECTION_DICT[type]]
        projection = {key: 1 if key in attributeList else 0 for key in attributeList}
        mongoList = collection.find({},projection)
        finalNamesList = []
        for item in mongoList:
            finalNamesList.append(item)
        return finalNamesList
