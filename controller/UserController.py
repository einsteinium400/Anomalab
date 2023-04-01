from model.Storage.StorageFactory import StorageFactory
from model.User import User


class UserController:
    operationFactory = StorageFactory()
    storage = operationFactory.CreateOperationItem()
    __instance = None

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

    def __GetAllUsers(self):
        return self.storage.GetNamesList("USER")

    def __GetUser(self, username):
        usersList = self.GetAllUsers()
        if (username not in usersList):
            raise Exception("User does not exist")
        return User(username)
    
    def UpdateUserType(self, username, newType):
        user = self.__GetUser(username)
        user.Type = newType

    def RegisterUser(self, username, password, type):
        usersList = self.__GetAllUsers()
        if (username in usersList):
            raise Exception("User Exists")
        newUser = User(username, password, type)
        newUser.SaveUser()

    def DeleteUser(self, username):
        usersList = self.__GetAllUsers()
        if (username not in usersList):
            raise Exception("User Does not exist")
        self.storage.Delete(username, "USER")

    def LoginUser(self, username, suggestedPass):
        usersList = self.__GetAllUsers()
        if username not in usersList:
            raise Exception("User Does not exist")
        attemptedLoggedUser = User(username)
        if attemptedLoggedUser.VerifyPassword(suggestedPass):
            return attemptedLoggedUser.Type
        else:
            raise Exception("Incorrect Password")

    def GetListForManager(self):
        return self.storage.GetListWithSpecificAttributes("USER",['name','type'])
    
    '''def GetAllInstances(self):
            availableUsers = self.GetAllUsers()
            finalList = []
            for item in availableUsers:
                finalList.append(self.__GetUser(item))
            return finalList'''
