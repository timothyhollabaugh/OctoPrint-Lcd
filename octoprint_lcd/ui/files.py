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
            #print "different"
            #print self.oldFiles
            self.ids.file_list.clear_widgets()

            #dates = [2, 3, 1, 5, 4]

            for i in self.files['local']:
            #for i in dates:
                btn = FileView(self.files['local'][i], size_hint_y=None, height=60)
                #btn = FileView({'name': 'Test', 'date': i}, size_hint_y=None, height=60)
                children = self.ids.file_list.children
                date = self.files['local'][i]['date']
                #date = i
                #print len(children)
                #print "Date:", date

                if len(children) > 0:
                    #print "Child:", children[0].date
                    if date <= int(children[0].date) :
                        #print "First:", date, children[0].date
                        #print date <= children[0].date
                        self.ids.file_list.add_widget(btn, index=0)
                        #for c in children:
                        #    print c.date
                        #time.sleep(1)
                    elif date > int(children[len(children)-1].date):
                        #print "Second:", date , children[len(children)-1].date
                        self.ids.file_list.add_widget(btn, index=len(children))
                        #for c in children:
                        #    print c.date
                        #time.sleep(1)
                    else:
                        #print "Third: "
                        for w in range(len(children)):
                            w = w
                            #print "w: ", w
                            if date <= int(children[w-1].date) and date >= int(children[w].date):
                                #print date, children[w-1].date, children[w].date
                                self.ids.file_list.add_widget(btn, index = w-1)
                                break
                                #for c in children:
                                #    print c.date
                                #time.sleep(1)
                else:
                    self.ids.file_list.add_widget(btn)
                    for c in children:
                        print c.date
                    time.sleep(1)

            self.oldFiles = self.files
