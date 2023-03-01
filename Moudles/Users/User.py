import json
from abc import abstractmethod
import os
import uuid
import pandas as pd
import time
from dotenv import load_dotenv
import hashlib


from Moudles.Storage.StorageFactory import StorageFactory

USERS_TYPE_DICT = {
    0: "regular",
    1: "analyst",
    2: "admin"
}
REVERSE_USERS_TYPE_DICT = {
    "regular": 1,
    "analyst":2,
    "admin":3
}


class User:
    _id = 0
    _username = 0
    _pass = 0
    _type = 0
    _jsonData = 0

    def __init__(
            self,
            name,
            password= None,
            type= None,
    ):
        if password is not None:
            self._username = name
            self._id = str(uuid.uuid1())
            self._password = hashlib.md5(password.encode()).hexdigest()
            self._type = type
            self._jsonData = {
                "name": self._username,
                "id": self._id,
                "pass": self._password,
                "type": self._type,
            }
        else:
            self._username = name
            self._jsonData = self.LoadUser()
            self._password = self._jsonData['pass']
            self._type = self._jsonData['type']
            self._id = self._jsonData['id']

    def __str__(self):
        return f"The username name is {self._username}"

    @property
    def Id(self):
        return self._id

    @property
    def Name(self):
        return self._username

    @property
    def Password(self):
        return self._password

    @Password.setter
    def Password(self, value):
        self._password = hashlib.md5(value.encode()).hexdigest()
        self.SaveUser()

    @property
    def Type(self):
        return self._type

    @Type.setter
    def Type(self, value):
        self._type = value
        self.SaveUser()

    def TypeNum(self):
        return REVERSE_USERS_TYPE_DICT[self._type]

    def VerifyPassword(self,value):
        valueHash = hashlib.md5(value.encode()).hexdigest()
        if valueHash == self.Password:
            return True
        return False

    def SaveUser(self):
        operationFactory = StorageFactory()
        saver = operationFactory.CreateOperationItem()
        saver.Save(self._username, self._jsonData, "USER")

    def LoadUser(self):
        operationFactory = StorageFactory()
        loader = operationFactory.CreateOperationItem()
        jsonData = loader.Load(self._username, "USER")
        return jsonData

