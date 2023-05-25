from kivy.config import Config
Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '480')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader

from kivy.properties import StringProperty

from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path

from random import randint

import csv
import datetime


sound=SoundLoader.load("警告音1.mp3")

# デフォルトに使用するフォントを変更する
resource_add_path('C:\Windows\Fonts')
LabelBase.register(DEFAULT_FONT, 'HGRPP1.TTC') #日本語が使用できるように日本語フォントを指定する

class UIWidget(Widget):

    def __init__(self, **kwargs):
        super(UIWidget, self).__init__(**kwargs)
        pass

    def buttonStart(self):
        a=self.input1.text
        b=self.input2.text
        c=self.input3.text
        d=self.input4.text
        filename=a+'_'+ b +'_'+c+'_'+d+ '.csv'
        date1= datetime.datetime.now().strftime('%H時%M分%S秒')
        body=[date1]
        with open(filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerows([body])  #start処理

    def buttonNotice(self):
        a=self.input1.text
        b=self.input2.text
        c=self.input3.text
        d=self.input4.text
        filename=a+'_'+ b +'_'+c+'_'+d+ '.csv'
        date2= datetime.datetime.now().strftime('%H時%M分%S秒')
        body2=[date2]
        with open(filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(body2)
        sound.play()   #notice処理

    def buttonFinish(self):
        a=self.input1.text
        b=self.input2.text
        c=self.input3.text
        d=self.input4.text
        filename=a+'_'+ b +'_'+c+'_'+d+ '.csv'
        date3= datetime.datetime.now().strftime('%H時%M分%S秒')
        body3=[date3]
        with open(filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(body3)

        with open(filename) as f:
            print(f.read())
      
          #finish処理

class UIApp(App):
    def __init__(self, **kwargs):
        super(UIApp, self).__init__(**kwargs)
        self.title = '音声生成'

if __name__ == '__main__':
    UIApp().run()