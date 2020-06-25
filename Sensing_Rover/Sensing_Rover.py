import threading
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
from Buzzer import Buzzer
from Laser import Laser
from Lcd1602 import Lcd1602
from DC_Motor import DC
from Sg90 import Sg90
import time
import queue

def flagstatus(*args,stats=True):
    for i in args:
        flags[i] = stats

def thread_flagstatus(*args,stats=True):
    for i in args:
        thread_flags[i] = stats

class Sensing_Rover():
    def __init__(self):
        pass

    ######################### 센서읽기 #################################################
    def read_sensor(self,gas ,thermister, photoresister, tracking, queue):
        try:
            publisher_sensor.read_sensor(gas ,thermister, photoresister, tracking, queue)
        except Exception:
            self.read_sensor(gas,thermister,photoresister,tracking,queue)
    def send(self):
        pass
################################## dc모터 #############################################
    def run_dc(self,channel_right,channel_left,set_speed,orderdata):
        try:
            if "DCGO" in orderdata:
                set_speed=int(orderdata.replace("DCGO",""))
                #for i in range(set_speed):
                dc_right.front(channel_right, set_speed)
                dc_left.front(channel_left, set_speed)
                    #time.sleep(0.01)
            elif "DCBACKGO" in orderdata:
                set_speed = int(orderdata.replace("DCBACKGO", ""))
                dc_right.back(channel_right, set_speed)
                dc_left.back(channel_left, set_speed)
            elif orderdata == "DCSTOP":
                dc_left.stop()
                dc_right.stop()
        except Exception:
            self.run_dc(channel_right,channel_left,set_speed,orderdata)
#################################### 서보모터 ########################################
    def run_sg(self, orderdata):
        try:
            if "SVGO" in orderdata:
                set_angle = int(orderdata.replace("SVGO",""))
                sv.angle(set_angle)
            if orderdata == "SVSTOP":
                sv.angle(20)
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
        except Exception:
            self.run_sg(orderdata)
 ############################# 레이저 ##################################
    def run_laser(self, orderdata):
        try:
            if orderdata == "ENABLE":
                laser.on()
            if orderdata == "DISABLE":
                laser.off()
        except Exception:
            self.run_laser(orderdata)
################################ LED##########################
    def run_led(self, orderdata):
        try:
            if orderdata == "R":
                rgbLed.red()
            if orderdata == "G":
                rgbLed.green()
            if orderdata == "B":
                rgbLed.blue()
            if orderdata == "W":
                rgbLed.white()
            if orderdata == "N":
                rgbLed.off()
        except Exception:
            self.run_led(orderdata)
################################ 버저 ################################
    def run_buzzer(self, orderdata):
        try:
            if orderdata == "ON":
                buzzer.on()
            if orderdata == "OFF":
                buzzer.off()
        except Exception:
            self.run_buzzer(orderdata)
############################ LCD ###################################
    def run_lcd(self, orderdata):
        try:
            if orderdata == "TURNON":
                lcd.write(0,0,"** M1 ABRAMS **")
                lcd.write(0,1,"MISSON CODE:AIOT")
            if orderdata == "TURNOFF":
                lcd.clear()
        except Exception:
            self.run_lcd(orderdata)
############################## 카메라 ################################
    def read_camera(self, video):
        try:
            publiser_camera.read_camera(video)
        except Exception:
            self.read_camera(orderdata)

################# AUTO SENSING - MOTOR TEMPERATURE ##################
def temperature_read():
    while True:
        if thread_flags[0] == True:
            while True:
                if thread_flags[0] == False:
                    break
                time.sleep(0.3)
        temperature = thermister.read()
        time.sleep(1)
        if temperature > 30:
            thread_flagstatus(1,2,3,4,stats=True)
            flagstatus(0,1,3,4,5,6,7,8,stats=True)
            while True:
                buzzer.on()
                rgbLed.off()
                dc_right.front(channel_right, 30)
                dc_left.front(channel_left, 30)
                lcd.clear()
                lcd.write(0,0,"MOTOR OVERHEATED")
                lcd.write(0,1,"PLZ CALM DOWN!!!")
                time.sleep(0.5)
                buzzer.off()
                rgbLed.red()
                time.sleep(0.5)
                if thermister.read() < 30:
                    dc_left.front(channel_left, 80)
                    dc_right.front(channel_right, 80)
                    lcd.clear()
                    rgbLed.off()
                    thread_flagstatus(1, 2, 3, 4, stats=False)
                    flagstatus(0, 1, 3, 4, 5, 6, 7, 8, stats=False)
                    break

################# AUTO SENSING - ENEMY DETECT ##################
def enemy_detect():
    try:
        pre_dis = 7
        while True:
            if thread_flags[1] == True:
                while True:
                    if thread_flags[1] == False:
                        break
                    time.sleep(0.3)
            dis = ultra.read()
            time.sleep(0.3)

            if abs(pre_dis - dis) < 1 and dis < 7:
                thread_flagstatus(0, 2, 3, 4, stats=True)
                flagstatus(0, 2, 3, 4, 5, 6, 7, 8, stats=True)
                while True:
                    sv.angle(20)
                    dc_left.stop()
                    dc_right.stop()
                    lcd.clear()
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
                        lcd.write(0, 0, "LASER RELEASED")
                        lcd.write(0, 1, "PATROL MODE ON")

                        laser.off()
                        sh.patrol_move()
                        dc_left.front(channel_left, 80)
                        dc_right.front(channel_right, 80)
                        sh.angle(90)
                        lcd.clear()
                        thread_flagstatus(0, 2, 3, 4, stats=False)
                        flagstatus(0, 2, 3, 4, 5, 6, 7, 8, stats=False)
                        break
            pre_dis = dis
    except Exception:
        enemy_detect()

################# AUTO SENSING - GAS DETECT ##################
def gas_detect():
    while True:
        if thread_flags[2] == True:
            while True:
                if thread_flags[2] == False:
                    break
                time.sleep(0.3)
        ggas = gas.read()
        time.sleep(1)
        if ggas > 80:
            thread_flagstatus(0, 1, 3, 4, stats=True)
            flagstatus(0, 1, 3, 4, 5, 6, 7, 8, stats=True)
            while True:
                dc_right.back(channel_right,80)
                dc_left.back(channel_left,80)
                lcd.write(0,0,"SITUATION : MOPP")
                lcd.write(0,1,"RETREAT MODE ON")
                sv.angle(90)
                rgbLed.green()
                for i in range(3):
                    buzzer.on()
                    time.sleep(0.3)
                    buzzer.off()
                    time.sleep(0.3)

                if gas.read() < 80:
                    rgbLed.off()
                    lcd.clear()
                    dc_left.front(channel_left,80)
                    dc_right.front(channel_right,80)
                    sv.angle(20)
                    thread_flagstatus(0, 1, 3, 4, stats=False)
                    flagstatus(0, 1, 3, 4, 5, 6, 7, 8, stats=False)
                    break

################ AUTO SENSING - LAND MINE DETECT ###################
def mine_detect():
    while True:
        if thread_flags[3] == True:
            while True:
                if thread_flags[3] == False:
                    break
                time.sleep(0.3)
        md = tracking.read()
        time.sleep(1)
        if md == 0:
            thread_flagstatus(0, 1, 2, 4, stats=True)
            flagstatus(0, 1, 3, 4, 5, 6, 7, 8, stats=True)
            while True:
                dc_left.stop()
                dc_right.stop()
                time.sleep(1)
                dc_right.back(channel_right, 20)
                dc_left.back(channel_left, 20)
                lcd.clear()
                lcd.write(0, 0, "MINE DETECTED")
                lcd.write(0, 1, "RETREAT MODE ON")
                for i in range(3):
                    rgbLed.blue()
                    buzzer.on()
                    time.sleep(0.3)
                    rgbLed.off()
                    buzzer.off()
                    time.sleep(0.3)
                if tracking.read() == 1:
                    rgbLed.off()
                    buzzer.off()
                    lcd.clear()
                    dc_left.front(channel_left, 80)
                    dc_right.front(channel_right, 80)
                    thread_flagstatus(0, 1, 2, 4, stats=False)
                    flagstatus(0, 1, 3, 4, 5, 6, 7, 8, stats=False)
                    break

################ AUTO SENSING - NIGHT DRIVING MODE ###################
def night_mode():
    while True:
        if thread_flags[4] ==True:
            while True:
                if thread_flags[4] == False:
                    break
                time.sleep(0.3)
        lux = photoresister.read()
        time.sleep(1)
        if lux >= 120:
            thread_flagstatus(0, 1, 2, 3, stats=True)
            flagstatus(1, 3, 5, 6, 7, 8, stats=True)
            while True:
                lcd.write(0,0,"Night Driving")
                lcd.write(0,1,"Flash ON")
                rgbLed.white()
                if photoresister.read() < 120:
                    lcd.clear()
                    rgbLed.off()
                    thread_flagstatus(0, 1, 2, 3, stats=False)
                    flagstatus(1, 3, 5, 6, 7, 8, stats=False)
                    break


if __name__ == "__main__":
    now_Thread = 0
    flags = [False,False,False,False,False,False,False,False,False]
    thread_flags = [False,False,False,False,False]
    GPIO.cleanup()
    sensing_Rover = Sensing_Rover()

    pcf8591 = Pcf8591(0x48)
    gas = Gas(pcf8591, ain=2)
    thermister = Thermistor(pcf8591, ain=1)
    tracking = Tracking(32)
    photoresister = Photoresister(pcf8591, ain=0)
    ultra = HcSr04(trigpin=38, echopin=40)
    queue = queue.Queue()
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
    publiser_camera.connect(gas,thermister, photoresister, tracking,ultra)

    publisher_sensor = Publisher_sensor("192.168.3.177", 1883, "/sensor", "/ultra")
    publisher_sensor.connect(gas ,thermister, photoresister, tracking, ultra, queue)

    subscriber_order = Subscriber_order("192.168.3.177", 1883, "/order/#")
    subscriber_order.connect()

    thread_tem = threading.Thread(target=temperature_read, daemon=True, name="3")
    thread_ult = threading.Thread(target=enemy_detect, daemon=True, name="1")
    thread_gas = threading.Thread(target=gas_detect, daemon=True, name="4")
    thread_mine = threading.Thread(target=mine_detect, daemon=True, name="2")
    thread_night = threading.Thread(target=night_mode, daemon=True, name="5")

    thread_tem.start()
    thread_ult.start()
    thread_gas.start()
    thread_mine.start()
    thread_night.start()

    while True:
        orderdata = subscriber_order.data.get()

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
        elif k== '/order/mode':
            if v == 'MODEON':
                thread_flags = [True,True,True,True,True]
                sensing_Rover.run_dc(channel_right, channel_left, set_speed, "DCSTOP")
                #tensor = np.array(thread_flags)
                #tensor = tensor+[True]
                #thread_flags= tensor.tolist()

            else:
                thread_flags = [False,False,False,False,False]
                sensing_Rover.run_dc(channel_right, channel_left,set_speed, "DCGO80")
                #tensor = np.array(thread_flags)
                #tensor = tensor * [False]
                #thread_flags = tensor.tolist()