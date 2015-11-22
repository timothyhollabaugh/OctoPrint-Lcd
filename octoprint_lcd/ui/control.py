from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.properties import ObjectProperty

import octoprint.server as Server

class TempKeypad(BoxLayout):

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
    def update(self, dt):
        temps = Server.printer.get_current_temperatures()

        if Server.printer.get_current_connection()[3] != None:
            if Server.printer.get_current_connection()[3]['heatedBed']:
                if 'bed' in temps.keys():
                    self.ids.bed_status.actual = str("%3.1f" % temps['bed']['actual']) if temps['bed']['actual'] > 1 else "--"
                    self.ids.bed_status.target = str("%3.0f" % temps['bed']['target']) if temps['bed']['actual'] > 1 else "--"
            if 'tool0' in temps.keys():
                self.ids.tool0_status.actual = str("%3.1f" % temps['tool0']['actual']) if temps['tool0']['actual'] > 1 else "--"
                self.ids.tool0_status.target = str("%3.0f" % temps['tool0']['target']) if temps['tool0']['actual'] > 1 else "--"
            if 'tool1' in temps.keys():
                self.ids.tool1_status.actual = str("%3.1f" % temps['tool1']['actual']) if temps['tool1']['actual'] > 1 else "--"
                self.ids.tool1_status.target = str("%3.0f" % temps['tool1']['target']) if temps['tool1']['actual'] > 1 else "--"
            if 'tool2' in temps.keys():
                self.ids.tool2_status.actual = str("%3.1f" % temps['tool2']['actual']) if temps['tool2']['actual'] > 1 else "--"
                self.ids.tool2_status.target = str("%3.0f" % temps['tool2']['target']) if temps['tool2']['actual'] > 1 else "--"

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
