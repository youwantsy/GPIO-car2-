import time
import math
from Modules.Pcf8591 import Pcf8591

class Thermistor:
    def __init__(self, pcf8591, ain=1):
        self.__pcf8591 = pcf8591
        self.__ain = ain

    def read(self):
        analog = self.__pcf8591.read(self.__ain)
        temp = 5 * float(analog) / 255
        temp = 10000 * temp / (5 - temp)
        temp = 1 / (((math.log(temp / 10000)) / 3950) + (1 / (273.15 + 25)))
        return (temp - 273.15)

if __name__ == "__main__":
    try:
        pcf8591 = Pcf8591(0x48)
        thermister = Thermistor(pcf8591, ain = 1)
        while True:
            tmeperature = thermister.read()
            print("temperature = ", tmeperature, "C")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print()
    finally:
        print("Program exit")