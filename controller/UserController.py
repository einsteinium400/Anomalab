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
        try:
            return self.storage.GetNamesList("USER")
        except Exception as e:
                raise Exception(f"Error getting all users")

    def __GetUser(self, username):
        try:
            usersList = self.__GetAllUsers()
            if (username not in usersList):
                raise Exception("User does not exist")
            return User(username)
        except Exception as e:
            raise Exception(f"Error getting users")   
         
    def UpdateUserType(self, username, newType):
        try:
            user = self.__GetUser(username)
            user.Type = newType
        except Exception as e:
            raise Exception(f"Error getting user type") 
        
    def RegisterUser(self, username, password, type):
        try:
            usersList = self.__GetAllUsers()
            if (username in usersList):
                raise Exception("User Exists")
            newUser = User(username, password, type)
            newUser.SaveUser()
        except Exception as e:
            raise Exception(f'Error Registering user: {e}') 
        
    def DeleteUser(self, username):
        try:
            usersList = self.__GetAllUsers()
            if (username not in usersList):
                raise Exception("User Does not exist")
            self.storage.Delete(username, "USER")
        except Exception as e:
            raise Exception(f"Error deleting users") 
        
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
        try:
            return self.storage.GetListWithSpecificAttributes("USER",['name','type'])
        except Exception as e:
                raise Exception(f"Error getting users") 
