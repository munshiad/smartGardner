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

URI = "mongodb://am5113:IoTFabulous!!!@cluster0-shard-00-00-faxh9.mongodb.net:27017,cluster0-shard-00-01-faxh9.mongodb.net:27017,cluster0-shard-00-02-faxh9.mongodb.net:27017/smartGardner?ssl=true&ssl_cert_reqs=CERT_NONE&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"
client = pymongo.MongoClient(URI)
db = client.smartGardner

def get_humidity():
    # Create library object using our Bus I2C port
    i2c = busio.I2C(SCL, SDA)
    sensor = HTU21D(i2c)
    # print("\nTemperature: %0.1f C" % sensor.temperature)
    print("Humidity: %0.1f %%" % sensor.relative_humidity)
    return sensor.relative_humidity

def get_light():
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

def get_soil():
    i2c_bus = busio.I2C(SCL, SDA)
    ss = Seesaw(i2c_bus, addr=0x36)
    # read moisture level through capacitive touch pad
    touch = ss.moisture_read()
    # read temperature from the temperature sensor
    temp = ss.get_temp()
    print("Soil moisture: {0}".format(touch))
    return touch

def get_temp():
    i2c_bus = busio.I2C(SCL, SDA)
    ss = Seesaw(i2c_bus, addr=0x36)
    # read temperature from the temperature sensor
    temp = ss.get_temp()
    print("Temperature: {0}".format(temp))
    return round(temp, 2)

def get_accelerometer():
    i2c = busio.I2C(SCL, SDA)
    accelerometer = adafruit_adxl34x.ADXL345(i2c)
    acc = accelerometer.acceleration
    print(acc)
    result = {}
    result["z"] = round(acc[0], 2)
    result["x"] = round(acc[1], 2)
    result["y"] = round(acc[2], 2)
    return result

def get_status():
    status = "OK"  #TODO: change
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)  # red led
    GPIO.setup(23, GPIO.OUT)  # green led
    # TODO: how to update status??
    # TODO: change so not blocking????
    if status == "OK":
        GPIO.output(23, True)
        sleep(2)
        GPIO.output(23, False)
    else:
        GPIO.output(18, True)
        sleep(2)
        GPIO.output(18, False)

while True:
    response = {}
    response["date"] = datetime.datetime.now()
    response["humidity"] = get_humidity()
    response["light"] = get_light()
    response["soil"] = get_soil()
    response["temp"] = get_temp()
    response["accelerometer"] = get_accelerometer()
    db.smartGardner.insert_one(response)
    sleep(120)