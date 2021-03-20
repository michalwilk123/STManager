import pathlib
import os
import time
import json
from fbs_runtime import platform

class ConfigPaths:
    CONFIG_FILE_FILENAME = "appData.json"
    CONFIG_FILE_PATH = ""


def findConfigFilePath() -> str:
    """
    Looks for config file from default location.
    Diffrent behaviour per platform
    If found one -> returns path, otherwise
    returns None.

    If correct path found -> function caches the result

    Windows:
    1) AppData\\Local\\STManager
    2) \\User\\.stmanager

    Linux:
    1) /home/.config/STManager
    2) /home/.stmanager

    Other:
    Throws error
    """
    if ConfigPaths.CONFIG_FILE_PATH:
        return ConfigPaths.CONFIG_FILE_PATH    
    
    p = pathlib.Path.home()

    if platform.is_windows():
        # look for config file in appData
        if os.path.exists(
            found := p.joinpath(
                "AppData", "Local", "STManager", ConfigPaths.CONFIG_FILE_FILENAME
            )
        ):
            ConfigPaths.CONFIG_FILE_PATH = found
            return found
        elif os.path.exists(
            found := p.joinpath(".stmanager", ConfigPaths.CONFIG_FILE_FILENAME)
        ):
            ConfigPaths.CONFIG_FILE_PATH = found
            return found

        return None  # config file not found -> returning None
    elif platform.is_linux():
        if os.path.exists(
            found := p.joinpath(".config", "STManager", ConfigPaths.CONFIG_FILE_FILENAME)
        ):
            ConfigPaths.CONFIG_FILE_PATH = found
            return found
        elif os.path.exists(
            found := p.joinpath(".stmanager", ConfigPaths.CONFIG_FILE_FILENAME)
        ):
            ConfigPaths.CONFIG_FILE_PATH = found
            return found

        return None

    from utils.DialogCollection import errorOccured

    errorOccured(
        "Platform is not known. App is not supported on your" "platform"
    )
    raise RuntimeError(
        "Platform is not known. App is not supported on your" "platform"
    )


def createConfigFile() -> str:
    """
    Creates config file and returns its location.
    Expects that the config file does not exist
    """
    userDirPath = pathlib.Path.home()

    if platform.is_windows():
        defautlDataPath = userDirPath.joinpath("AppData", "Local")
    elif platform.is_linux():
        defautlDataPath = userDirPath.joinpath(".config")
    else:
        from utils.DialogCollection import errorOccured

        errorOccured(
            "Platform is not known. App is not supported on your" "platform"
        )
        raise RuntimeError(
            "Platform is not known. App is not supported on your" "platform"
        )

    if os.path.exists(defautlDataPath):
        # creating folder and empty config file
        defautlDataPath = defautlDataPath.joinpath("STManager")
        configPath = defautlDataPath
    else:
        # creating folder and empty config file
        altDataPath = userDirPath.joinpath(".stmanager")
        configPath = altDataPath

    try:
        os.mkdir(configPath)
    except FileExistsError:
        pass

    configPath = configPath.joinpath(ConfigPaths.CONFIG_FILE_FILENAME)

    try:
        from utils.DialogCollection import getFolderPath, askNewUser

        photoDirectory = getFolderPath()

        newLogin, newPassword = askNewUser()

        while newLogin is None or newPassword is None:
            newLogin, newPassword = askNewUser()

        newConfigFileContent = {
            "configuration": {
                "loggedUser": newLogin,
                "scanner_mode": False,
                "savePath": photoDirectory,
            },
            "userData": [
                {
                    "username": newLogin,
                    "password": newPassword,
                    "created": time.strftime("%d-%m-%Y-%H_%M_%S"),
                    "items": [],
                }
            ],
        }

        with open(configPath, "w") as configFile:
            configFile.write(json.dumps(newConfigFileContent))
        return configPath
    except PermissionError:
        from utils.DialogCollection import errorOccured

        errorOccured(
            "Cannot create config file!! Check the permissions "
            "for the application"
        )
        return None
