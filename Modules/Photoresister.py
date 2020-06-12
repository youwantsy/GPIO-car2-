from Modules.Pcf8591 import Pcf8591
import time

class Photoresister:
    def __init__(self, pcf8591, ain = 0):
        self.__pcf8591 = pcf8591
        self.__ain = ain

    def read(self):
        value = self.__pcf8591.read(self.__ain) # 0~255
        return value

if __name__ == "__main__":
    try:
        pcf8591 = Pcf8591(0x48)
        photoresister = Photoresister(pcf8591, ain = 0)
        while True:
            tmeperature = photoresister.read()
            print("photoresister = ", tmeperature)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print()
    finally:
        print("Program exit")