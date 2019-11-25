from machine import Pin, I2C
import tsl2591

tsl = tsl2591.Tsl2591(123)  # initialize

while(1):
    full, ir = tsl.get_full_luminosity()  # read raw values (full spectrum and ir spectrum)
    lux = tsl.calculate_lux(full, ir)  # convert raw values to lux
    print(lux, full, ir)

# i2c = I2C(-1, scl=Pin(5), sda=Pin(4))