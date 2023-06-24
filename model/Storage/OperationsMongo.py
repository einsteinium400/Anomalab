import json
import os
from pathlib import Path
import datetime
import threading

from dotenv import load_dotenv
import pymongo

from model.Storage import Operations
from model.Storage.OperationsLocal import OperationsLocal

COLLECTION_DICT = {
    "FUNCTION": "functions",
    "DATASET": "datasets",
    "MODEL": "models",
    "USER": "users",
    "RAW_DATASET": "raw-dataset"
}



class OperationsMongo(Operations.Operations):
    __instance = None
    __LocalCache = OperationsLocal()
    __lastCacheTime = datetime.datetime.now() - datetime.timedelta(minutes=10)
    load_dotenv()
    CACHE_TIME_IN_SEC = int(os.getenv('CACHE_TIME_IN_SEC',300))

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self, *args, **kwargs):
        if self.__initialized:
            return
        self.__initialized = True
        # initialization code here
        self._name = "Mongo"
        self.MONGO = os.getenv('MONGODB')
        self.CLIENT = pymongo.MongoClient(self.MONGO)
        self.PROJECTDB = self.CLIENT["AnomaLab"]

    def __cacheRule(self):
        if(datetime.datetime.now() >= self.__lastCacheTime + datetime.timedelta(seconds=300)):
            self.__lastCacheTime = datetime.datetime.now()
            return True
        return False

    def __cast_keys_to_string(self, obj):
        """
        Recursively converts all dictionary keys to strings.
        """
        if isinstance(obj, dict):
            return {str(k): self.__cast_keys_to_string(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.__cast_keys_to_string(elem) for elem in obj]
        else:
            return obj

    def Save(self, name, jsonData, type):
        safeJsonData = self.__cast_keys_to_string(jsonData)
        collection = self.PROJECTDB[COLLECTION_DICT[type]]
        query = {"name": name}
        if(collection.find_one(query) == None):
            collection.insert_one(safeJsonData)
        else:
            collection.update_one(query,{"$set":safeJsonData})
        self.__LocalCache.Save(name, safeJsonData, type)


    def Load(self, name, type):
        try:
            return self.__LocalCache.Load(name, type)
        except Exception as e :
            collection = self.PROJECTDB[COLLECTION_DICT[type]]
            query = {"name": name}
            item = collection.find_one(query)
            self.__LocalCache.Save(name,item,type)
            return item

    def Delete(self, name, type):
        collection = self.PROJECTDB[COLLECTION_DICT[type]]
        query = {"name": name}
        self.__LocalCache.Delete(name, type)
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

    
    def GetListWithSpecificAttributesWithName(self, name, type, attributeList):
        collection = self.PROJECTDB[COLLECTION_DICT[type]]
        projection = {key: 1 if key in attributeList else 0 for key in attributeList}
        mongoList = collection.find({'name':name},projection)
        finalNamesList = []
        for item in mongoList:
            finalNamesList.append(item)
        return finalNamesList

    def DeleteItemsByTypeAndFilter(self,itemType,filter):
        if itemType in COLLECTION_DICT:
            collection = self.PROJECTDB[COLLECTION_DICT[itemType]]
            result = collection.delete_many(filter)
            deleted_names = []
            for doc in collection.find(filter, {"name": 1}):
                deleted_names.append(doc["name"])
            self.__LocalCache.DeleteItemsByTypeAndFilter(itemType,filter)
            return deleted_names
        else:
            raise Exception("Invalid itemType")