#!/usr/bin/python
#left to do:
#1. get extension wires to locate temp sensor away from fan (to reduce reaction time)
#2. replace BMP sensor with BME sensor. This should work with this script without modification

import sys
import RPi.GPIO as GPIO
import I2C_LCD_driver

from Adafruit_BME280 import *
from time import sleep, strftime, time
import time

sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)


mylcd = I2C_LCD_driver.lcd()

GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)

mylcd.lcd_display_string("    STARTING    ", 1)
mylcd.lcd_display_string("    PROGRAM     ", 2)

def measure():
	with open("autochicklog.csv", "a") as log:
        	degrees = sensor.read_temperature()
		degreesF = degrees * 1.8 + 32
		roundtemp = round(degreesF,1)
        	pascals = sensor.read_pressure()
        	hectopascals = pascals / 100
        	humidity = sensor.read_humidity()

		DATE = strftime("%Y-%m-%d_%H:%M:%S")
	        log.write("{0},{1},{2},{3}\n".format(strftime(DATE),degreesF, hectopascals, humidity))

        	print 'T = {0:0.3f} F'.format(degreesF)
        	print 'P = {0:0.2f} hPa'.format(hectopascals)
        	print 'Humidity  = {0:0.2f} %'.format(humidity)
		#check to see if it's too hot. If so, turn on fan. 33C = 91.4F
		if roundtemp > 75:
                        #mylcd.lcd_display_string(str(degrees*1.8+32) + "F, " + str(humidity) + "%hum", 1)
			mylcd.lcd_display_string(str(roundtemp) + "F, " + str(humidity) + "%hum", 1)
			mylcd.lcd_display_string("Fan On          ", 2)
			GPIO.output(13, True)
			time.sleep( 1 )
                        mylcd.lcd_display_string("Fan On .        ", 2)
			time.sleep( 1)
                        mylcd.lcd_display_string("Fan On . .      ", 2)
                        time.sleep( 1)
                        mylcd.lcd_display_string("Fan On . . .    ", 2)
                        time.sleep( 1)
                        mylcd.lcd_display_string("Fan On . . . .  ", 2)
                        time.sleep( 1)
                        mylcd.lcd_display_string("Fan On . . . . .", 2)
                        time.sleep( 1)

		#check to see if it's too cold. If so, turn off fan. 31C = 87.8F
		elif roundtemp < 73:
			print("too cold!")
        	        mylcd.lcd_display_string(str(roundtemp) + "F, " + str(humidity) + "%hum", 1)
                        GPIO.output(13, False)
        	        mylcd.lcd_display_string("TOO COLD!!!!    ", 2)
                        time.sleep( 1)
                        mylcd.lcd_display_string("                ", 2)
                        time.sleep( 1)
                        mylcd.lcd_display_string("TOO COLD!!!!    ", 2)
                        time.sleep( 1)
                        mylcd.lcd_display_string("                ", 2)
                        time.sleep( 1)
                        mylcd.lcd_display_string("TOO COLD!!!!    ", 2)
                        time.sleep( 1)
		else:
			print("Temp Good.")
                        GPIO.output(13, False)
        	        mylcd.lcd_display_string(str(roundtemp) + "F, " + str(humidity) + "%hum", 1)
        	        mylcd.lcd_display_string("Temp Good.      ", 2)
                        time.sleep( 1)
                        mylcd.lcd_display_string("Temp Good..     ", 2)
                        time.sleep( 1)
                        mylcd.lcd_display_string("Temp Good...    ", 2)
                        time.sleep( 1)
                        mylcd.lcd_display_string("Temp Good....   ", 2)
                        time.sleep( 1)
                        mylcd.lcd_display_string("Temp Good.....  ", 2)
                        time.sleep( 1)

while True:
	measure()
