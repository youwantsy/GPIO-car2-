import smbus
import time

class Pcf8591:
    def __init__(self, addr):
        self.__bus = smbus.SMBus(1)
        self.__addr = addr

    def read(self, channel):
        try:
            if channel == 0:
                self.__bus.write_byte(self.__addr, 0x40)
            elif channel == 1:
                self.__bus.write_byte(self.__addr, 0x41)
            elif channel == 2:
                self.__bus.write_byte(self.__addr, 0x42)
            elif channel == 3:
                self.__bus.write_byte(self.__addr, 0x43)
            else:
                pass
            self.__bus.read_byte(self.__addr)
        except Exception as e:
            print(e)
        return self.__bus.read_byte(self.__addr)

    def write(self, val):
        try:
            temp = int(val)
            self.__bus.write_byte_date(self.__addr, 0x40, temp)
        except Exception as e:
            print(e)