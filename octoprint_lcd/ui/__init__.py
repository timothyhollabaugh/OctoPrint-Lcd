
def start():
    import os
    os.environ["KIVY_NO_ARGS"] = "1"
    os.environ["KIVY_NO_CONSOLELOG"] = "1"

    import kivy
    kivy.require('1.9.0') # replace with your current kivy version !

    from kivy.app import App
    from kivy.clock import Clock
    from kivy.properties import StringProperty
    from kivy.properties import ObjectProperty
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.tabbedpanel import TabbedPanel
    from kivy.uix.floatlayout import FloatLayout
    from kivy.uix.tabbedpanel import TabbedPanelItem

    from kivy.config import Config

    import octoprint.server as Server

    import threading

    from .status import StatusTab
    from .control import ControlTab
    from .files import FilesTab
    from .printer import PrinterTab
    from .usb import UsbTab
    from .usb import start_listening
    from .. import conf

    Config.set('graphics', 'height', '480')
    Config.set('graphics', 'width', '800')
    Config.set('graphics', 'borderless', '1')
    Config.write()

    class OctoprintLcd(FloatLayout):

        conf  = ObjectProperty(None)

        def __init__(self):
            super(OctoprintLcd, self).__init__()

            self.conf = conf

            Clock.schedule_interval(self.update, .1)

            # Start the usb listener
            thread=threading.Thread(target=start_listening, args=(self,))
            thread.daemon=True              # This makes sure that CTRL+C works
            thread.start()

        def update(self, dt):
            self.conf = conf
            self.ids.status_tab.update(dt)
            self.ids.status_box.update(dt)
            self.ids.control_tab.update(dt)
            self.ids.printer_tab.update(dt)
            self.ids.files_tab.update(dt)

        def addUsb(self, usb):
            usb.text = "USB"
            self.ids.tabbedpanel.add_widget(usb)

        def removeUsb(self, usb):
            self.ids.tabbedpanel.remove_widget(usb)

        def switchDefault(self):
            self.ids.tabbedpanel.switch_to(self.ids.tabbedpanel.default_tab)

    class OctoprintLcdApp(App):

        def build(self):
            return OctoprintLcd()


    OctoprintLcdApp.run(OctoprintLcdApp())
