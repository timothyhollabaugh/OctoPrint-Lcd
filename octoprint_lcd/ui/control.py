from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.button import Button
from kivy.properties import ObjectProperty

from .status import TemperatureLabel

import octoprint.server as Server

class TempKeypad(BoxLayout):

    tempBox = ObjectProperty(None)

    profile = None
    oldProfile = None

    tempIn = ObjectProperty(None)
    tool = ""

    def on_touch_down(self, touch):
        if self.collide_point(touch.pos[0], touch.pos[1]) and not self.ids.keypad.collide_point(touch.pos[0], touch.pos[1]):
            return True
        else:
            if not self.collide_point(touch.pos[0], touch.pos[1]):
                self.remove()
                return False
            elif super(TempKeypad, self).on_touch_down(touch):
                return True
            else:
                return False

    def remove(self):
        print self.tool
        if self.tempIn.text != "":
            Server.printer.set_temperature(self.tool, int(self.tempIn.text))
        self.parent.remove_widget(self)

class ControlTab(FloatLayout):

    profile = None
    oldProfile = None

    def update(self, dt):

        self.profile = Server.printer.get_current_connection()[3]

        if self.profile != self.oldProfile:
            self.tempBox.clear_widgets()
            if self.profile != None:
                if self.profile['heatedBed']:
                    box = BoxLayout()

                    label = TemperatureLabel()
                    label.size_hint_x = 0.8
                    label.title = "Bed:"
                    label.name = 'bed'
                    box.add_widget(label)

                    btn = Button()
                    btn.text = "Set"
                    btn.size_hint_x = 0.2
                    btn.on_press = lambda: self.showKeyboard('bed', "Bed")
                    box.add_widget(btn)

                    self.tempBox.add_widget(box)

                if self.profile['extruder']['count'] == 1:
                    box = BoxLayout()

                    label = TemperatureLabel()
                    label.size_hint_x = 0.8
                    label.title = "Tool:"
                    label.name = 'tool0'
                    box.add_widget(label)

                    btn = Button()
                    btn.text = "Set"
                    btn.size_hint_x = 0.2
                    btn.on_press = lambda: self.showKeyboard('tool0', "Tool")
                    box.add_widget(btn)

                    self.tempBox.add_widget(box)
                else:
                    for i in range(self.profile['extruder']['count']):
                        box = BoxLayout()

                        label = TemperatureLabel()
                        label.size_hint_x = 0.8
                        label.title = "Tool " + str(i) + ":"
                        label.name = 'tool' + str(i)
                        box.add_widget(label)

                        btn = Button()
                        btn.text = "Set"
                        btn.size_hint_x = 0.2
                        btn.on_press = lambda i=i: self.showKeyboard('tool' + str(i), "Tool " + str(i) + ":")
                        box.add_widget(btn)

                        self.tempBox.add_widget(box)

                        print str(i)
            else:
                pass
            self.oldProfile = self.profile

        for i in self.tempBox.children:
            for j in i.children:
                if isinstance(j, TemperatureLabel):
                    j.update(dt)

    def jog(self, axis, mult):
        self.selected = None
        #print "Jogging", axis
        if 'x' in axis or 'y' in axis:
            step = 0
            for f in ToggleButtonBehavior.get_widgets('xystep'):
                if f.state == 'down':
                    step = float(f.text)
                    break
            #print step*mult
            Server.printer.jog(axis, step*mult)

        if 'z' in axis:
            step = 0
            for f in ToggleButtonBehavior.get_widgets('zstep'):
                if f.state == 'down':
                    step = float(f.text)
                    break
            #print step*mult
            Server.printer.jog(axis, step*mult)

        if 'e' in axis:
            step = 0
            for f in ToggleButtonBehavior.get_widgets('estep'):
                if f.state == 'down':
                    step = float(f.text)
                    break
            #print step*mult
            Server.printer.jog(axis, step*mult)

    def showKeyboard(self, tool, title):
        keypad = TempKeypad()
        keypad.title = title
        keypad.tool = tool
        self.add_widget(keypad)
