#!/usr/bin/env python3

import sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from os.path import abspath

from htmlDE.windows import HtmlDePanelWindow
from htmlDE.pluginmanager import load_plugins

if __name__ == "__main__":
    Gtk.init(sys.argv)

    load_plugins()

    mainWindow = HtmlDePanelWindow('file://'+abspath(sys.argv[1]), 0, 0, 1000, 500, transparent=True)
    mainWindow.show_all()
    
    Gtk.main()
