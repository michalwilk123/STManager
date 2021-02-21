"""
Operations with the json file. Creates account. Executes json pseudo queries
"""
from typing import List
from config.macros import APP_DATA_PATH
import json
import time


def createNewUser(username:str, password:str):
    """
    Adds new user to the json file. Creates also NULL product value into the product list.
    This ensures that data will be updated correctly.
    """
    userEntry = {
      "username" : username,
      "password" : password,
      "created" : time.strftime("%d-%m-%Y-%H_%M_%S"),
      "items" : [createNullProduct(0)]
    }
    data = getAllData()
    data["userData"].append(userEntry)
    setNewData(data)


def findProducts(id:str=None, phrase:str=None, timeFrom:str=None, 
    timeTo:str=None, tags:List[str]=None, username:str=None):
    """
    Get list of products which pass given filters.
    id : barcode value (exact)
    phrase : looks for phrase in description. Makes small grammar correction on the fly
    timeFrom - timeTo : time when the product was created
    tags - get products with given tags, only needs to match one
    user - get products made by user with given username
    """
    # TODO : matching beetween time intervals left
    data = getAllData()["userData"]
    if username:    
        data = next(filter(lambda x:x["username"]==username, data))
        data = data["items"]
    else:
        d = []
        for usrData in data:
            for entry in usrData["items"]: 
                entry["user"] = usrData["username"]

            d += usrData["items"]
        data = d


    if tags:
        # looking for any element in intersection of tags
        data = filter(lambda x: bool([el for el in tags if el in x["tags"]]))

    if phrase:
        data = filter(lambda x: phrase in x["desc"], data)

    return list(data)


def checkForCredentials(username:str, password:str) -> bool:
    usrData = getAllData()["userData"]

    for usr in usrData:
        if usr["username"] == username and \
            usr["password"] == password:
            return True
    return False


def getConfiguration():
    with open(APP_DATA_PATH, "r") as dataFile:
        configuration = json.loads(dataFile.read())["configuration"]
    return configuration


def createNullProduct(index:int):
    return {
        "index" : index,
        "filenames":[],
        "id" : "",
        "desc" : "",
        "tags" : [],
        "creation_date" : "",
        "last_updated" : ""
    }


def getAllData():
    with open(APP_DATA_PATH, "r") as dataFile:
        data = json.loads(dataFile.read())
    return data


def setNewData(data):
    with open(APP_DATA_PATH, "w") as oldData:
        oldData.write(json.dumps(data))


def getUsrList():
    data = getAllData()["userData"]
    return list(map(
        lambda x: x["username"],
        data
    ))
    
