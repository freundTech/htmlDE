#!/usr/bin/env python3

import sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from os.path import abspath
from htmlDE.pluginmanager import load_plugins

if __name__ == "__main__":
    Gtk.init(sys.argv)

    load_plugins()

    Gtk.main()
