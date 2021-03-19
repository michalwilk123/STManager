import pathlib
import os
import time
import json
from fbs_runtime import platform

CONFIG_FILE_FILENAME = "appData.json"


def findConfigFilePath() -> str:
    """
    Looks for config file from default location.
    Diffrent behaviour per platform
    If found one -> returns path, otherwise
    returns None.

    Windows:
    1) AppData\\Local\\STManager
    2) \\User\\.stmanager

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
            found := p.joinpath(
                "%APPDATA%", "Local", "STManager", CONFIG_FILE_FILENAME
            )
        ):
            return found
        elif os.path.exists(
            found := p.joinpath(".stmanager", CONFIG_FILE_FILENAME)
        ):
            return found

        return None  # config file not found -> returning None
    elif platform.is_linux():
        if os.path.exists(
            found := p.joinpath(".config", "STManager", CONFIG_FILE_FILENAME)
        ):
            return found
        elif os.path.exists(
            found := p.joinpath(".stmanager", CONFIG_FILE_FILENAME)
        ):
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
        altDataPath = p.joinpath(".stmanager")
        configPath = altDataPath

    try:
        os.mkdir(configPath)
    except FileExistsError:
        pass

    configPath = configPath.joinpath(CONFIG_FILE_FILENAME)

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
