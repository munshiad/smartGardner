from machine import Pin, I2C
import math
import time

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


i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000)
adx = ADXL345(i2c)

while True :
    # time.sleep(50)
    x = adx.xValue
    y = adx.yValue
    z = adx.zValue
    print('The acceleration info of x, y, z are:%d,%d,%d' % (x, y, z))
    roll, pitch = adx.RP_calculate(x, y, z)
    print('roll=', roll)
    print('pitch=', pitch)
    time.sleep(.5)
