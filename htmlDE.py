#!/usr/bin/env python3

import sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from os.path import abspath
from signal import signal, SIGINT, SIG_DFL
from htmlDE import settings
from htmlDE.pluginmanager import load_plugins
from htmlDE.arguments import parse_args
from htmlDE.windows import BackgroundWindow, PanelWindow

if __name__ == "__main__":
    Gtk.init(sys.argv)

    settings.setup()
    
    for window in settings.windows:
        window.show_all()
    
    signal(SIGINT, SIG_DFL)

    Gtk.main()
