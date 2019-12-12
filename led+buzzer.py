import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)  # red led
GPIO.setup(25, GPIO.OUT)  # green led
GPIO.setup(23, GPIO.OUT)  # blue led
GPIO.setup(24, GPIO.OUT)  # buzzer
GPIO.setup(12, GPIO.OUT)  # yellow led



i = 1
while True:
    print(str(i%5))
    if (i % 5 == 0):
        print('red on')
        GPIO.output(18, True)
        time.sleep(1)
        GPIO.output(18, False)
        time.sleep(1)
    elif(i % 5 == 1):
        print('green on')
        GPIO.output(25, True)
        time.sleep(1)
        GPIO.output(25, False)
        time.sleep(1)
    elif(i % 5 == 2):
        print('yellow on')
        GPIO.output(12, True)
        time.sleep(1)
        GPIO.output(12, False)
        time.sleep(1)
    elif(i % 5 == 3):
        print('blue on')
        GPIO.output(23, True)
        time.sleep(1)
        GPIO.output(23, False)
        time.sleep(1)
    else:
        print('buzzer')
        GPIO.output(24, True)
        time.sleep(1)
        GPIO.output(24, False)
        time.sleep(1)
    i += 1
