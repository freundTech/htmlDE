import sys
import inspect
from os import listdir
from os.path import dirname, basename, abspath, isfile, isdir, join

_plugins = {}

def load_plugins():
	folder = join(dirname(abspath(sys.argv[0])), "plugins")
	
	plugins = [f for f in listdir(folder) if isdir(join(folder, f))]
	for plugin in plugins:
	    _plugins[plugin] = __import__("plugins."+plugin, globals(), locals(), ['object'], 0)
	    setattr(_plugins[plugin], "print", pluginprint)
	    try:
	        if getattr(_plugins[plugin], "setup")() == False:
	            raise
	    except:
	        print("{} failed to load".format(plugin))
	        _plugins.pop(plugin)
	    
	    
def getfromplugin(pluginname, path, query):
    obj = _plugins[pluginname]
    attributes = path.split(".")
    for attr in attributes:
        try:
            obj = getattr(obj, attr)
        except AttributeError as err:
            raise err
    if callable(obj):
        return obj(**query)
    else:
        return obj

def inject_libraries(webview):
    folder = join(dirname(abspath(sys.argv[0])), "plugins")

    webview.execute_script("window.plugins = {}")
    for plugin in _plugins.keys():
        file_ = join(folder, plugin, "js", "main.js")
        if isfile(file_):
            with open(file_, 'r') as f:
                script = f.read()
                webview.execute_script("window.plugins.{}=".format(plugin)+script)

def pluginprint(*args, **kwargs):
    pluginname = basename(dirname(inspect.stack()[1][1]))
    print("["+pluginname+"]",  *args, **kwargs)
