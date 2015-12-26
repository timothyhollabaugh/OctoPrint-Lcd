from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout

import time
import os

import octoprint.server as Server
from octoprint.printer import get_connection_options

from .. import conf

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
        for i in conf.plugin._printer_profile_manager.get_all():
            profiles.append(conf.plugin._printer_profile_manager.get_all()[i]['name'])
        self.ids.profiles.values = profiles

        if self.first:
            self.ids.ports.text = connections['portPreference']
            self.ids.baudrates.text = str(connections['baudratePreference'])
            self.ids.profiles.text = conf.plugin._printer_profile_manager.get_all()['_default']['name']
            self.first = False

        self.connection = conf.plugin._printer.get_current_connection()

        if self.connection != self.oldConnection:

            if self.connection[0] != 'Closed':
                self.ids.ports.disabled = True
                self.ids.baudrates.disabled = True
                self.ids.profiles.disabled = True
                self.ids.connect.text = "Disconnect"
                self.ids.connect.on_press = conf.plugin._printer.disconnect

                self.ids.ports.text = self.connection[1]
                self.ids.baudrates.text = str(self.connection[2])
                self.ids.profiles.text = self.connection[3]['name']
            else:
                self.ids.ports.disabled = False
                self.ids.baudrates.disabled = False
                self.ids.profiles.disabled = False
                self.ids.connect.text = "Connect"
                self.ids.connect.on_press = lambda: conf.plugin._printer.connect(self.ids.ports.text, self.ids.baudrates.text, self.ids.profiles.text)

            self.oldConnection = self.connection

    def power(self, state):
        conf.plugin._logger.info("setting power to " + str(state))
        #GPIO.output(2, state)

    def outlet(self, state):
        conf.plugin._logger.info("setting outlet to " + str(state))
        #GPIO.output(3, state)

    def shutdown(self):
        conf.plugin._logger.info()"Shuting Down")
        os.system("sudo shutdown -h now");
