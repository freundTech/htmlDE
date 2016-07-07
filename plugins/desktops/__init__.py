from threading import Thread
import xpybutil
from xpybutil import ewmh, window, event, util
from htmlDE.helpers.pluginhelpers import sendEvent

dependencies = ["corefunctions"]

def setup():
    window.listen(xpybutil.root, "PropertyChange")
    event.connect("PropertyNotify", xpybutil.root, handleEvents)
    t = Thread(target=event.main)
    t.start()
    print("desktops setup")

def handleEvents(e):
    atom = util.get_atom_name(e.atom)
    if atom == '_NET_CURRENT_DESKTOP':
        sendEvent("desktops", "desktopChanged", getCurrentDesktop())

def getCurrentDesktop():
    return ewmh.get_current_desktop().reply()

def getDesktopNames():
    return ewmh.get_desktop_names().reply()

def getNumberOfDesktops():
    return ewmh.get_number_of_desktops().reply()

def setCurrentDesktop(desktop=None):
    ensureArguments(desktop)
    desktop = int(desktop)
    ewmh.request_current_desktop_checked(desktop).check()

public = {
    "getCurrentDesktop": getCurrentDesktop,
    "getDesktopNames": getDesktopNames,
    "getNumberOfDesktops": getNumberOfDesktops,
    "setCurrentDesktop": setCurrentDesktop
}
