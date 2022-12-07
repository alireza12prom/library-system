import json


class JsonManager:
    __PATH = "data.json"
    def pullData(self):
        with open(self.__PATH, "r") as file:
            return json.load(file)

    def __write(self, data):
        with open(self.__PATH, "w") as file:
            json.dump(data, file, indent=4)

    def updateData(self, category:str, uniqId:str, target:str, value:str):
        if category not in ["Users", "Books"]:
            raise ValueError("JsongManagerError: Category is wrong")
        
        data = self.pullData()
        try:
            data[category][uniqId][target] = value
            self.__write(data)
        except:
            raise Exception("JsonManagerError: Update date is not possible")
    
    def appendDataToCategory(self, category:str, value:dict):
        data = self.pullData()
        data[category].update(value)
        self.__write(data)
    
    def removeDataFromCategory(self, category:str, uniqId:str):
        data = self.pullData()
        data[category].pop(uniqId)
        self.__write(data)
        