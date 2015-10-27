import kivy
kivy.require('1.9.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel

from kivy.config import Config

Config.set('graphics', 'height', '480')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'borderless', '1')
Config.write()

class OctoprintLcd(TabbedPanel):
    pass

class OctoprintLcdApp(App):

    def build(self):
        return OctoprintLcd()


if __name__ == '__main__':
    OctoprintLcdApp().run()
