import json
from gi.repository import GObject
from htmlDE import settings

def ensureArguments(*args):
    for i, arg in enumerate(args):
        if arg == None:
            raise ArgumentsError("Argument {} is None".format(i))
    return True

def normalizeArguments(*args):
    for i, arg in enumerate(args):
        try:
            if len(arg) == 1:
                args[i] = args[i][0]
        except:
            pass
    return args


def sendEvent(pluginname, eventname, data):
    GObject.idle_add(_sendEvent, pluginname, eventname, data)

def _sendEvent(pluginname, eventname, data):
    for window in settings.windows:
        window.webview.execute_script("window.{}.events.dispatch(\"{}\", {})".format(pluginname, eventname, json.dumps(data, separators=(',',':'))))
