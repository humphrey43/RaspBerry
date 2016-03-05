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

kivy.require('1.0.7')


class RadioClock(App):
    
    def __init__(self):
        super(RadioClock, self).__init__()
        
        self.tb = swbus.master.register_component(TimeBase())
        self.p = swbus.master.register_component(Player())
        self.env = swbus.master.register_component(Environment())
        self.clockWork = swbus.master.register_component(ClockWork(self))
        self.clockFace = swbus.master.register_component(ClockFace())

        swbus.connect_components(
            '''
            TimeBase.Second -> ClockFace.Time
        
        # dies ist ein Kommentar
            Environment.Button1LED -> ClockWork.LED 
            Environment.Button1    -> ClockWork.Trigger
            ClockWork.Play         -> Player.Play
            ClockWork.Off          -> Player.Off
            
            ClockFace.Stop ->  ClockWork.Halt
            Environment.Volume -> ClockFace.Volume
            Environment.Brightness -> ClockFace.Brightness
            
            ''')
        
        
        i = 42

    def system_halt(self):
        swbus.master.bus_stop()
        App.stop(self)

    def build(self):
        root = self.clockFace.build()
        swbus.master.read_configurations(self.config)
        return root

    def build_config(self, config):
        config.add_section("Test")
        
if __name__ == '__main__':
        RadioClock().run()

