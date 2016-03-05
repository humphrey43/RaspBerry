'''
Created on 22.12.2015

@author: hardy
'''
from datetime import datetime

import kivy
import sys
from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


kivy.require('1.0.7')


#from kivy.animation import Animation

class Source:
    
    def __init__(self, name, address):
        self.name = name
        self.address = address
        
        
class Player:
    
    def __init__(self):
        self.playing = False
        self.sound = None
        
    def play(self, source):
        
        if self.sound != None:
            self.sound.stop()
            self.sound = None
            self.playing = False
        
        self.name = source.name
        self.address = source.address
        self.sound = SoundLoader.load(self.address)
        self.sound.play()
        self.playing = True
            
    def off(self):
        if self.sound != None:
            self.sound.stop()
            self.playing = False
            self.sound = None

class AlarmType:
    def __init__(self):
        self.isSpecial = False
        self.day = Alarm.DAYS_ALL
        self.hour = 0
        self.minute = 0
        self.alarmtype = "STANDARD"

class Alarm:
    
    DAYS_ALL = "MO-SO"
    DAYS_WEEK = "MO-FR"
    DAYS_WEEKEND = "SA-SO"
    DAYS_NONE = "NONE"
    DAY_MONDAY = "MO"
    DAY_TUESDAY = "DI"
    DAY_WEDNESYDAY = "MI"
    DAY_THURSDAY = "DO"
    DAY_FRIDAY = "FR"
    DAY_SATURDAY = "SA"
    DAY_SUNDAY = "SO"
    
    def __init__(self):
        self.isSpecial = False
        self.day = Alarm.DAYS_ALL
        self.hour = 0
        self.minute = 0
        self.alarmtype = "STANDARD"
                

class RadioClock(App):
    i = 42
    label = None
    sound = None
    on = False
#    musicSource = "C:\Users\hardy\Music\iTunes\iTunes Media\Music\"
    musicSource = "/home/pi/Music/"
    ndr2 = Source("NDR2","http://ndr-ndr2-nds-mp3.akacast.akamaistream.net/7/400/252763/v1/gnl.akacast.akamaistream.net/ndr_ndr2_nds_mp3.mp3")
    player = None
    jimi = Source("Jimi Hendrix",musicSource + "Jimi Hendrix Experience/The Ultimate Experience/03 Hey Joe.mp3")

    alarmedToday = False
    alarmTime = datetime(2016, 2, 8, 4, 58)
    
    alarmtypes = {}
    alarms = {}
    
#    Window.fullscreen = True
    def animate(self, dt):
        s = datetime.now().isoformat()[11:19]
        self.label.text = s
        if self.checkAlarmTime():
            self.ringAlarm()
#        self.label.refresh()


    def ringAlarm(self): 
        if self.player == None:
            self.player = Player()
        self.player.play(self.ndr2)

    def setTime(self,instance): 
        self.i += 1
        s = datetime.now().isoformat()[11:19]
        self.label.text = s
        self.label.padding = '10dp'
        self.label.size = self.label.texture_size

    def play(self,instance): 
        if self.player == None:
            self.player = Player()
            self.player.play(self.ndr2)
        elif self.player.name == "NDR2":
            self.player.play(self.jimi)
##       elif self.player.name == "Jimi Hendrix":
##            self.player.off()
##            self.player.name = ""
        else:
            sys.exit(0)
##            self.player.play(self.ndr2)
        
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.label = Label(font_size='128dp')
        s = datetime.now().isoformat()[11:19]
        self.label.text = s
        self.label.padding = (10,10)
        self.label.size = self.label.texture_size
        layout.add_widget(self.label)
        button = Button(size_hint=(.5, .5), text='plop',
                        pos_hint={'x':0.3},on_press=self.play)
        layout.add_widget(button)
        button.pos_hint_x=0.3
        Clock.schedule_interval(self.animate,1/5)
        return layout

    def checkAlarmTime(self):
        self.checkNewDay()
        if not self.alarmedToday and self.alarmTime <= datetime.now():
            self.alarmedToday = True
            return True
        return False
            
    def checkNewDay(self):
        s = datetime.now().isoformat()[11:16]
        if s == "00:00":
            self.alarmedToday = False
            
if __name__ == '__main__':
        RadioClock().run()

