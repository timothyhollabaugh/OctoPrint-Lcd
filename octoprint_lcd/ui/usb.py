from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.clock import Clock

from kivy.graphics import *

import dbus
from dbus.mainloop.glib import DBusGMainLoop

from .files import FileView

import time, os

from .. import conf
#import octoprint.server as Server
from octoprint.filemanager.util import DiskFileWrapper

class UsbTab(TabbedPanelItem):
    file_list = ObjectProperty(None)
    back = ObjectProperty(None)
    title = StringProperty("")
    dpath = StringProperty("")
    date = NumericProperty(0.0)

    iface = None
    path = None
    cpath = None

    tabbedpanel = None

    files = None
    oldFiles = None

    selected = None

    first = True

    def __init__(self, iface, tabbedpanel, **kwargs):
        super(UsbTab, self).__init__(**kwargs)
        self.iface = iface
        self.tabbedpanel = tabbedpanel
        #self.iface.Unmount({})
        self.path = self.iface.Mount({})
        self.cpath = self.path

        Clock.schedule_interval(self.update, .1)

        print os.listdir(self.path)

    def update(self, dt):
        if self.first:
            self.ids.file_list.bind(minimum_height=self.ids.file_list.setter('height'))
            self.first = False

        if os.path.exists(self.cpath) and os.access(self.cpath, os.R_OK):
            #print self.cpath
            self.files = os.listdir(self.cpath)

            #print self.files

            if self.files != self.oldFiles:
                self.ids.file_list.clear_widgets()
                #print self.files
                for i in self.files:
                    date = os.path.getatime(os.path.join(self.cpath, i))
                    btn = FileView('usb', i, date, size_hint_y=None, height=60)
                    children = self.ids.file_list.children

                    if len(children) > 0:
                        if date <= int(children[0].date):
                            self.ids.file_list.add_widget(btn, index=0)
                        elif date > int(children[len(children)-1].date):
                            self.ids.file_list.add_widget(btn, index=len(children))
                        else:
                            for w in range(len(children)):
                                w = w
                                if date <= int(children[w-1].date) and date >= int(children[w].date):
                                    self.ids.file_list.add_widget(btn, index = w-1)
                                    break
                    else:
                        self.ids.file_list.add_widget(btn)

                self.oldFiles = self.files

            self.selected = None
            for f in ToggleButtonBehavior.get_widgets('usb'):
                if f.state == 'down':
                    self.selected = f
                    break


            if self.selected != None:
                cfile = os.path.join(self.cpath, self.selected.title)
                #print cfile
                if os.path.isdir(cfile):
                    self.cpath = cfile
                    self.selected.state = 'normal'
                    self.ids.copy_button.disabled = True
                else:
                    self.title = self.selected.title
                    self.date = os.path.getatime(cfile)
                    self.ids.copy_button.disabled = False
            else:
                self.title = "No File"
                self.date = ""
                self.ids.copy_button.disabled = True

            self.dpath = os.path.relpath(self.cpath, self.path)

            if os.path.samefile(self.cpath, self.path):
                self.back.disabled = True
            else:
                self.back.disabled = False

        else:
            Clock.unschedule(self.update)
            self.tabbedpanel.switchDefault()
            self.tabbedpanel.removeUsb(self)

    def goback(self):
        self.cpath = os.path.dirname(self.cpath)
        if self.selected != None:
            self.selected.state = 'normal'

    def add(self):
        conf.plugin._file_managerfileManager.add_file('local', self.selected.title, DiskFileWrapper(self.selected.title, os.path.join(self.cpath, self.selected.title), False), allow_overwrite=True)

def start_listening(tabbedpanel):
    DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()

    # Function which will run when signal is received
    def added(*args):
        if 'org.freedesktop.UDisks2.Filesystem' in args[1]:
            print args[0]
            obj = bus.get_object('org.freedesktop.UDisks2', args[0])
            iface = dbus.Interface(obj, 'org.freedesktop.UDisks2.Filesystem')
            usb = UsbTab(iface, tabbedpanel)
            tabbedpanel.addUsb(usb)

    # Which signal to have an eye for
    bus.add_signal_receiver(added, 'InterfacesAdded', 'org.freedesktop.DBus.ObjectManager')

    # Let's start the loop
    import gobject
    gobject.threads_init()      # Without this, we will be stuck in the glib loop
    loop = gobject.MainLoop()
    loop.run()
