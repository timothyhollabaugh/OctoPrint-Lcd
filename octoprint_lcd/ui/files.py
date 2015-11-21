from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors import ToggleButtonBehavior

from kivy.graphics import *

import time

import octoprint.server as Server

class FileView(ToggleButtonBehavior, BoxLayout):
    title=StringProperty(None)
    date=StringProperty(None)
    def __init__(self, file, **kwargs):
        super(FileView, self).__init__(**kwargs)
        self.group = 'files'
        self.title = file['name']
        self.date = str(file['date'])
        self.bind(state=self.changeState)
        #print file

    def changeState(self, button, state):
        if state == 'normal':
            self.setBackground(0.4, 0.4, 0.4)
        elif state == 'down':
            self.setBackground(0.6, 0.6, 0.6)

    def setBackground(self, r, g, b):
        with self.canvas.before:
            Color(r, g, b, 1)
            Rectangle(pos=self.pos, size=self.size)
            Color(0.5, 0.5, 0.5, 1)
            Line(points=[self.pos[0]+15, self.pos[1], self.pos[0]+self.width-15, self.pos[1]])

class FilesTab(BoxLayout):
    file_list=ObjectProperty(None)
    title = StringProperty("")
    date = StringProperty("")
    etime = StringProperty("")
    ltime = StringProperty("")
    tool0l = StringProperty("")
    tool1l = StringProperty("")
    tool2l = StringProperty("")
    tool0v = StringProperty("")
    tool1v = StringProperty("")
    tool2v = StringProperty("")
    selected = None
    first = True
    oldFiles = {}
    files = {}

    def __init__(self, **kwargs):
        super(FilesTab, self).__init__(**kwargs)
        self.files = Server.fileManager.list_files()

    def update(self, dt):
        self.files = Server.fileManager.list_files()
        if self.first:
            self.ids.file_list.bind(minimum_height=self.ids.file_list.setter('height'))
            self.first = False

        if self.files != self.oldFiles:
            self.ids.file_list.clear_widgets()
            #print self.files
            for i in self.files['local']:
                btn = FileView(self.files['local'][i], size_hint_y=None, height=60)
                children = self.ids.file_list.children
                date = self.files['local'][i]['date']

                if len(children) > 0:
                    if date <= int(children[0].date) :
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
                    #for c in children:
                    #    print c.date
                    #time.sleep(1)

            self.oldFiles = self.files

        self.selected = None
        for f in ToggleButtonBehavior.get_widgets('files'):
            if f.state == 'down':
                self.selected = f
                break

        if self.selected == None or not self.selected.title in self.files['local'].keys():
            #print "None"
            self.title = "No File"
            self.date = ""
            self.etime = "--:--:--"
            self.tool0l = " - - "
            self.tool0v = " - - "
            self.tool1l = " - - "
            self.tool1v = " - - "
            self.tool2l = " - - "
            self.tool2v = " - - "
        else:
            #print self.selected.title
            file = self.files['local'][self.selected.title]
            #print file
            self.title = f.title
            self.date = str(f.date)

            if('analysis' in file.keys()):
                etime = file['analysis']['estimatedPrintTime']

                if not etime == None:
                    m, s = divmod(int(etime), 60)
                    h, m = divmod(m, 60)
                else:
                    h, m, s = 0, 0, 0

                self.etime = str("%02d:%02d:%02d" % (h, m, s))
            else:
                self.etime = "--:--:--"

            filament = file['analysis']['filament']
            changed = []
            if filament != None:
                if 'tool0' in filament.keys():
                    self.tool0l = str("%.2f" % (filament['tool0']['length']/1000))
                    self.tool0v = str("%3.2f" % filament['tool0']['volume'])
                else:
                    self.tool0l = " - - "
                    self.tool0v = " - - "
                if 'tool1' in filament.keys():
                    self.tool1l = str("%.2f" % (filament['tool0']['length']/1000))
                    self.tool1v = str("%3.2f" % filament['tool0']['volume'])
                else:
                    self.tool1l = " - - "
                    self.tool1v = " - - "
                if 'tool2' in filament.keys():
                    self.tool2l = str("%.2f" % (filament['tool0']['length']/1000))
                    self.tool2v = str("%3.2f" % filament['tool0']['volume'])
                else:
                    self.tool2l = " - - "
                    self.tool2v = " - - "
