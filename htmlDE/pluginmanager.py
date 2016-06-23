import sys
import inspect
from os import listdir
from os.path import dirname, basename, abspath, isfile, join

_plugins = {}

def load_plugins():
	folder = join(dirname(abspath(sys.argv[0])), "plugins")
	
	files = [f[:-3] for f in listdir(folder) if isfile(join(folder, f)) and f.endswith(".py")]
	for file_ in files:
	    _plugins[file_] = __import__("plugins."+file_, globals(), locals(), ['object'], 0)
	    setattr(_plugins[file_], "print", pluginprint)
	    try:
	        if getattr(_plugins[file_], "setup")() == False:
	            raise
	    except:
	        print("{} failed to load".format(file_))
	        _plugins.pop(file_)
	    
	    
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
    folder = join(dirname(abspath(sys.argv[0])), "plugins", "js")

    webview.execute_script("window.plugins = {}")
    for plugin in _plugins.keys():
        file_ = join(folder, plugin+".js")
        if isfile(file_):
            with open(file_, 'r') as f:
                script = f.read()
                webview.execute_script("window.plugins.{}=".format(plugin)+script)

def pluginprint(*args, **kwargs):
    pluginname = '.'.join(basename(inspect.stack()[1][1]).split(".")[:-1])
    print("["+pluginname+"]",  *args, **kwargs)
