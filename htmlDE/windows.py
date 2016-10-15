import json
from urllib.parse import urlparse, parse_qsl
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, WebKit2, GObject
import cairo

from htmlDE.helpers.regionhelpers import cairo_region_create_from_surface
from htmlDE.pluginmanager import getfromplugin, inject_libraries

mask_accuracy = 5

mainWindow = None

class _Window(Gtk.Window):
    webview = None
    isPageLoaded = False

    def __init__(self, url, posx, posy, width, height, transparent):
        Gtk.Window.__init__(self, Gtk.WindowType.TOPLEVEL, title='')
        self.transparent = transparent
        self.move(posx, posy)
        self.set_default_size(width, height)
        self.set_decorated(False)
        
        
        self.webview = WebKit2.WebView()
        
        settings = self.webview.get_settings()
        settings.set_allow_file_access_from_file_urls(True)
        settings.set_allow_universal_access_from_file_urls(True)
        settings.set_enable_webgl(True)
        self.webview.set_settings(settings)

        self.add(self.webview)
        
        if (self.transparent):
            self.webview.set_background_color(Gdk.RGBA(0, 0, 0, 0))
            self.installTransparency(self)
            self.installTransparency(self.webview)
    
        self.connect("delete_event", self.close_application)

        self.webview.connect("context-menu", self.context_menu)
        self.webview.connect("decide-policy", self.navigation_requested)
        self.webview.connect("resource-load-started", self.resource_load_started)

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

    def resource_load_started(self, webview, resource, request):
        url = urlparse(request.get_uri())
        if url.scheme != "python":
            return
        #I have no idea how to get the query for other methods. The request body is empty!
        if request.get_http_method() != "GET": 
            print("Unsupported method")
            return
        query = dict(parse_qsl(url.query))
        
        try:
            result = getfromplugin(url.netloc, url.path[1:].replace("/", "."), query)
            if result == None:
                request.set_uri("about:blank")
            else:
                if type(result) == tuple:
                    returntype = result[1]
                    return_ = result[0]
                else:
                    returntype = "application/json"
                    return_ = json.dumps({
                        "status": 0,
                        "result": result,
                    })
                request.set_uri("data:"+returntype+","+return_)
        except AttributeError as err:
            request.set_uri("data:application/json,{\"status\": 1, \"error\": \""+str(err)+"\"}")
        

    #Prevent navigation. For example by clicking on links
    def navigation_requested(self, webview, decision, type_):
        if type_ == WebKit2.PolicyDecisionType.NAVIGATION_ACTION:
            if self.isPageLoaded:
                decision.ignore()
            else:
                self.isPageLoaded = True

    #Disable context menu
    def context_menu(self, webview, context_menu, event, hit_test_result):
        return True

    def close_application(self, widget, event, data=None):
        Gtk.main_quit()


class BackgroundWindow(_Window):
    def __init__(self, url, posx, posy, width, height, transparent=False):
        _Window.__init__(self, url, posx, posy, width, height, transparent)
        self.set_type_hint(Gdk.WindowTypeHint.DESKTOP)

class PanelWindow(_Window):
    def __init__(self, url, posx, posy, width, height, transparent=True):
        _Window.__init__(self, url, posx, posy, width, height, transparent)
        self.set_type_hint(Gdk.WindowTypeHint.DOCK)
        self.stick()
