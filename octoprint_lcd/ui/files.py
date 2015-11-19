from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

import octoprint.server as Server

class FilesTab(BoxLayout):
    file_list=ObjectProperty(None)

    first = True

    def __init__(self, **kwargs):
        super(FilesTab, self).__init__(**kwargs)

    def update(self, dt):
        if self.first:
            # files = GridLayout(cols=1, spacing=10, size_hint_y=None)
            # # Make sure the height is such that there is something to scroll.
            # files.bind(minimum_height=files.setter('height'))
            # for i in range(30):
            #     btn = Button(text=str(i), size_hint_y=None, height=40)
            #     files.add_widget(btn)
            # scroll = ScrollView(size_hint=(None, None), size=(400, 400))
            # scroll.add_widget(files)
            # self.ids.file_list.add_widget(scroll)
            self.ids.file_list.bind(minimum_height=self.ids.file_list.setter('height'))
            for i in range(30):
                btn = Button(text=str(i), size_hint_y=None, height=40)
                self.ids.file_list.add_widget(btn)
            self.first = False
