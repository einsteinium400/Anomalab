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
        print(f"****{datetime.datetime.now()} >=  {self.__lastCacheTime} +  {datetime.timedelta(seconds=300)}  -- {datetime.datetime.now() >= self.__lastCacheTime + datetime.timedelta(seconds=300)}")
        if(datetime.datetime.now() >= self.__lastCacheTime + datetime.timedelta(seconds=300)):
            self.__lastCacheTime = datetime.datetime.now()
            print("## __cacheRule True ")
            return True
        print("## __cacheRule False ")
        return False


    def Save(self, name, jsonData, type):
        print ('DEBUG JSON DATA:' , jsonData)
        collection = self.PROJECTDB[COLLECTION_DICT[type]]
        query = {"name": name}
        if(collection.find_one(query) == None):
            collection.insert_one(jsonData)
        else:
            collection.update_one(query,{"$set":jsonData})
        self.__LocalCache.Save(name, jsonData, type)


    def Load(self, name, type):
        try:
            return self.__LocalCache.Load(name, type)
        except Exception as e :
            print(f"### LOAD Error {str(e)}")
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
        if(self.__cacheRule() is True):
            print("### General Cache time miss 1")
            print(type)
            thread = threading.Thread(target=self.GetFullItemsList, args = (type,))
            thread.start()
            
        else:
            print("### General Cache time hit 1")
            return self.__LocalCache.GetListWithSpecificAttributes(type, attributeList)
    
    def GetListWithSpecificAttributesWithName(self, name, type, attributeList):
        collection = self.PROJECTDB[COLLECTION_DICT[type]]
        projection = {key: 1 if key in attributeList else 0 for key in attributeList}
        mongoList = collection.find({'name':name},projection)
        finalNamesList = []
        for item in mongoList:
            finalNamesList.append(item)
        return finalNamesList
        if(self.__cacheRule() is True):
            print("### General Cache time miss 2")
            thread = threading.Thread(target=self.GetFullItemsList, args = (type,))
            thread.start()
            
        
        else:
            print("### General Cache time hit 2")
            return self.__LocalCache.GetListWithSpecificAttributesWithName(name,type,attributeList)

    def DeleteItemsByTypeAndFilter(self,itemType,filter):
        if itemType in COLLECTION_DICT:
            collection = self.PROJECTDB[COLLECTION_DICT[itemType]]
            result = collection.delete_many(filter)
            print(f'{result.deleted_count} documents were deleted.')
            deleted_names = []
            for doc in collection.find(filter, {"name": 1}):
                deleted_names.append(doc["name"])
            self.__LocalCache.DeleteItemsByTypeAndFilter(itemType,filter)
            return deleted_names
        else:
            raise Exception("Invalid itemType")