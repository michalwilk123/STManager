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
      "items" : [
        {
          "index" : 0,
          "filenames" : [],
          "id" : "",
          "descr" : "",
          "tags" : [],
          "creation_date" : "",
          "last_updated" : ""
        },
      ]
    }

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
    # TODO : do this function later, this will get pretty complicated
    return []


def checkForCredentials(username:str, password:str) -> bool:
    return True

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
