# -*- coding: utf-8 -*-
import japanize_kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from parts.depth_preview import DepthPreview
from parts.controll_widget import ControlWidget

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

class LabApp(App):
    def build(self,):
        return MainScreen()

if __name__ == '__main__':
    Builder.load_file('./view/main.kv')
    Builder.load_file('./view/depth_preview.kv')
    Builder.load_file('./view/controll_widget.kv')
    LabApp().run()