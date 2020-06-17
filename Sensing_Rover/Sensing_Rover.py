import threading
import cv2
import paho.mqtt.client as mqtt
import base64
import RPi.GPIO as GPIO
from Modules.Pca9685 import Pca9685
from Mqtt.Publisher_camera import Publisher_camera
from Mqtt.Publisher_sensor import Publisher_sensor
from Mqtt.Subscriber_order import Subscriber_order
from HcSr04 import HcSr04
from Photoresister import Photoresister
from Tracking import Tracking
from Thermistor import Thermistor
from Gas import Gas
from RgbLed import RgbLed
from Pcf8591 import Pcf8591
from collections import deque
from Buzzer import Buzzer
from Laser import Laser
from Lcd1602 import Lcd1602
from DC_Motor import DC
from Sg90 import Sg90
import queue
import time
import json

class Sensing_Rover():
    def __init__(self):
        pass

    def __run(self):
        pass

    def read_sensor(self,gas ,thermister, photoresister, tracking, queue,):
        publisher_sensor.read_sensor(gas ,thermister, photoresister, tracking, queue)

    def send(self):
        pass

    def run_dc(self,channel_right,channel_left,set_speed,orderdata):
        if "DCGO" in orderdata:
            set_speed=int(orderdata.replace("DCGO",""))
            #for i in range(set_speed):
            dc_right.front(channel_right, set_speed)
            dc_left.front(channel_left, set_speed)
                #time.sleep(0.01)
        elif orderdata == "DCSTOP":
            dc_left.stop()
            dc_right.stop()

    def run_sg(self, orderdata):
        if "SVGO" in orderdata:
            set_angle = int(orderdata.replace("SVGO",""))
            sv.angle(set_angle)
        if orderdata == "SVSTOP":
            sv.angle(12)
        if "SHGO" in orderdata:
            set_angle = int(orderdata.replace("SHGO",""))
            sh.angle(set_angle)
        if orderdata == "SHSTOP":
            sh.angle(90)
        if "SWGO" in orderdata:
            set_angle = int(orderdata.replace("SWGO", ""))
            sw.angle(set_angle)
        if orderdata == "SWSTOP":
            sw.angle(90)
        if "SUGO" in orderdata:
            set_angle = int(orderdata.replace("SUGO", ""))
            su.angle(set_angle)
        if orderdata == "SUSTOP":
            su.angle(80)

    def run_laser(self, orderdata):
        if orderdata == "ENABLE":
            laser.on()
        if orderdata == "DISABLE":
            laser.off()

    def run_led(self, orderdata):
        if orderdata == "R":
            rgbLed.red()
        if orderdata == "G":
            rgbLed.green()
        if orderdata == "B":
            rgbLed.blue()
        if orderdata == "N":
            rgbLed.off()

    def run_buzzer(self, orderdata):
        if orderdata == "ON":
            buzzer.on()
        if orderdata == "OFF":
            buzzer.off()


    def run_lcd(self, orderdata):
        if orderdata == "TURNON":
            lcd.write(0,0,"HI HI HI")
            lcd.write(0,1,"BYE BYE BYE")
        if orderdata == "TURNOFF":
            lcd.clear()

    def read_camera(self, video):
        publiser_camera.read_camera(video)
def temperature_read():
    while True:
        temperature = thermister.read()
        time.sleep(1)
        if temperature > 30:
            flags[0] = True
            flags[1] = True
            flags[3] = True
            flags[4] = True
            while True:
                buzzer.on()
                rgbLed.off()
                dc_right.front(channel_right, 30)
                dc_left.front(channel_left, 30)
                lcd.write(0,0,"MOTOR OVERHEATED")
                lcd.write(0,1,"PLZ CALM DOWN!!!")
                time.sleep(0.5)
                buzzer.off()
                rgbLed.red()
                time.sleep(0.5)
                if thermister.read() < 30:

                    dc_left.stop()
                    dc_right.stop()
                    lcd.clear()
                    rgbLed.off()
                    flags[0] = False
                    flags[1] = False
                    flags[3] = False
                    flags[4] = False
                    break
def enemy_detect():
    try:
        while True:
            dis = ultra.read()
            time.sleep(0.3)
            if dis < 7:
                flags[0] = True
                flags[2] = True
                flags[3] = True
                flags[4] = True
                flags[6] = True
                while True:
                    dc_left.stop()
                    dc_right.stop()
                    lcd.write(0,0,"ENEMY DETECTED")
                    lcd.write(0,1,"LASER ATTACK!!!")
                    laser.on()

                    if ultra.read() < 3:
                        buzzer.on()
                    else:
                        buzzer.on()
                        time.sleep(0.3)
                        buzzer.off()
                    if ultra.read() > 7:
                        lcd.clear()
                        laser.off()
                        sh.patrol_move()
                        sh.angle(90)
                        flags[0] = False
                        flags[2] = False
                        flags[3] = False
                        flags[4] = False
                        flags[6] = False
                        break
    except Exception:
        enemy_detect()

if __name__ == "__main__":
    flags = [False,False,False,False,False,False,False,False,False]
    GPIO.cleanup()
    sensing_Rover = Sensing_Rover()

    pcf8591 = Pcf8591(0x48)
    gas = Gas(pcf8591, ain=2)
    thermister = Thermistor(pcf8591, ain=1)
    tracking = Tracking(32)
    photoresister = Photoresister(pcf8591, ain=0)
    ultra = HcSr04(trigpin=38, echopin=40)
    queue = deque()
    rgbLed = RgbLed(16,18,22)
    buzzer = Buzzer(35)
    laser = Laser(37)
    lcd = Lcd1602(0x27)

    pca9685 = Pca9685()
    dc_left = DC(11, 12, pca9685)
    dc_right = DC(13, 15, pca9685)
    channel_left = 5
    channel_right = 4
    set_speed = 80

    sv = Sg90(pca9685, 0)   # 5~90도   (default = 12도, 줄어들면 LOWER, 커지면 HIGHER)
    sh = Sg90(pca9685, 1)   # 12~170도   (default = 90도, 줄어들면 RIGHT, 커지면 LEFT)
    sw = Sg90(pca9685, 14)  # 50~130도   (default = 90도, 줄어들면 LEFT, 커지면 RIGHT)
    su = Sg90(pca9685, 15)  # 40~120도   (default = 80도, 줄어들면 RIGHT, 커지면 LEFT)

    publiser_camera = Publisher_camera("192.168.3.177", 1883, "/camerapub")
    publiser_camera.connect()

    publisher_sensor = Publisher_sensor("192.168.3.177", 1883, "/sensor", "/ultra")
    publisher_sensor.connect(gas ,thermister, photoresister, tracking, ultra, queue)

    subscriber_order = Subscriber_order("192.168.3.177", 1883, "/order/#")
    subscriber_order.connect()

    thread_tem = threading.Thread(target=temperature_read, daemon=True)
    thread_ult= threading.Thread(target=enemy_detect, daemon=True)

    thread_tem.start()
    thread_ult.start()
    while True:
        if len(subscriber_order.data) != 0:
            ##오더 부분
            orderdata = subscriber_order.data.popleft()

            k,v = orderdata.popitem()
            print(k)
            print(v)
            if  k == '/order/buzzer' and flags[0] == False:
                sensing_Rover.run_buzzer(v)
            elif  k == '/order/led' and flags[1] == False:
                sensing_Rover.run_led(v)
            elif  k == '/order/laser' and flags[2] == False:
                sensing_Rover.run_laser(v)
            elif  k == '/order/lcd' and flags[3] == False:
                sensing_Rover.run_lcd(v)
            elif k == '/order/dc' and flags[4] == False:
                sensing_Rover.run_dc(channel_right,channel_left,set_speed,v)
            elif k == '/order/sv' and flags[5] == False:
                sensing_Rover.run_sg(v)
            elif k == '/order/sh' and flags[6] == False:
                sensing_Rover.run_sg(v)
            elif k == '/order/sw' and flags[7] == False:
                sensing_Rover.run_sg(v)
            elif k == '/order/su' and flags[8] == False:
                sensing_Rover.run_sg(v)

        ## 센서값으로만 제어가 되는부분