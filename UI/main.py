from kivy.config import Config
Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '480')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label

from kivy.properties import StringProperty

from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path

from random import randint

# デフォルトに使用するフォントを変更する
resource_add_path('C:\Windows\Fonts')
LabelBase.register(DEFAULT_FONT, 'HGRPP1.TTC') #日本語が使用できるように日本語フォントを指定する

class UIWidget(Widget):

    def __init__(self, **kwargs):
        super(UIWidget, self).__init__(**kwargs)
        pass

    def buttonStart(self):
        pass   #start処理

    def buttonNotice(self):
        pass   #notice処理

    def buttonFinish(self):
        pass   #finish処理

class UIApp(App):
    def __init__(self, **kwargs):
        super(UIApp, self).__init__(**kwargs)
        self.title = '音声生成'

if __name__ == '__main__':
    UIApp().run()