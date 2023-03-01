from Moudles.Storage.StorageFactory import StorageFactory
from Moudles.Users.User import User


class UsersController:
    operationFactory = StorageFactory()
    storage = operationFactory.CreateOperationItem()

    def UpdateUserType(self, username, newType):
        user = self.GetUser(username)
        user.Type = newType

    def GetAllUsers(self):
        operationFactory = StorageFactory()
        self.storage = operationFactory.CreateOperationItem()
        return self.storage.GetList("USER")

    def GetUser(self, username):
        usersList = self.GetAllUsers()
        if (username not in usersList):
            raise Exception("User does not exist")
        return User(username)

    def RegisterUser(self, username, password, type):
        usersList = self.GetAllUsers()
        if (username in usersList):
            raise Exception("User Exists")
        newUser = User(username, password, type)
        newUser.SaveUser()

    def DeleteUser(self, username):
        usersList = self.GetAllUsers()
        if (username not in usersList):
            raise Exception("User Does not exist")
        self.storage.Delete(username, "USER")

    def LoginUser(self, username, suggestedPass):
        usersList = self.GetAllUsers()
        if username not in usersList:
            raise Exception("User Does not exist")
        attemptedLoggedUser = User(username)
        if attemptedLoggedUser.VerifyPassword(suggestedPass):
            return attemptedLoggedUser
        else:
            raise Exception("Incorrect Password")
        raise Exception("Login Error")
