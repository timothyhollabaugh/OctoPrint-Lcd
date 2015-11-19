from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors import ToggleButtonBehavior

from kivy.graphics import *

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
        print self.title, state
        if state == 'normal':
            self.setBackground(0.4, 0.4, 0.4)
        elif state == 'down':
            self.setBackground(0.6, 0.6, 0.6)

    def setBackground(self, r, g, b):
        with self.canvas.before:
            Color(r, g, b, 1)
            Rectangle(pos=self.pos, size=self.size)

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

        if(self.files != self.oldFiles):
            print "different"
            print self.oldFiles
            self.ids.file_list.clear_widgets()
            for i in self.files['local']:
                btn = FileView(self.files['local'][i], size_hint_y=None, height=60)
                for w in range(self.ids.file_list.children.size)
                    if self.files[min(w-1, 0)]
                self.ids.file_list.add_widget(btn)
            self.oldFiles = self.files
