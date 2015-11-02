def start():
    import kivy
    kivy.require('1.9.0') # replace with your current kivy version !

    from kivy.app import App
    from kivy.lang import Builder
    from kivy.clock import Clock
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.tabbedpanel import TabbedPanel

    from kivy.config import Config

    from . import Data

    Config.set('graphics', 'height', '480')
    Config.set('graphics', 'width', '800')
    Config.set('graphics', 'borderless', '1')
    Config.write()

    class OctoprintLcd(TabbedPanel):

        def __init__(self):
            super(OctoprintLcd, self).__init__()
            Clock.schedule_interval(self.update, .5)


        def update(self, dt):
            self.ids.status_label.text = Data.getCurrentData()['state']['text']

            if Data.getCurrentData()['state']['flags']['printing'] :
                self.ids.print_button.text = "Print"
                self.ids.pause_button.text = "Pause"

                self.ids.print_button.disabled = True
                self.ids.pause_button.disabled = False
                self.ids.cancel_button.disabled = False
            elif Data.getCurrentData()['state']['flags']['paused']:
                self.ids.print_button.text = "Restart"
                self.ids.pause_button.text = "Resume"

                self.ids.print_button.disabled = False
                self.ids.pause_button.disabled = False
                self.ids.cancel_button.disabled = False
            else:
                self.ids.print_button.text = "Print"
                self.ids.pause_button.text = "Pause"

                if Data.getCurrentData()['job']['file']['name'] == None:
                    self.ids.print_button.disabled = True
                else:
                    self.ids.print_button.disabled = False

                self.ids.pause_button.disabled = True
                self.ids.cancel_button.disabled = True

            file = Data.getCurrentData()['job']['file']['name']
            if file == None:
                file = ""
            self.ids.file_label.text = file

            timein = Data.getCurrentData()['progress']['printTime']

            if not timein == None:
                m, s = divmod(int(timein), 60)
                h, m = divmod(m, 60)
            else:
                h, m, s = 0, 0, 0

            self.ids.time_in.time = str("%02d:%02d:%02d" % (h, m, s))

            timeleft = Data.getCurrentData()['progress']['printTimeLeft']

            if not timeleft == None:
                m, s = divmod(int(timeleft), 60)
                h, m = divmod(m, 60)
            else:
                h, m, s = 0, 0, 0

            self.ids.time_remaining.time = str("%02d:%02d:%02d" % (h, m, s))

            timetotal = Data.getCurrentData()['job']['estimatedPrintTime']

            if not timetotal == None:
                m, s = divmod(int(timetotal), 60)
                h, m = divmod(m, 60)
            else:
                h, m, s = 0, 0, 0

            self.ids.time_total.time = str("%02d:%02d:%02d" % (h, m, s))

            prog = Data.getCurrentData()['progress']['completion']

            if prog == None:
                prog = 0

            self.ids.progress.value = prog

    class OctoprintLcdApp(App):

        def build(self):
            return OctoprintLcd()



    #Builder.load_file('octoprintlcd.kv')

    OctoprintLcdApp.run(OctoprintLcdApp())
