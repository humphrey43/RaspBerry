'''
Created on 28.02.2016

@author: hardy
'''
from datetime import datetime
import os
import smbus
import RPi.GPIO as GPIO
import logger

BUTTON1_LED = 27
BUTTON1_SWITCH = 24

ON = True
OFF = False

I2C_BUS = 1
I2C_TSL2561_ADRESS = 0x29
I2C_TCS34725_ADRESS = 0x29

class EnvironmentPi(object):

    def __init__(self):
        self.handler = None        
        GPIO.setwarnings(False)
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(BUTTON1_LED, GPIO.OUT)
        self.set_button1_led(OFF)

        GPIO.setup(BUTTON1_SWITCH, GPIO.IN)
        GPIO.add_event_detect(BUTTON1_SWITCH, GPIO.BOTH, callback=self._handle_button1, bouncetime=500)

        self.i2cBus = smbus.SMBus(I2C_BUS)
#        self.i2cBus.write_byte_data(I2C_TSL2561_ADRESS, 0x80, 0x03)
        self.i2cBus.write_byte(I2C_TCS34725_ADRESS, 0x80|0x00) # 0x00 = ENABLE register
        self.i2cBus.write_byte(I2C_TCS34725_ADRESS, 0x01|0x02) # 0x01 = Power on, 0x02 RGB sensors enabled
        self.i2cBus.write_byte(I2C_TCS34725_ADRESS, 0x80|0x14) # Reading results start register 14, LSB then MSB

    def stop(self):
        GPIO.cleanup() 
    
    def set_handler(self, handler):
        self.handler = handler
        
    def set_volume(self, volume):
        os.system("amixer sset Master " + str(volume) + "%")

    def set_brightness(self, brightness):
        b = int(2.55 * brightness)
        os.system("sudo chmod 666  /sys/class/backlight/rpi_backlight/brightness")
        os.system("echo " + str(b) + " > /sys/class/backlight/rpi_backlight/brightness")

    def set_button1_led(self, on_off):
        GPIO.output(BUTTON1_LED, on_off)

    def _handle_button1(self, channel):
        self.handler.raise_event("Button1", None)

    def get_ambient_light(self):
        data = self.i2cBus.read_i2c_block_data(0x29, 0)
        light = {}
        light['c'] = data[1] << 8 | data[0]
        light['r'] = data[3] << 8 | data[2]
        light['g'] = data[5] << 8 | data[4]
        light['b'] = data[7] << 8 | data[6]
        lux = (-0.32466 * light['r']) + (1.57837 * light['g']) + (-0.73191 * light['b'])
        light['l'] = int(lux) 
        return light

    def log_ambient_light(self, light):
        logger.logvalue("Light", light)

    def get_ambient_light_2(self):
        self.i2cBus.write_byte_data(I2C_TSL2561_ADRESS, 0x80, 0x03)
        ambiente_low_byte = self.i2cBus.read_byte_data(I2C_TSL2561_ADRESS, 0x8c)
        ambiente_high_byte = self.i2cBus.read_byte_data(I2C_TSL2561_ADRESS, 0x8d)
        ambiente = (ambiente_high_byte*256)+ambiente_low_byte
        ir_low_byte = self.i2cBus.read_byte_data(I2C_TSL2561_ADRESS, 0x8e)
        ir_high_byte = self.i2cBus.read_byte_data(I2C_TSL2561_ADRESS, 0x8f)
        ir = (ir_high_byte*256)+ir_low_byte
        if ambiente == 0:
            ambiente = 1
        ratio = ir / float (ambiente)
        lux = 0
        if 0 < ratio <= 0.50:
            lux = 0.0304*ambiente-0.062*ambiente*(ratio**1.4)
        elif 0.50 < ratio <= 0.61:
            lux = 0.0224*ambiente-0.031*ir
        elif 0.61 < ratio <= 0.80:
            lux = 0.0128*ambiente-0.0153*ir
        elif 0.80 < ratio <= 1.3:
            lux = 0.00146*ambiente-0.00112*ir
        else:
            lux = 0
        return lux

    def log_ambient_light_2(self):
        lux = self.get_ambient_light()
        logger.logvalue("Lux", lux)

        