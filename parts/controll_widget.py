# -*- coding: utf-8 -*-
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget


import os
import csv
import numpy as np
import pandas as pd
import utils.MotiveControll as motive
from datetime import datetime


class ControlWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(ControlWidget, self).__init__(**kwargs)
        # /*-----------------------------------------------
        #    Initialize Sound Player
        # ------------------------------------------------*/
        self.sound = SoundLoader.load('../Data/etc/warning.mp3')

        # /*-----------------------------------------------
        #    Param
        # ------------------------------------------------*/
        self.baseDir = './Data/Ex1/Subject1/T1'
        self.columns = ['start', 'notice', 'end']
        self.times   = []

    def buttonStart(self):

        # /*-----------------------------------------------
        #    接続の確認
        # ------------------------------------------------*/
        try:
            motive.turn_off()
        except:
            print("[INFO  ] Don't connect COM3 with your PC ")

        a=self.input1.text
        b=self.input2.text
        c=self.input3.text
        d=self.input4.text
        filename=os.path.join(self.baseDir,a+'_'+b+'_'+c+'_'+d+ '.csv')
        date1= datetime.now()#.strftime('%H時%M分%S秒')
        self.times.append(date1)

    def buttonNotice(self):
        a=self.input1.text
        b=self.input2.text
        c=self.input3.text
        d=self.input4.text
        filename=a+'_'+ b +'_'+c+'_'+d+ '.csv'
        date2= datetime.now()#.strftime('%H時%M分%S秒')
        self.times.append(date2)
        # with open(filename, 'a') as f:
        #     writer = csv.writer(f)
        #     writer.writerow(body2)

    def buttonFinish(self):

        # /*-----------------------------------------------
        #    接続の確認
        # ------------------------------------------------*/
        try:
            # motive.turn_off()
            motive.turn_on()
        except:
            print("[INFO  ] Don't connect COM3 with your PC ")

        a=self.input1.text
        b=self.input2.text
        c=self.input3.text
        d=self.input4.text
        filename=a+'_'+ b +'_'+c+'_'+d+ '.csv'
        date3= datetime.now()#.strftime('%H時%M分%S秒')
        self.times.append(date3)
        df = pd.DataFrame(np.array(self.times), columns=self.columns)
        df.to_csv(os.path.join(self.baseDir,filename))
        
      
          #finish処理

    def slideCallback(self, instance, value):
        # Slider横のLabelをSliderの値に
        self.s1Label.text = 'Slider %s' % int(value)

    def buttonCallback(self, instance):
        # 何かのフラグに使える
        self.sound.play()
