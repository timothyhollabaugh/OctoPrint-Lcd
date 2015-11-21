def start():
    import kivy
    kivy.require('1.9.0') # replace with your current kivy version !

    from kivy.app import App
    from kivy.lang import Builder
    from kivy.clock import Clock
    from kivy.properties import StringProperty
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.tabbedpanel import TabbedPanel
    from kivy.uix.floatlayout import FloatLayout

    from kivy.config import Config

    import octoprint.server as Server

    from .status import StatusTab
    from .files import FilesTab
    from .printer import PrinterTab

    Config.set('graphics', 'height', '480')
    Config.set('graphics', 'width', '800')
    Config.set('graphics', 'borderless', '1')
    Config.write()

    class OctoprintLcd(FloatLayout):

        def __init__(self):
            super(OctoprintLcd, self).__init__()
            Clock.schedule_interval(self.update, .1)


        def update(self, dt):
            pass
            self.ids.status_tab.update(dt)
            self.ids.status_box.update(dt)
            self.ids.printer_tab.update(dt)
            self.ids.files_tab.update(dt)

    class OctoprintLcdApp(App):

        def build(self):
            return OctoprintLcd()


    OctoprintLcdApp.run(OctoprintLcdApp())
