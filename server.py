import socket
import json
from time import sleep
from board import SCL, SDA  # Circuit Python
import busio  # Circuit Python
from adafruit_htu21d import HTU21D  # humidity sensor library
import adafruit_tsl2591  # light sensor library
from adafruit_seesaw.seesaw import Seesaw  # soil moisture
import adafruit_adxl34x  # accelerometer

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
    print('Visible: {0}'.format(sensor.visible))
    # print('Infrared: {0}'.format(sensor.infrared))
    return sensor.visible

def get_soil():
    i2c_bus = busio.I2C(SCL, SDA)
    ss = Seesaw(i2c_bus, addr=0x36)
    # read moisture level through capacitive touch pad
    touch = ss.moisture_read()
    # read temperature from the temperature sensor
    temp = ss.get_temp()
    print("Soil moisture: {0}".format(touch))
    return touch

def get_accelerometer():
    i2c = busio.I2C(board.SCL, board.SDA)
    accelerometer = adafruit_adxl34x.ADXL345(i2c)
    print(accelerometer.acceleration)
    return accelerometer.acceleration

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    print("server running")

    while True :
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        try :
            request = conn.recv(1024).decode('utf8')
            request = json.loads(request)
            print(request)
            command = request.get("Command")  # TODO: make consistent on android side
            response = json()
            if "humidity" in command:
                response["humidity"] = get_humidity()
            elif "light" in command:
                response["light"] = get_light()
            elif "soil" in command:
                response["soil"] = get_soil()
            # TODO: change to an alert if accelerometer changes or something
            elif accelerometer in command:
                response["accelerometer"] = get_accelerometer()
            else:
                pass

            conn.send(b'HTTP/1.0 200 OK\n')
            conn.send(b'Content-Type: text/html\n')
            conn.send(b'Connection: close\n\n')
            conn.send(bytes(response, encoding='json'))
            response = 'Command successfully processed!'
            conn.send(bytes(response, encoding='utf8'))


        except Exception as e:
            print(e)
            print("404: File not found")
            conn.send(b"HTTP/1.0 404\r\n")
            conn.send(b"Content-Type:text/html\r\n\r\n")
            response = "Command failed! Try again"
            conn.send(bytes(response, encoding='utf8'))

        conn.close()



server()