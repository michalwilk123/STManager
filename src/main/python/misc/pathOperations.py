import pathlib
import os
from fbs_runtime import platform

CONFIG_FILE_FILENAME = "appData.json"

def findConfigFilePath() -> str:
    """
    Looks for config file from default location. 
    Diffrent behaviour per platform
    If found one -> returns path, otherwise
    returns None.

    Windows:
    1) AppData\Local\STManager
    2) \User\.stmanager

    Linux:
    1) /home/.config/STManager
    2) /home/.stmanager

    Other:
    Throws error
    """
    p = pathlib.Path.home()

    if platform.is_windows():
        # look for config file in appData
        if os.path.exists(
               found := p.joinpath("%APPDATA%", "Local", 
                    "STManager", CONFIG_FILE_FILENAME)):
            return found
        elif os.path.exists(
               found := p.joinpath(".stmanager", CONFIG_FILE_FILENAME)):
            return found
        
        return None # config file not found -> returning None
    elif platform.is_linux():
        if os.path.exists(
            found := p.joinpath(".config", "STManager", CONFIG_FILE_FILENAME)):
            return found
        elif os.path.exists(
            found := p.joinpath(".stmanager", CONFIG_FILE_FILENAME)):
        )
            return found

        return None

    from utils.DialogCollection import errorOccured
    errorOccured("Platform is not known. App is not supported on your"
        "platform")
    raise RuntimeError("Platform is not known. App is not supported on your"
        "platform")


def createConfigFile() -> str:
    """
    Creates config file and returns its location.
    Expects that the config file does not exist
    """
    if findConfigFilePath() is not None:
        from utils.DialogCollection import errorOccured
        errorOccured("Trying to overwrite current config file!! Abort")
        raise RuntimeError("Trying to overwrite current config file!! Abort")

    p = pathlib.Path.home()

    if platform.is_windows():
        defautlDataPath = p.joinpath("%APPDATA%", "Local")
    elif platform.is_linux():
        defautlDataPath = p.joinpath(".config")
    else:
        from utils.DialogCollection import errorOccured
        errorOccured("Platform is not known. App is not supported on your"
            "platform")
        raise RuntimeError("Platform is not known. App is not supported on your"
            "platform")

    if os.path.exists(defautlDataPath) and os.access(defautlDataPath, os.W_OK):
        # creating folder and empty config file
        os.mkdir(defautlDataPath := defautlDataPath.joinpath("STManager"))
        open(defautlDataPath := defautlDataPath.joinpath(CONFIG_FILE_FILENAME)).close()
        return defautlDataPath
        
    if os.access(p, os.W_OK):
        # creating folder and empty config file
        os.mkdir(altDataPath := p.joinpath(".stmanager"))
        open(altDataPath := altDataPath.joinpath(CONFIG_FILE_FILENAME)).close()
        return altDataPath
    else:
        from utils.DialogCollection import errorOccured
        errorOccured("Cannot create config file!! Check the permissions "
            "for the application")
        return None


def testConfigFile(configFilePath:str) -> bool:
    """
    Check for permission of the program to modify the config file.

    """
    return  os.access(configFilePath, os.W_OK) and\
        os.access(configFilePath, os.R_OK):
