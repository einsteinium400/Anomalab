import json
from abc import abstractmethod
import os


class Operations:
    def __init__(self):
        self._name= "null"
    @abstractmethod
    def Save(self,name, jsonData, type):
        pass

    @abstractmethod
    def Load(self, name, type):
        pass

    @abstractmethod
    def Delete(self, name, type):
        pass

    @abstractmethod
    def GetList(self, type):
        pass
