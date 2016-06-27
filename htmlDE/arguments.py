import argparse
from gi.repository import Gtk, Gdk
from htmlDE.helpers.argumenthelpers import get_pixels_from_argument

windowtypes = [
        "background",
        "panel"
]

def parse_args():
    global file
    global x
    global y
    global width
    global height
    global type
    global screen
    global transparent
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="The file to open")
    parser.add_argument("x", help="The x position of the window as pixels or percentage")
    parser.add_argument("y", help="The y position of the window as pixels or percentage")
    parser.add_argument("width", help="The width of the window as pixels or percentage")
    parser.add_argument("height", help="The height of the window as pixels or percentage")
    parser.add_argument("type", help="The type of the window. Valid values are \"background\" and \"panel\"")
    parser.add_argument("--screen", help="Which screen to display the window on. Default is 0", default=0)
    parser.add_argument("--transparent", help="If set the window has a transparent background", action="store_true", default=False)
    args = parser.parse_args()
    
    file = args.file
    window = Gtk.Window()
    screen = window.get_screen()
    nmons = screen.get_n_monitors()
    if args.screen >= nmons:
        print("Can't use screen {}. There are only {} screens".format(args.screen, nmons))
        exit(1)
    global monitors
    monitors = []
    for i in range(nmons):
        monitors.append(screen.get_monitor_geometry(i))
    x = get_pixels_from_argument(args.x, monitors[args.screen].width)
    x += monitors[args.screen].x
    y = get_pixels_from_argument(args.y, monitors[args.screen].height)
    y += monitors[args.screen].y
    width = get_pixels_from_argument(args.width, monitors[args.screen].width)
    height = get_pixels_from_argument(args.height, monitors[args.screen].height)
    
    if args.type.lower() not in windowtypes:
        print("{} is not a supported window type".format(args.type))
        exit(1)
    type = args.type.lower()
    transparent = args.transparent
    window.destroy()
