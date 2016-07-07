import sys
from os.path import abspath, dirname
from urllib.parse import urlparse
from htmlDE import settings
from htmlDE.windows import BackgroundWindow, PanelWindow
from htmlDE.helpers.pluginhelpers import ensureArguments

dependencies = ["corefunctions"]

def setup():
    print("windows setup")

def createBackgroundWindow(url=None, x=None, y=None, width=None, height=None, transparent=False, own=None):
    ensureArguments(url, x, y, width, height, own)
    x = int(x)
    y = int(y)
    width = int(width)
    height = int(height)
    path = dirname(urlparse(own).path)
    url = "file://"+path+"/"+url
    id = len(settings.windows)
    settings.windows.append(BackgroundWindow(url, x, y, width, height, transparent))
    windows[id].show_all()
    return {"id": id}

def createPanelWindow(url=None, x=None, y=None, width=None, height=None, transparent=True, own=None):
    ensureArguments(url, x, y, width, height, own)
    x = int(x)
    y = int(y)
    width = int(width)
    height = int(height)
    path = dirname(urlparse(own).path)
    url = "file://"+path+"/"+url
    id = len(settings.windows)
    settings.windows.append(PanelWindow(url, x, y, width, height, transparent))
    settings.windows[id].show_all()
    return {"id": id}

def deleteWindow(id=None):
    ensureArguments(id)
    id = int(id)
    if id < len(settings.windows) and settings.windows[id] != None:
        settings.windows[id].destroy()
        settings.windows[id] = None

def moveWindow(id=None, x=None, y=None):
    ensureArguments(id, x, y)
    id = int(id)
    x = int(x)
    y = int(y)
    if id < len(settings.windows) and settings.windows[id] != None:
        settings.windows[id].move(x, y);

def resizeWindow(id=None, width=None, height=None):
    ensureArguments(id, width, height)
    id = int(id)
    width = int(width)
    height = int(height)
    if id < len(settings.windows) and settings.windows[id] != None:
        settings.windows[id].resize(width, height);

def getWindowPosition(id=None):
    ensureArguments(id)
    id = int(id)
    pos = settings.windows[id].get_position()

    return {"x": pos[0], "y": pos[1]}

def getWindowSize(id=None):
    ensureArguments(id)
    id = int(id)
    pos = settings.windows[id].get_geometry()

    return {"width": pos[2], "height": pos[3]}

public = {
    "createBackgroundWindow": createBackgroundWindow,
    "createPanelWindow": createPanelWindow,
    "deleteWindow": deleteWindow,
    "moveWindow": moveWindow,
    "resizeWindow": resizeWindow,
    "getWindowPosition": getWindowPosition,
    "getWindowSize": getWindowSize
}
