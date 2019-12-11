# source: https://learn.adafruit.com/adafruit-tsl2591/python-circuitpython
import board  # circuit python stuff
import busio  # circuit python stuff
import adafruit_tsl2591  # sensor library
from time import sleep

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_tsl2591.TSL2591(i2c)

while True:
    sleep(1)
    print('Light: {0}lux'.format(sensor.lux))
    print('Visible: {0}'.format(sensor.visible))
    print('Infrared: {0}'.format(sensor.infrared))