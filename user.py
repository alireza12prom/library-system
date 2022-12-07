from DataManager import JsonManager
import datetime

jsLib = JsonManager()

class User:
    def __init__(self, Id, name, password, creditType):
        self._id = Id
        self._name = name
        self._passowrd = password
        self._creditType = creditType
    
    @property    
    def Id(self):
        return self._id
   
    @property
    def name(self):
        return self._name
    
    @property
    def password(self):
        return len(self._passowrd) * "*"
    
    @property
    def creditType(self):
        return self._creditType

    def changeId(self, newId:str):
        if len(newId) < 1:
            print("InputError: id is wrong!")
            return -1
        
        users = jsLib.pullData()["Users"]
        if newId in users:
            print("This id has already used")
            return -1

        jsLib.removeDataFromCategory("Users", self._id)
        jsLib.appendDataToCategory("Users", {newId:users[self._id]})
        self._id = newId
        print("Your id changed successfully(^,^)")

    def changeName(self, newName:str):
        if len(newName) < 1:
            print("InputError: name is wrong!")
            return -1
        
        jsLib.updateData("Users", self._id, "Name", newName)
        self._name = newName
        print("Your name changed successfully(^,^)")
    
    def changePassword(self, oldPass:str, newPass:str):
        if oldPass != self._passowrd:
            print("InputError: Your old password is wrong")
            return -1
        if len(newPass) < 5:
            print("InputError: Your password shoud be have at least five characters")
            return -1
        
        jsLib.updateData("Users", self._id, "Password", newPass)
        self._passowrd = newPass
        print("Your password changed successfully(^,^)")

