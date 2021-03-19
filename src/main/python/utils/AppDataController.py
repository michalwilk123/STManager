"""
Operations with the json file. Creates account. Executes json pseudo queries
"""
from config.macros import CONFIG_FILE_PATH
import misc.pathOperations as pathOper
import json
import time


def createNewUser(username: str, password: str):
    """
    Adds new user to the json file. Creates also NULL
    product value into the product list.
    This ensures that data will be updated correctly.
    """
    userEntry = {
        "username": username,
        "password": password,
        "created": time.strftime("%d-%m-%Y-%H_%M_%S"),
        "items": [createNullProduct(0)],
    }
    data = getAllData()
    data["userData"].append(userEntry)
    setNewData(data)


def findProducts(
    prodId: str = None,
    phrase: str = None,
    timeFrom: str = None,
    timeTo: str = None,
    tags: str = None,
    username: str = None,
):
    """
    Get list of products which pass given filters.
    prodId : barcode value (exact)
    phrase : looks for phrase in description. Makes small grammar
    correction on the fly
    timeFrom - timeTo : time when the product was created
    tags - get products with given tags, only needs to match one
    user - get products made by user with given username
    """
    data = getAllData()["userData"]
    if username:
        data = next(filter(lambda x: x["username"] == username, data))
        data = data["items"]
    else:
        d = []
        for usrData in data:
            for entry in usrData["items"]:
                entry["user"] = usrData["username"]

            d += usrData["items"]
        data = d

    if prodId:
        data = filter(lambda x: prodId == x["id"], data)

    if tags:
        # looking for any element in intersection of tags
        data = filter(lambda x: bool([el for el in tags if el in x["tags"]]))

    if phrase:
        data = filter(lambda x: phrase in x["desc"], data)

    if timeFrom:
        data = filter(
            lambda x: 0 < compareDatetimes(x["last_updated"], timeFrom), data
        )

    if timeTo:
        data = filter(
            lambda x: 0 > compareDatetimes(x["last_updated"], timeTo), data
        )

    return list(data)


def checkForCredentials(
    username: str, password: str, onlyCheckLogin: bool = False
) -> bool:
    usrData = getAllData()["userData"]

    for usr in usrData:
        if usr["username"] == username and usr["password"] == password:
            return True

        if onlyCheckLogin and usr["username"] == username:
            return True
    return False


def createNullProduct(index: int):
    return {
        "index": index,
        "filenames": [],
        "id": "",
        "desc": "",
        "tags": [],
        "creation_date": "",
        "last_updated": "",
    }


def resolveConfigFile(debug: bool = False):
    """
    Fix problems with the configuration file.
    Returns string with new file location
    """
    if debug:
        print("Config file does not exist! Creating new one")
    CONFIG_FILE_PATH = pathOper.createConfigFile()
    if debug:
        print(f"File created at {CONFIG_FILE_PATH}")


def getAllData(debug: bool = False):
    """
    Get all app data in form of dictionary
    """
    try:
        with open(CONFIG_FILE_PATH, "r") as dataFile:
            data = json.loads(dataFile.read())
    except (FileNotFoundError, TypeError):
        resolveConfigFile()
        return getAllData(debug)

    return data


def setNewData(data):
    try:
        with open(CONFIG_FILE_PATH, "w") as oldData:
            oldData.write(json.dumps(data))
    except OSError as e:
        from utils.DialogCollection import errorOccured
        errorOccured("No permission to access config file!")
        raise e(f"NO PERMISSION TO ACCESS {CONFIG_FILE_PATH} FILE")
    except (FileNotFoundError, TypeError):
        resolveConfigFile()
        setNewData(data)


def getUsrList():
    data = getAllData()["userData"]
    return list(map(lambda x: x["username"], data))


def compareDatetimes(date_0: str, date_1: str):
    """
    Do a LESS THEN operation (<) beetween two strings
    containing dates.
    Date Format [Name(Number of characters)]:
    [DAY(2)]-[MONTH(2)]-[YEAR(4)]-[HOUR(2)]_[MIN(2)]_[SEC(2)]
    ex.
    01-01-2020-12_36_45
    If date is badly formatted then program raises
    an error.
    """
    if len(date_0) != 19 or len(date_1) != 19:
        print(date_1)
        raise Exception("BAD DATA FORMAT!!!")

    def splitIntoSubdates(date: str):
        date = date.split("-")
        return date[:-1], date[-1]

    day0, hour0 = splitIntoSubdates(date_0)
    day1, hour1 = splitIntoSubdates(date_1)

    day0 = [int(i) for i in day0][::-1]
    day1 = [int(i) for i in day1][::-1]
    if not day0 == day1:
        res = day0 < day1
        return -1 if res else 1

    hour0 = [int(i) for i in hour0.split("_")]
    hour1 = [int(i) for i in hour1.split("_")]
    res = hour0 < hour1
    return -1 if res else 1
