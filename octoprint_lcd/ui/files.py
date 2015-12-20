from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors import ToggleButtonBehavior

from kivy.graphics import *

from .status import FilamentLabel

import time

import octoprint.server as Server

class FileView(ToggleButtonBehavior, BoxLayout):
    title=StringProperty(None)
    date=NumericProperty(0.0)
    def __init__(self, group, title, date, **kwargs):
        super(FileView, self).__init__(**kwargs)
        self.group = group
        self.title = title
        self.date = date
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
    title = StringProperty("")
    date = NumericProperty(0.0)

    etime = ObjectProperty(None)
    filaBox = ObjectProperty(None)

    selected = None
    oldSelected = None
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
                date = self.files['local'][i]['date']
                btn = FileView('files', self.files['local'][i]['name'], date, size_hint_y=None, height=60)
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
            self.date = 0
            self.etime.title = ""
            self.etime.time = ""
            self.ids.print_button.disabled = True
            self.ids.load_button.disabled = True
            self.ids.delete_button.disabled = True
        else:
            #print self.selected.title
            file = self.files['local'][self.selected.title]
            #print file
            self.title = f.title
            self.date = f.date

            if('analysis' in file.keys()):
                etime = file['analysis']['estimatedPrintTime']

                if not etime == None:
                    m, s = divmod(int(etime), 60)
                    h, m = divmod(m, 60)
                else:
                    h, m, s = 0, 0, 0

                self.etime.title = "Estimated"
                self.etime.time = str("%02d:%02d:%02d" % (h, m, s))
                filament = file['analysis']['filament']

                if(self.selected != self.oldSelected):
                    self.filaBox.clear_widgets()
                    if len(filament) == 1 and Server.printer.get_current_connection()[3]['extruder']['count'] == 1:
                        fila_widget = FilamentLabel()
                        fila_widget.title = "Usage:"
                        fila_widget.name = 'tool0'
                        self.filaBox.add_widget(fila_widget)
                    else:
                        for i in range(len(filament)):
                            fila_widget = FilamentLabel()
                            fila_widget.title = "Tool " + str(i) + " Usage:"
                            fila_widget.name = 'tool' + str(i)
                            self.filaBox.add_widget(fila_widget)

                    self.oldSelected = self.selected

                for i in self.filaBox.children:
                    if isinstance(i, FilamentLabel):
                        i.update(filament)
            else:
                pass
                #self.etime = "--:--:--"
                #self.tool0l = " - - "
                #self.tool0v = " - - "
                #self.tool1l = " - - "
                #self.tool1v = " - - "
                #self.tool2l = " - - "
                #self.tool2v = " - - "

            if Server.printer.is_printing() or Server.printer.is_closed_or_error():
                self.ids.print_button.disabled = True
            else:
                self.ids.print_button.disabled = False

            if Server.printer.get_current_job()['file']['name'] == f.title or Server.printer.is_printing() or Server.printer.is_closed_or_error():
                self.ids.load_button.disabled = True
            else:
                self.ids.load_button.disabled = False

            self.ids.delete_button.disabled = False
