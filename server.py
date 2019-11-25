from machine import Pin, I2C, RTC, ADC
import ssd1306
import socket

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    while True :
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        try :
            request = conn.recv(1024)  # might be getting tuple (message, addr) or just message
            request = str(request, 'utf8')
            # print(request)

            # command = request[-1]
            # print('command = %s' % request)
            print(request)

            conn.send('HTTP/1.0 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            response = 'Command successfully processed!'
            conn.send(response)

        except :
            print("404: File not found")
            conn.send("HTTP/1.0 404\r\n")
            conn.send("Content-Type:text/html\r\n\r\n")
            response = "Command failed! Try again"
            conn.send(response)

        conn.close()



server()
