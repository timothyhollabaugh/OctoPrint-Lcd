from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout

import time

import octoprint.server as Server
from octoprint.settings import settings
from octoprint.printer import get_connection_options

#import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(2, GPIO.OUT)
#GPIO.setup(3, GPIO.OUT)

class PrinterTab(BoxLayout):

    first = True

    connection = ()
    oldConnection = ()

    def update(self, dt):
        connections = get_connection_options()

        self.ids.ports.values = connections['ports']
        self.ids.baudrates.values = map(str, connections['baudrates'])
        profiles = []
        for i in Server.printerProfileManager.get_all():
            profiles.append(Server.printerProfileManager.get_all()[i]['name'])
        self.ids.profiles.values = profiles

        if self.first:
            self.ids.ports.text = connections['portPreference']
            self.ids.baudrates.text = str(connections['baudratePreference'])
            self.ids.profiles.text = Server.printerProfileManager.get_all()['_default']['name']
            self.first = False

        self.connection = Server.printer.get_current_connection()

        if self.connection != self.oldConnection:
            #print self.connection

            if self.connection[0] != 'Closed':
                self.ids.ports.disabled = True
                self.ids.baudrates.disabled = True
                self.ids.profiles.disabled = True
                self.ids.connect.text = "Disconnect"
                self.ids.connect.on_press = Server.printer.disconnect

                self.ids.ports.text = self.connection[1]
                self.ids.baudrates.text = str(self.connection[2])
                self.ids.profiles.text = self.connection[3]['name']
            else:
                self.ids.ports.disabled = False
                self.ids.baudrates.disabled = False
                self.ids.profiles.disabled = False
                self.ids.connect.text = "Connect"
                self.ids.connect.on_press = lambda: Server.printer.connect(self.ids.ports.text, self.ids.baudrates.text, self.ids.profiles.text)

            self.oldConnection = self.connection

    def power(self, state):
        print "setting power to " + str(state)
        #GPIO.output(2, state)

    def outlet(self, state):
        print "setting outlet to " + str(state)
        #GPIO.output(3, state)
