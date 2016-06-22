import sys
import inspect
from os import listdir
from os.path import dirname, basename, abspath, isfile, join

plugins = {}

def load_plugins():
	folder = dirname(abspath(sys.argv[0]))+"/plugins"
	
	files = [f[:-3] for f in listdir(folder) if isfile(join(folder, f)) and f.endswith(".py")]
	for file_ in files:
	    plugins[file_] = __import__("plugins."+file_, globals(), locals(), ['object'], 0)
	    setattr(plugins[file_], "print", pluginprint)
	    try:
	        if getattr(plugins[file_], "setup")() == False:
	            raise
	    except:
	        print("{} failed to load".format(file_))
	        plugins.pop(file_)
	    
	    
def getfromplugin(pluginname, path, query):
    obj = plugins[pluginname]
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
        
def pluginprint(*args, **kwargs):
    pluginname = '.'.join(basename(inspect.stack()[1][1]).split(".")[:-1])
    print("["+pluginname+"]",  *args, **kwargs)
