# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

#import octoprint.server as Server

import os
import thread

from . import ui
from . import conf

class LcdPlugin(octoprint.plugin.SettingsPlugin, octoprint.plugin.AssetPlugin, octoprint.plugin.StartupPlugin):

    def on_after_startup(self):
        self._logger.info("Lcd Plugin Starting Up")
        conf.plugin = self
        thread.start_new_thread(ui.start, ())
        self._logger.info("Starting UI")
        some_setting = self._settings.get(["some_setting"])
        some_value = self._settings.get_int(["some_value"])
        some_flag = self._settings.get_boolean(["sub", "some_flag"])
        self._logger.info("some_setting = {some_setting}, some_value = {some_value}, sub.some_flag = {some_flag}".format(**locals()))

    def get_settings_defaults(self):
        return dict(
            some_setting="foo",
            some_value=23,
            sub=dict(
                some_flag=True
            )
        )

    def on_settings_save(self, data):
        old_flag = self._settings.get_boolean(["sub", "some_flag"])

        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

        new_flag = self._settings.get_boolean(["sub", "some_flag"])
        if old_flag != new_flag:
            self._logger.info("sub.some_flag changed from {old_flag} to {new_flag}".format(**locals()))

    def get_assets(self):
		return {
			"js": ["js/slic3r.js"],
			"less": ["less/slic3r.less"],
			"css": ["css/slic3r.css"]
		}

__plugin_name__ = "Lcd Plugin"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = LcdPlugin()
