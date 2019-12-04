from machine import Pin, I2C, RTC, ADC
import ssd1306
import socket
import tsl2591
import network

device = const(0x53)
regAddress = const(0x32)
TO_READ = 6
buff = bytearray(6)


class ADXL345 :
    def __init__(self, i2c, addr=device) :
        self.addr = addr
        self.i2c = i2c
        b = bytearray(1)
        b[0] = 0
        self.i2c.writeto_mem(self.addr, 0x2d, b)
        b[0] = 16
        self.i2c.writeto_mem(self.addr, 0x2d, b)
        b[0] = 8
        self.i2c.writeto_mem(self.addr, 0x2d, b)

    @property
    def xValue(self) :
        buff = self.i2c.readfrom_mem(self.addr, regAddress, TO_READ)
        x = (int(buff[1]) << 8) | buff[0]
        if x > 32767 :
            x -= 65536
        return x

    @property
    def yValue(self) :
        buff = self.i2c.readfrom_mem(self.addr, regAddress, TO_READ)
        y = (int(buff[3]) << 8) | buff[2]
        if y > 32767 :
            y -= 65536
        return y

    @property
    def zValue(self) :
        buff = self.i2c.readfrom_mem(self.addr, regAddress, TO_READ)
        z = (int(buff[5]) << 8) | buff[4]
        if z > 32767 :
            z -= 65536
        return z

    def RP_calculate(self, x, y, z) :
        roll = math.atan2(y, z) * 57.3
        pitch = math.atan2((- x), math.sqrt(y * y + z * z)) * 57.3
        return roll, pitch

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000)
    adx = ADXL345(i2c)
    tsl = tsl2591.Tsl2591(123)  # initialize
    sta_if = network.WLAN(network.STA_IF)
    print(sta_if.ifconfig())
    while True :
        print("listening....")
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        try :
            request = conn.recv(1024)  # might be getting tuple (message, addr) or just message
            request = str(request, 'utf8')
            # print(request)
            print(request)

            # command = request[-1]
            # print('command = %s' % request)
            if "acceleration" in request:
                x = adx.xValue
                y = adx.yValue
                z = adx.zValue
                response = (x, y, z)
                print('The acceleration info of x, y, z are:%d,%d,%d' % (x, y, z))
                conn.send('HTTP/1.0 200 OK\n')
                conn.send('Content-Type: text/html\n')
                conn.send('Connection: close\n\n')
                conn.send(str.encode(response))
            elif "light" in request:
                full, ir = tsl.get_full_luminosity()  # read raw values (full spectrum and ir spectrum)
                lux = tsl.calculate_lux(full, ir)  # convert raw values to lux
                response = (lux, full, ir)
                print(response)
                conn.send(b'HTTP/1.0 200 OK\n')
                conn.send(b'Content-Type: text/html\n')
                conn.send(b'Connection: close\n\n')
                conn.send(str.encode(response))

            else:
                conn.send(b'HTTP/1.0 200 OK\n')
                conn.send(b'Content-Type: text/html\n')
                conn.send(b'Connection: close\n\n')
                # response = 'Command successfully processed!'
                conn.send(str.encode(request))

        except Exception as e:
            print("404: File not found")
            print(e)
            conn.send(b"HTTP/1.0 404\r\n")
            conn.send(b"Content-Type:text/html\r\n\r\n")
            response = "Command failed! Try again"
            conn.send(str.encode(response))

        conn.close()



server()
