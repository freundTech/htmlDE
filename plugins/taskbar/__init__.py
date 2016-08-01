import json
from time import time
from collections import defaultdict
from base64 import b64encode
from xpybutil import ewmh, icccm
from xpybutil.util import get_atom
from htmlDE.helpers.pluginhelpers import sendEvent, ensureArguments

import gi
gi.require_version("Wnck", "3.0")
from gi.repository.Wnck import Screen, Window
from gi.repository import Gtk

dependencies = ["corefunctions"]

screen = None
allWindows = []

def setup():
    global screen
    global allWindows
    screen = Screen.get_default()
    screen.force_update()
    screen.connect("active-window-changed", activeWindowChanged)
    screen.connect("window-opened", windowAdded)
    screen.connect("window-closed", windowRemoved)
    
    allWindows = screen.get_windows()
    for window in allWindows:
        window.connect("state-changed", windowStateChanged)
    
    print("tasks setup")

def getWindows(stacked=False, desktop=-1):
    stacked = False #Stacking not yet implemented js-side
    global allWindows
    windows = defaultdict(list) if stacked else []
    for window in screen.get_windows():
        if window.is_skip_tasklist():
            continue
        if desktop != -1 and window.get_workspace().get_number() != desktop:
            skip_tasklist.append(window)
            continue
        if stacked:
            windows[window.get_class_group().get_name()].append(window.get_xid())
        else:
            windows.append(window.get_xid())
    return windows

def getActiveWindow():
    window = screen.get_active_window()
    if window != None:
        return window.get_xid()

def getPreviouslyActiveWindow():
    window = screen.get_previously_active_window()
    if window != None:
        return window.get_xid()

def getWindowName(xid=None):
    ensureArguments(xid)
    xid = int(xid)
    Window.get(xid).get_name()    

def getWindowIcon(xid=None):
    ensureArguments(xid)
    xid = int(xid)
    image = Window.get(xid).get_icon()
    buf = image.save_to_bufferv("png", [], [])[1]
    return b64encode(buf).decode(), "image/png;base64"

def getWindowGroup(xid=None):
    ensureArguments(xid)
    xid = int(xid)
    return Window.get(xid).get_class_group_name()

def closeWindow(xid=None):
    ensureArguments(xid)
    xid = int(xid)
    Window.get(xid).close(time())

def activateWindow(xid=None):
    ensureArguments(xid)
    xid = int(xid)
    Window.get(xid).activate(time())

def minimizeWindow(xid=None):
    ensureArguments(xid)
    xid = int(xid)
    Window.get(xid).minimize()

def isWindowMinimized(xid=None):
    ensureArguments(xid)
    xid = int(xid)
    return Window.get(xid).is_minimized()

def getWindowNeedsAttention(xid=None):
    ensureArguments(xid)
    xid = int(xid)
    return Window.get(xid).needs_attention()

def activeWindowChanged(screen, previous):
   sendEvent("taskbar", "activeWindowChanged", getActiveWindow()) 

def windowAdded(screen, window):
    allWindows.append(window)
    window.connect("state-changed", windowStateChanged)
    sendEvent("taskbar", "windowAdded", window.get_xid())

def windowRemoved(screen, window):
    allWindows.remove(window)
    sendEvent("taskbar", "windowRemoved", window.get_xid())

def windowStateChanged(window, mask, state):
    if mask.SKIP_TASKLIST:
        if state.SKIP_TASKLIST:
            sendEvent("taskbar", "windowRemoved", window.get_xid())
        else:
            sendEvent("taskbar", "windowAdded", window.get_xid())

public = {
    "getWindows": getWindows,
    "getWindowName": getWindowName,
    "getWindowIcon": getWindowIcon,
    "closeWindow": closeWindow,
    "activateWindow": activateWindow,
    "minimizeWindow": minimizeWindow,
    "isWindowMinimized": isWindowMinimized
}

if __name__ == "__main__":
    setup()
    screen.force_update()
    print(getWindows())
    Gtk.main()
