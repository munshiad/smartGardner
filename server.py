import socket
import json
from time import sleep
from board import SCL, SDA  # Circuit Python
import busio  # Circuit Python
from adafruit_htu21d import HTU21D  # humidity sensor library
import adafruit_tsl2591  # light sensor library
from adafruit_seesaw.seesaw import Seesaw  # soil moisture
import adafruit_adxl34x  # accelerometer
import RPi.GPIO as GPIO  # LED stuff
import pymongo

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
print("server running")

URI = "mongodb://am5113:IoTFabulous!!!@cluster0-shard-00-00-faxh9.mongodb.net:27017,cluster0-shard-00-01-faxh9.mongodb.net:27017,cluster0-shard-00-02-faxh9.mongodb.net:27017/smartGardner?ssl=true&ssl_cert_reqs=CERT_NONE&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"
client = pymongo.MongoClient(URI)
db = client.smartGardner

while True :
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    #try :
    request = conn.recv(1024).decode('utf8')
    #print(request)

    #request = json.loads(request)

    print(request)
    #command = request.get("Command")  # TODO: make consistent on android side
    command = request
    response = {}
    #command = "humidity"
    if "status" in command:

        response["humidity"] = get_humidity()
        response["light"] = get_light()
        response["soil"] = get_soil()
        response["accelerometer"] = get_accelerometer()
        get_status()
    elif "humidity" in command:
        response["humidity"] = get_humidity()
    elif "light" in command:
        response["light"] = get_light()
    elif "soil" in command:
        response["soil"] = get_soil()
    # TODO: change to an alert if accelerometer changes or something
    elif "accelerometer" in command:
        response["accelerometer"] = get_accelerometer()
    else:
        response["other"] = "Not a valid command!"
    response = json.dumps(response)

    conn.send(b'HTTP/1.0 200 OK\n')
    conn.send(b'Content-Type: text/html\n')
    conn.send(b'Connection: close\n\n')
    conn.sendall(bytes(response, encoding='utf8'))
    response = 'Command successfully processed!'
    conn.send(bytes(response, encoding='utf8'))


    #except Exception as e:
        #print(e)
        #print("404: File not found")
        #conn.send(b"HTTP/1.0 404\r\n")
        #conn.send(b"Content-Type:text/html\r\n\r\n")
        #response = "Command failed! Try again"
        #conn.send(bytes(response, encoding='utf8'))

    conn.close()



server()