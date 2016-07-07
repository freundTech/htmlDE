#!/usr/bin/env python3

import sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from os.path import abspath
from htmlDE import arguments, settings
from htmlDE.pluginmanager import load_plugins
from htmlDE.arguments import parse_args
from htmlDE.windows import BackgroundWindow, PanelWindow

if __name__ == "__main__":
    parse_args()
    Gtk.init(sys.argv)

    settings.setup()

    load_plugins()

    if arguments.type == "background":
        mainWindow = BackgroundWindow('file://'+abspath(arguments.file), arguments.x, arguments.y, arguments.width, arguments.height, transparent=arguments.transparent)
    else:
        mainWindow = PanelWindow('file://'+abspath(arguments.file), arguments.x, arguments.y, arguments.width, arguments.height, transparent=arguments.transparent)

    mainWindow.show_all()
    settings.windows.append(mainWindow)

    Gtk.main()
