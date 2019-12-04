import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)  # red led
GPIO.setup(23, GPIO.OUT)  # green led

i = 1
while True:
    if (i % 2 == 0):
        GPIO.output(18, True)
        time.sleep(1)
        GPIO.output(18, False)
        time.sleep(1)
    else:
        GPIO.output(23, True)
        time.sleep(1)
        GPIO.output(23, False)
        time.sleep(1)
    i += 1
