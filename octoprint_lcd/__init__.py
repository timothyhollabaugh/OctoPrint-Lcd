# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

import octoprint.server as Server

import thread

from .internal import OctoprintUpdate
from .ui import *

class LcdPlugin(octoprint.plugin.StartupPlugin):

    def on_after_startup(self):
        Server.printer.register_callback(OctoprintUpdate())
        thread.start_new_thread(ui.start, ())
        self._logger.info("Starting UI")

#    def on_after_startup(self):
#        self._logger.info("Activating UI")

__plugin_name__ = "Lcd Plugin"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = LcdPlugin()
