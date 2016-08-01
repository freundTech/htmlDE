import json
import argparse
from os.path import abspath, join, dirname
from gi.repository import Gtk
from htmlDE.helpers.argumenthelpers import calc_window_coords
from htmlDE.pluginmanager import load_plugins
from htmlDE.windows import BackgroundWindow, PanelWindow

windowtypes = [
    "background",
    "panel"
]

def setup():
    global windows
    global file
    global debug
    global plugins
    windows = []

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="The file to open")
    parser.add_argument("--debug", help="Start in debug mode", action="store_true", default=False)
    args = parser.parse_args()

    file_ = args.file
    debug = args.debug

    window = Gtk.Window()
    screen = window.get_screen()
    nmons = screen.get_n_monitors()
    monitors = []
    for i in range(nmons):
        monitors.append(screen.get_monitor_geometry(i))

    with open(file_) as f:
        config = json.load(f)
    plugins = load_plugins(config["plugins"])
    fileloc = abspath(dirname(args.file))
    for w in config["windows"]:
        if "screens" in w:
            if w["screens"] >= nmons:
                raise Exception("Can't use screen {}. There are only {} screens".format(w["screen"], nmons))
        w = calc_window_coords(w, 0, monitors)
        if w["type"] == "background":
            windows.append(BackgroundWindow("file://"+join(fileloc, w["file"]), w["x"], w["y"], w["width"], w["height"], transparent=w["transparent"]))
        elif w["type"] == "panel":
            windows.append(PanelWindow("file://"+join(fileloc, w["file"]), w["x"], w["y"], w["width"], w["height"], transparent=w["transparent"]))
        else:
            raise Exception("There is no window type called {}.".format(w["type"]))

