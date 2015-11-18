def start():
    import kivy
    kivy.require('1.9.0') # replace with your current kivy version !

    from kivy.app import App
    from kivy.lang import Builder
    from kivy.clock import Clock
    from kivy.properties import StringProperty
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.tabbedpanel import TabbedPanel

    from kivy.config import Config

    import octoprint.server as Server

    from .status import StatusTab

    Config.set('graphics', 'height', '480')
    Config.set('graphics', 'width', '800')
    Config.set('graphics', 'borderless', '1')
    Config.write()

    class FileView(BoxLayout):

        name = StringProperty("[NAME]")
        uploaded = StringProperty("[UPLOADED]")
        size = StringProperty("[SIZE]")

        def __init__(self, destination, path):
            self.destination = destination
            self.path = path
            self.info = Server.fileManager.get_metadata(self.destination, self.path)

            print info

            self.add_widget(Label(text="HELOSDS"))

        def update(self):
            self.info = Server.fileManager.get_metadata(self.destination, self.path)

    class OctoprintLcd(TabbedPanel):

        def __init__(self):
            super(OctoprintLcd, self).__init__()
            Clock.schedule_interval(self.update, .1)


        def update(self, dt):
            pass
            self.ids.status_tab.update(dt)

    class OctoprintLcdApp(App):

        def build(self):
            return OctoprintLcd()


    OctoprintLcdApp.run(OctoprintLcdApp())
