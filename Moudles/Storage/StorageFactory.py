from abc import abstractmethod
from dotenv import load_dotenv
import os

from Moudles.Storage.OperationsLocal import OperationsLocal
from Moudles.Storage.OperationsMongo import OperationsMongo


class StorageFactory:
    def __init__(self):
        load_dotenv()
        self.STORAGE = os.getenv('STORAGE')

    def CreateOperationItem(self):
        item = 0
        if self.STORAGE == 'LOCAL':
            item = OperationsLocal()
        if self.STORAGE == "MONGO":
            item = OperationsMongo()
        return item
