import pathlib
import os
from fbs_runtime import platform

def getDefConfigPath() -> str:
    """
    Depending on platform, returns suggested config path.
    On unix based systems, creates path to dotfile .stmanager/appData.json.
    Prefferably .config path
    On windows show path to the %Appdata%/Local
    """
    p = pathlib.Path.home()
    if platform.is_windows():
        p = p.joinpath("%APPDATA%", "Local", "STManager")
    elif platform.is_linux():
        pConfig = p.joinpath(".config")
        if os.path.exists(pConfig):
            p = pConfig.joinpath("stmanager")
        else:
            p = p.joinpath(".stmanager")
    
    p = p.joinpath("appData.json")
    return str(p.absolute())


def constructPath(inputPath:str) -> bool:
    """
    Path and makes sure that all directories
    exist, if not -> return False.
    If path is default -> contructs directories.
    """
    if path == getDefConfigPath():
        if platform.is_windows():
            dirpath = os.dirname(
                str(pathlib.PureWindowsPath(inputPath)))

        elif platform.is_linux():
            pass

        if not os.path.exists(dirpath):
        access_rights = 755
        try:
            os.mkdir(dirpath, access_rights)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        return True
    elif os.path.exists(os.dirname(inputPath)):
        return True
    return False




def lookForConfig() -> str:
    """
    Looks for config file from default location. 
    Diffrent behaviour per platform
    If found one -> returns path, otherwise
    returns empty string
    """
    if os.path.exists(p := getDefConfigPath()):
        return p
    else:
        return ""
