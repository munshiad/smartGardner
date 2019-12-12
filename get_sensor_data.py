from time import sleep
from board import SCL, SDA  # Circuit Python
import busio  # Circuit Python
from adafruit_htu21d import HTU21D  # humidity sensor library
import adafruit_tsl2591  # light sensor library
from adafruit_seesaw.seesaw import Seesaw  # soil moisture
import adafruit_adxl34x  # accelerometer
import RPi.GPIO as GPIO  # LED stuff
import datetime
import pymongo
import I2C_LCD_driver

URI = "mongodb://am5113:IoTFabulous!!!@cluster0-shard-00-00-faxh9.mongodb.net:27017,cluster0-shard-00-01-faxh9.mongodb.net:27017,cluster0-shard-00-02-faxh9.mongodb.net:27017/smartGardner?ssl=true&ssl_cert_reqs=CERT_NONE&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"
client = pymongo.MongoClient(URI)
db = client.smartGardner

def get_humidity():
    try:
        # Create library object using our Bus I2C port
        i2c = busio.I2C(SCL, SDA)
        sensor = HTU21D(i2c)
        # print("\nTemperature: %0.1f C" % sensor.temperature)
        print("Humidity: %0.1f %%" % sensor.relative_humidity)
        return sensor.relative_humidity
    except Exception as e:
        return 0

def get_light():
    try:
        i2c = busio.I2C(SCL, SDA)
        sensor = adafruit_tsl2591.TSL2591(i2c)
        # print('Light: {0}lux'.format(sensor.lux))
        # print('Visible: {0}'.format(sensor.visible))
        # print('Infrared: {0}'.format(sensor.infrared))
        result = {}
        result["light"] = sensor.lux
        result["visible"] = sensor.visible
        result["infrared"] = sensor.infrared
        result["full_spectrum"] = sensor.full_spectrum
        result["raw_luminosity"] = sensor.raw_luminosity
        print(result)
        return result
    except Exception as e:
        result = {}
        result["light"] = 0
        result["visible"] = 0
        result["infrared"] = 0
        result["full_spectrum"] = 0
        result["raw_luminosity"] = 0
        return result


def get_soil():
    try:
        i2c_bus = busio.I2C(SCL, SDA)
        ss = Seesaw(i2c_bus, addr=0x36)
        # read moisture level through capacitive touch pad
        touch = ss.moisture_read()
        # read temperature from the temperature sensor
        temp = ss.get_temp()
        print("Soil moisture: {0}".format(touch))
        return touch
    except Exception as e:
        return 0

def get_temp():
    try:
        i2c_bus = busio.I2C(SCL, SDA)
        ss = Seesaw(i2c_bus, addr=0x36)
        # read temperature from the temperature sensor
        temp = ss.get_temp()
        print("Temperature: {0}".format(temp))
        return round(temp, 2)
    except Exception as e:
        return 0

def get_accelerometer():
    try:
        i2c = busio.I2C(SCL, SDA)
        accelerometer = adafruit_adxl34x.ADXL345(i2c)
        acc = accelerometer.acceleration
        print("Accelerometer" + str(acc))
        result = {}
        result["z"] = round(acc[0], 2)
        result["x"] = round(acc[1], 2)
        result["y"] = round(acc[2], 2)
        return result
    except Exception as e:
        result = {}
        result["z"] = 0
        result["x"] = 0
        result["y"] = 0
        return result

def evaluate_status(score, fall_status, water_status):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)  # red led
    GPIO.setup(25, GPIO.OUT)  # green led
    GPIO.setup(12, GPIO.OUT)  # yellow led
    GPIO.setup(24, GPIO.OUT)  # buzzer
    GPIO.setup(23, GPIO.OUT)  # blue led
    mylcd = I2C_LCD_driver.lcd()
    mylcd.lcd_display_string("Health: " + str(score), 1)
    fall = False
    need_water = False
    try:
        # eval score
        if 70 <= score <= 100:  # good!
            GPIO.output(25, True) # green
            GPIO.output(12, False)  # yellow
            GPIO.output(18, False)  # red
            GPIO.output(24, False)  # buzzer
        elif 40 <= score <= 70:  # ok -- yellow
            GPIO.output(25, False) # green
            GPIO.output(12, True)  # yellow
            GPIO.output(18, False)  # red
            GPIO.output(24, False)  # buzzer
        elif 0 < score <= 40:  # bad -- red
            GPIO.output(25, False) # green
            GPIO.output(12, False)  # yellow
            GPIO.output(18, True)  # red
            GPIO.output(24, True)  # buzzer
        else:
            # something went wrong
            GPIO.output(25, True) # green
            GPIO.output(12, True)  # yellow
            GPIO.output(18, True)  # red
        
        # eval water_status
        if water_status <= 700:  # TODO*: figure out value
            GPIO.output(23, True)  # blue
            need_water = True
        else:
            GPIO.output(23, False)  # blue
        
        # eval fall
        if -12 <= fall_status["z"] <= -8:  # upright
            if 0 < score <= 40:
                pass
            else:
                GPIO.output(18, False)  # red
                GPIO.output(24, False)  # buzzer
        else:
            GPIO.output(18, True)  # red
            GPIO.output(24, True)  # buzzer
            fall = True


    except Exception as e:
        pass
    return fall, need_water

# TODO*: add other rules ex. temp, light, soil
def get_health_score(response):
    score = 0
    humidityScore = 0
    tempScore = 0
    soilScore = 0
    lightScore = 0  #max 25 each
    try:
        #humidityScores
        if 0 <= response["humidity"] < 10:
            humidityScore += 10
        elif 10 <= response["humidity"] < 60:
            humidityScore += 25  # good!
        elif 60 <= response["humidity"] < 80:
            humidityScore +=20
        elif 80 <= response["humidity"] < 100:
            humidityScore += 5  # bad
        else:
            humidityScore += 0  #worst
        print("Humidity score: " + str(humidityScore))

        #tempScores  # Celcius
        if response["temp"] < 10:
            tempScore +=0   #really bad
        elif 10 <= response["temp"] < 18:
            tempScore += 15  #bad
        elif  18 <= response["temp"] < 22:
            tempScore +=25  #good
        elif 22 <= response["temp"] < 33:
            tempScore += 15  # bad
        else:
            tempScore += 0  #worst
        print("Temp score: " + str(tempScore))

        #lightScores ****
        light_dict = response["light"]
        light = light_dict["light"]
        if light < 20:
            lightScore += 5
        elif 20 <= light <= 200:
            lightScore +=25   #best
        elif 200 <= light <= 1000:
            lightScore += 15
        elif 1000 <= light <= 1800: # flashlight to sensor
            lightScore += 10
        else:
            lightScore += 0  #worst
        print("Light score: " + str(lightScore))

        #soilScores ****
        if response["soil"] < 300:
            soilScore +=0   #really bad
        elif 300 <= response["soil"] <=500:
            soilScore +=10
        elif 500 <= response["soil"] <= 700:
            soilScore += 20
        elif 700 <= response["soil"] <=1020:
            soilScore += 25
        else:
            # error?
            soilScore += 0
        print("Soil score: " + str(soilScore))
        
        score  = humidityScore + tempScore + soilScore + lightScore

        print("Total score: " + str(score))
        return score
    except:
        return 0  # error!!

while True:
    try:
        response = {}
        response["date"] = datetime.datetime.now()
        response["humidity"] = get_humidity()
        response["light"] = get_light()
        response["soil"] = get_soil()
        response["temp"] = get_temp()
        response["accelerometer"] = get_accelerometer()
        print("----------")
        score = get_health_score(response)
        fall, need_water = evaluate_status(score, response["accelerometer"], response["soil"])
        response["fall_status"] = fall
        response["water_status"] = need_water
        response["score"] = score
        print("Fallen? " + str(fall))
        print("Need water? " + str(need_water))
        #db.demoDay.insert_one(response)
        db.smartGardner.insert_one(response)
        sleep(60)
    except Exception as e:
        pass
