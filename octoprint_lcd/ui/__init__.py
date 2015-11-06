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
            temps = Server.printer.get_current_temperatures()

            if Server.printer.get_current_connection()[3] != None:
                if Server.printer.get_current_connection()[3]['heatedBed']:
                    if 'bed' in temps.keys():
                        self.ids.bed_status.actual = str("%3.1f" % temps['bed']['actual'])
                        self.ids.bed_status.target = str("%3.0f" % temps['bed']['target'])
                if 'tool0' in temps.keys():
                    self.ids.tool0_status.actual = str("%3.1f" % temps['tool0']['actual'])
                    self.ids.tool0_status.target = str("%3.0f" % temps['tool0']['target'])
                if 'tool1' in temps.keys():
                    self.ids.tool1_status.actual = str("%3.1f" % temps['tool1']['actual'])
                    self.ids.tool1_status.target = str("%3.0f" % temps['tool1']['target'])
                if 'tool2' in temps.keys():
                    self.ids.tool2_status.actual = str("%3.1f" % temps['tool2']['actual'])
                    self.ids.tool2_status.target = str("%3.0f" % temps['tool2']['target'])


            data = Server.printer.get_current_data()

            filament = data['job']['filament']

            changed = []

            if filament != None:
                if 'tool0' in filament.keys() or 'tool1' in filament.keys() or 'tool2' in filament.keys():
                    for i in filament:
                        #print i
                        self.ids[i + '_filament'].length = str("%.2f" % (filament[i]['length']/1000))
                        self.ids[i + '_filament'].volume = str("%3.2f" % filament[i]['volume'])
                        changed.append(i)

            if not 'tool0' in changed:
                self.ids['tool0_filament'].length = " - - "
                self.ids['tool0_filament'].volume = " - - "
            if not 'tool1' in changed:
                self.ids['tool1_filament'].length = " - - "
                self.ids['tool1_filament'].volume = " - - "
            if not 'tool2' in changed:
                self.ids['tool2_filament'].length = " - - "
                self.ids['tool2_filament'].volume = " - - "

            self.ids.status_label.text = data['state']['text']

            if data['state']['flags']['printing'] :
                self.ids.print_button.text = "Print"
                self.ids.pause_button.text = "Pause"

                self.ids.print_button.disabled = True
                self.ids.pause_button.disabled = False
                self.ids.cancel_button.disabled = False
            elif data['state']['flags']['paused']:
                self.ids.print_button.text = "Restart"
                self.ids.pause_button.text = "Resume"

                self.ids.print_button.disabled = False
                self.ids.pause_button.disabled = False
                self.ids.cancel_button.disabled = False
            else:
                self.ids.print_button.text = "Print"
                self.ids.pause_button.text = "Pause"

                if data['job']['file']['name'] == None:
                    self.ids.print_button.disabled = True
                else:
                    self.ids.print_button.disabled = False

                self.ids.pause_button.disabled = True
                self.ids.cancel_button.disabled = True

            file = data['job']['file']['name']
            if file == None:
                file = "No File Loaded"
            self.ids.file_label.text = file

            timein = data['progress']['printTime']

            if not timein == None:
                m, s = divmod(int(timein), 60)
                h, m = divmod(m, 60)
            else:
                h, m, s = 0, 0, 0

            self.ids.time_in.time = str("%02d:%02d:%02d" % (h, m, s))

            timeleft = data['progress']['printTimeLeft']

            if not timeleft == None:
                m, s = divmod(int(timeleft), 60)
                h, m = divmod(m, 60)
            else:
                h, m, s = 0, 0, 0

            self.ids.time_remaining.time = str("%02d:%02d:%02d" % (h, m, s))

            timetotal = data['job']['lastPrintTime']

            if timetotal == None:
                timetotal = data['job']['estimatedPrintTime']

            if not timetotal == None:
                m, s = divmod(int(timetotal), 60)
                h, m = divmod(m, 60)
            else:
                h, m, s = 0, 0, 0

            self.ids.time_total.time = str("%02d:%02d:%02d" % (h, m, s))

            prog = data['progress']['completion']

            if prog == None:
                prog = 0

            self.ids.progress.value = prog

    class OctoprintLcdApp(App):

        def build(self):
            return OctoprintLcd()


    OctoprintLcdApp.run(OctoprintLcdApp())
