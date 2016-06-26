import sys
from os.path import abspath, dirname
from urllib.parse import urlparse
from htmlDE.windows import BackgroundWindow, PanelWindow
from htmlDE.helpers.pluginhelpers import ensureArguments

windows = []

def setup():
    mainWindow = PanelWindow('file://'+abspath(sys.argv[1]), 0, 0, 1000, 500, transparent=True)
    mainWindow.show_all()
    
    windows.append(mainWindow)
    print("windows setup")

def createBackgroundWindow(url=None, x=None, y=None, width=None, height=None, transparent=False, own=None):
    ensureArguments(url, x, y, width, height, own)
    x = int(x)
    y = int(y)
    width = int(width)
    height = int(height)
    path = dirname(urlparse(own).path)
    url = "file://"+path+"/"+url
    id = len(windows)
    windows.append(BackgroundWindow(url, x, y, width, height, transparent))
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
    id = len(windows)
    windows.append(PanelWindow(url, x, y, width, height, transparent))
    windows[id].show_all()
    return {"id": id}

def deleteWindow(id=None):
    ensureArguments(id)
    id = int(id)
    if id < len(windows) and windows[id] != None:
        windows[id].destroy()
        windows.pop(id)

def moveWindow(id=None, x=None, y=None):
    ensureArguments(id, x, y)
    id = int(id)
    x = int(x)
    y = int(y)
    if id < len(windows) and windows[id] != None:
        windows[id].move(x, y);

public = {
    "createBackgroundWindow": createBackgroundWindow,
    "createPanelWindow": createPanelWindow,
    "deleteWindow": deleteWindow,
    "moveWindow": moveWindow
}
