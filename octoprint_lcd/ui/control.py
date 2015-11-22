from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ToggleButtonBehavior

import octoprint.server as Server

class ControlTab(FloatLayout):
    def update(self, dt):
        pass

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
