import socket
import json
import pymongo
from datetime import datetime, timedelta
import get_sensor_data as sensor_data

status = "OK"
# cron job for image capture: 0 1,13 * * * rm /var/www/*/somedir/index.php > /home/someuser/cronlogs/some.log 2>&1  is for 1AM and 1PM
# for us: 0 7,19 * * * python3 ___________________ > /home/someuser/cronlogs/some.log 2>&1  is for 7AM and 7PM
#def server():
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
    if "humidity" in command:
        response["humidity"] = sensor_data.get_humidity()
    elif "light" in command:
        response["light"] = sensor_data.get_light()
    elif "soil" in command:
        response["soil"] = sensor_data.get_soil()
    # TODO: change to an alert if accelerometer changes or something
    elif "accelerometer" in command:
        response["accelerometer"] = sensor_data.get_accelerometer()
    elif "status" in command:

        response["humidity"] = sensor_data.get_humidity()
        response["light"] = sensor_data.get_light()
        response["soil"] = sensor_data.get_soil()
        response["accelerometer"] = sensor_data.get_accelerometer()
        sensor_data.get_status()
        # put on database
    else:
        response["other"] = "Not a valid command!"
    response = json.dumps(response)
    #db.smartGardner.insert_one(response)

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



#server()