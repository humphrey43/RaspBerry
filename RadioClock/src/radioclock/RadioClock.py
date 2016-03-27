'''
Created on 22.12.2015

@author: hardy
'''
import kivy
from kivy.app import App

import swbus
from timebase import TimeBase
from player import Player
from clockwork import ClockWork
from clockface import ClockFace
from environment import Environment
from alarmclock import AlarmClock
from jukebox import JukeBox
import logger

kivy.require('1.0.7')


class RadioClock(App):
    
    def __init__(self):
        super(RadioClock, self).__init__()
        
        logger.logfile = "radioclock.log"
        logger.console = True
        logger.log("Start")
        
        self.jukeBox = swbus.master.register_component(JukeBox())
        self.tb = swbus.master.register_component(TimeBase())
        self.p = swbus.master.register_component(Player())
        self.env = swbus.master.register_component(Environment())
        self.clockWork = swbus.master.register_component(ClockWork(self))
        self.clockFace = swbus.master.register_component(ClockFace())
        self.alarmClock = swbus.master.register_component(AlarmClock())

        swbus.connect_components(
            '''
            TimeBase.Second -> ClockFace.Time
            TimeBase.Minute -> Environment.Time
            TimeBase.Minute -> AlarmClock.Time
        
        # dies ist ein Kommentar
            Environment.Button1LED -> ClockWork.LED 
            Environment.Button1    -> ClockWork.Trigger
            Environment.AmbientLight  -> ClockFace.AmbientLight
            ClockWork.Play         -> Player.Play
            ClockWork.Off          -> Player.Off
            ClockWork.Enable       -> ClockFace.Enable
            
            ClockFace.Stop ->  ClockWork.Halt
            ClockFace.Clean ->  ClockWork.Disabled
            ClockFace.Volume -> Environment.Volume
            ClockFace.Brightness -> Environment.Brightness

            AlarmClock.Alarm -> ClockWork.Alarm
            AlarmClock.AlarmTime -> ClockWork.AlarmTime
            AlarmClock.AlarmInfo -> ClockWork.AlarmInfo
            ClockFace.AlarmTime -> ClockWork.AlarmTimeDisplay
            ClockFace.AlarmInfo -> ClockWork.AlarmInfoDisplay
            ClockFace.Clean -> ClockWork.Disabled
            ClockFace.Click -> ClockWork.Trigger

            JukeBox.SourceName -> ClockWork.SourceName
            JukeBox.Source -> ClockWork.Source

            ''')
        
        
        i = 42

    def system_halt(self):
        swbus.master.bus_stop()
        logger.log("Halt")
        App.stop(self)

    def build(self):
        self.clockFace.read_configuration1(self.config)
        root = self.clockFace.build()
        swbus.master.read_configurations(self.config)
        return root

    def build_config(self, config):
        config.add_section("Test")
        
if __name__ == '__main__':
        RadioClock().run()

