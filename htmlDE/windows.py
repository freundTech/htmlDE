import json
from urllib.parse import urlparse, parse_qs
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("WebKit", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, WebKit, GObject
import cairo

from htmlDE.helpers.regionhelpers import cairo_region_create_from_surface
from htmlDE.pluginmanager import getfromplugin, inject_libraries

mask_accuracy = 5

class _HtmlDeWindow(Gtk.Window):
    webview = None
    isPageLoaded = False

    def __init__(self, url, posx, posy, width, height, transparent):
        Gtk.Window.__init__(self, Gtk.WindowType.TOPLEVEL, title='')
        self.transparent = transparent
        self.move(posx, posy)
        self.set_default_size(width, height)
        self.set_decorated(False)
        
        
        self.webview = WebKit.WebView()
        
        settings = self.webview.get_settings()
        settings.set_property("enable-universal-access-from-file-uris", True)
        self.webview.set_settings(settings)

        self.add(self.webview)
        
        if (self.transparent):
            self.webview.set_transparent(True)
            self.installTransparency(self)
            self.installTransparency(self.webview)
    
        self.connect("delete_event", self.close_application)

        self.webview.connect("context-menu", self.context_menu)
        self.webview.connect("navigation-policy-decision-requested", self.navigation_requested)
        self.webview.connect("resource-request-starting", self.resource_request_starting)

        self.webview.load_uri(url)
        inject_libraries(self.webview)

    def do_draw(self, cr):
        Gtk.Window.do_draw(self, cr)
        if (self.transparent):
            width, height = self.get_size()
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
            cr = cairo.Context(surface)
            self.webview.draw(cr)
            region = cairo_region_create_from_surface(surface, mask_accuracy)
            self.input_shape_combine_region(None)
            self.input_shape_combine_region(region)

    def installTransparency(self, component):
        component.set_visual(component.get_screen().get_rgba_visual())
        
        component.override_background_color(Gtk.StateFlags.ACTIVE, Gdk.RGBA(0, 0, 0, 0))
        component.override_background_color(Gtk.StateFlags.BACKDROP, Gdk.RGBA(0, 0, 0, 0))
        component.override_background_color(Gtk.StateFlags.DIR_LTR, Gdk.RGBA(0, 0, 0, 0))
        component.override_background_color(Gtk.StateFlags.DIR_RTL, Gdk.RGBA(0, 0, 0, 0))
        component.override_background_color(Gtk.StateFlags.FOCUSED, Gdk.RGBA(0, 0, 0, 0))
        component.override_background_color(Gtk.StateFlags.INCONSISTENT, Gdk.RGBA(0, 0, 0, 0))
        component.override_background_color(Gtk.StateFlags.INSENSITIVE, Gdk.RGBA(0, 0, 0, 0))
        component.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 0))
        component.override_background_color(Gtk.StateFlags.PRELIGHT, Gdk.RGBA(0, 0, 0, 0))
        component.override_background_color(Gtk.StateFlags.SELECTED, Gdk.RGBA(0, 0, 0, 0))
        
    def open(self, url):
        self.webview.open(url)

    def resource_request_starting(self, webview, webframe, webresource, request, response):
        url = urlparse(request.get_uri())
        if url.scheme != "python":
            return
        message = request.get_message()
        #I have no idea how to get the query for other methods. The request body is empty!
        if message.get_property("method") != "GET": 
            print("Unsupported method")
            return
        query = dict(parse_qs(url.query))
        
        try:
            result = getfromplugin(url.netloc, url.path[1:].replace("/", "."), query)
            if result == None:
                request.set_uri("about:blank")
            else:
                return_ = {
                    "status": 0,
                    "result": str(result),
                }
                request.set_uri("data:application/json,"+json.dumps(return_))
        except AttributeError as err:
            request.set_uri("data:application/json,{\"status\": 1, \"error\": \""+str(err)+"\"}")
        

    #Prevent navigation. For example by clicking on links
    def navigation_requested(self, widget, frame, request, action, decision):
        if self.isPageLoaded:
            return True
        else:
            self.isPageLoaded = True

    #Disable context menu
    def context_menu(self, widget, result, keyboard, user_data):
        return True

    def close_application(self, widget, event, data=None):
        Gtk.main_quit()


class HtmlDeBackgroundWindow(_HtmlDeWindow):
    def __init__(self, url, posx, posy, width, height, transparent=False):
        _HtmlDeWindow.__init__(self, url, posx, posy, width, height, transparent)
        self.set_type_hint(Gdk.WindowTypeHint.DESKTOP)

class HtmlDePanelWindow(_HtmlDeWindow):
    def __init__(self, url, posx, posy, width, height, transparent=True):
        _HtmlDeWindow.__init__(self, url, posx, posy, width, height, transparent)
        self.set_type_hint(Gdk.WindowTypeHint.DOCK)

