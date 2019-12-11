import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)  # red led
GPIO.setup(25, GPIO.OUT)  # green led
GPIO.setup(12, GPIO.OUT)  # yellow led

while True:
    print(str(i%3))
    if (i % 3 == 0):
        print('red on')
        GPIO.output(18, True)
        time.sleep(1)
        GPIO.output(18, False)
        time.sleep(1)
    elif(i % 3 == 1):
        print('green on')
        GPIO.output(25, True)
        time.sleep(1)
        GPIO.output(25, False)
        time.sleep(1)
    else:
        print('yellow on')
        GPIO.output(12, True)
        time.sleep(1)
        GPIO.output(12, False)
        time.sleep(1)
    i += 1