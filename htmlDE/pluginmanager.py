import sys
import inspect
from os import listdir
from os.path import dirname, basename, abspath, isfile, isdir, join
from collections import OrderedDict

_plugins = {}

def load_plugins():
        global _plugins
        folder = join(dirname(abspath(sys.argv[0])), "plugins")

        installedplugins = [f for f in listdir(folder) if isdir(join(folder, f)) and f != "__pycache__"]
        loadedplugins = {}
        for pluginname in installedplugins:
                loadedplugins[pluginname] = __import__("plugins."+pluginname, globals(), locals(), ['object'], 0)
        _plugins = _sortplugins(loadedplugins)
        for plugin in _plugins:
            _plugins[plugin].setup()

def getfromplugin(pluginname, path, query):
    obj = _plugins[pluginname].public
    attributes = path.split(".")
    obj = obj[attributes[0]]
    for attr in attributes[1:]:
        obj = getattr(obj, attr)

    if callable(obj):
        return obj(**query)
    else:
        return obj

def inject_libraries(webview):
    folder = join(dirname(abspath(sys.argv[0])), "plugins")
    webview.execute_script("window.plugins = {}")
    plugins = list(_plugins.keys())
    for plugin in plugins:
        file_ = join(folder, plugin, "js", "main.js")
        if isfile(file_):
            with open(file_, 'r') as f:
                script = f.read()
                webview.execute_script("window.plugins.{}=".format(plugin)+script)

def pluginprint(*args, **kwargs):
    pluginname = basename(dirname(inspect.stack()[1][1]))
    print("["+pluginname+"]",  *args, **kwargs)

def _sortplugins(plugins):
    sortedplugins = OrderedDict()
    deps = {}
    for key in plugins.keys():
        deps[key] = plugins[key].dependencies[:]
    while True:
        count = len(plugins)
        for key in list(plugins.keys()):
            if len(deps[key]) == 0:
                sortedplugins[key] = plugins.pop(key)
                for plugin in deps:
                    if key in deps[plugin]:
                        deps[plugin].remove(key)
        if len(plugins) == 0:
            break
        if count == len(plugins):
            print("The following plugins have missing cyclic dependencies:")
            for key in plugins.keys():
                print(key)
            break
    return sortedplugins
