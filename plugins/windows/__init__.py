import sys
from os.path import abspath, dirname
from urllib.parse import urlparse
from htmlDE.windows import BackgroundWindow, PanelWindow
from htmlDE.helpers.pluginhelpers import ensureArguments

windows = {}

def setup():
    mainWindow = PanelWindow('file://'+abspath(sys.argv[1]), 0, 0, 1000, 500, transparent=True)
    mainWindow.show_all()
    
    windows["main"] = mainWindow
    print("windows setup")

def list():
    return windows.keys()

def createBackgroundWindow(name=None, url=None, x=None, y=None, width=None, height=None, transparent=False, own=None):
    ensureArguments(name, url, x, y, width, height, own)
    x = int(x)
    y = int(y)
    width = int(width)
    height = int(height)
    path = dirname(urlparse(own).path)
    url = "file://"+path+"/"+url
    windows[name] = BackgroundWindow(url, x, y, width, height, transparent)
    windows[name].show_all()

def createPanelWindow(name=None, url=None, x=None, y=None, width=None, height=None, transparent=True, own=None):
    ensureArguments(name, url, x, y, width, height, own)
    x = int(x)
    y = int(y)
    width = int(width)
    height = int(height)
    path = dirname(urlparse(own).path)
    url = "file://"+path+"/"+url
    windows[name] = PanelWindow(url, x, y, width, height, transparent)
    windows[name].show_all()

public = {
    "list": list,
    "createBackgroundWindow": createBackgroundWindow,
    "createPanelWindow": createPanelWindow
}
