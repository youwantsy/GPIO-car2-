import threading
import cv2
import paho.mqtt.client as mqtt
import base64
import json


#v = cv2.VideoCapture(0)
class Publisher_camera:
    def __init__(self, brokerIp, brokerPort, pubtopic):
        self.__brokerIp = brokerIp
        self.__brokerPort = brokerPort
        self.pubtopic = pubtopic

    def __run(self):
        self.client = mqtt.Client()
        self.client.on_connect= self.__on_connect
        self.client.on_disconnect = self.__on_disconnect
        self.client.connect(self.__brokerIp, self.__brokerPort)
        self.client.loop_forever()

    def connect(self,gas ,thermister, photoresister, tracking, ultra):
        print("Vconnect")
        thread = threading.Thread(target=self.read_camera, daemon=True, args=(gas ,thermister, photoresister, tracking, ultra))
        thread.start()
        thread2 = threading.Thread(target=self.__run, daemon=True)
        thread2.start()

    def disconnect(self):
        self.client.disconnect()

    def __on_connect(self, client, userdata, flags, rc):
        print("VImageMqttClient mqtt broker connected")

    def __on_disconnect(self, client, userdata, rc):
        print("VImageMqttClient mqtt broker disconnected")

    def sendBase64(self, frame):
        if self.client.is_connected() is False: # jpg -> cv2.imeconde ->  base64.b64encode
            return
        retval, bytes = cv2.imencode('.jpg', frame)
        if not retval:
            print("image encoding fail")
            return
        b64_bytes = base64.b64encode(bytes)
        self.client.publish(self.pubtopic , b64_bytes)

    def read_camera(self,gas ,thermister, photoresister, tracking, ultra):
        video = cv2.VideoCapture(0)
        video.read()

        video.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        video.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        print("된다")
        while True:
            if video.isOpened():

                retval, data = video.read()
                # cv2.circle(data, (160, 120), 75, color=(0, 0, 255), thickness=2, lineType=cv2.LINE_4)
                # cv2.line(data, (160, 70), (160, 20), color=(0, 0, 255), thickness=2, lineType=cv2.LINE_4)
                # cv2.line(data, (160, 170), (160, 220), color=(0, 0, 255), thickness=2, lineType=cv2.LINE_4)
                # cv2.line(data, (210, 120), (260, 120), color=(0, 0, 255), thickness=2, lineType=cv2.LINE_4)
                # cv2.line(data, (110, 120),(60, 120), color=(0, 0, 255), thickness=2, lineType=cv2.LINE_4)
                # cv2.putText(data, "GAS :"+str(gas.read()),(230,180),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.3,color=(255,255,255),thickness=1,lineType=cv2.LINE_AA)
                # cv2.putText(data, "Thermister :"+str(thermister.read()), (230, 190),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.3, color=(255,255,255), thickness=1, lineType=cv2.LINE_AA)
                # cv2.putText(data, "Photoresister :"+str(photoresister.read()), (230, 200),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.3, color=(255,255,255), thickness=1, lineType=cv2.LINE_AA)
                # cv2.putText(data, "Ultrasonic :"+str(ultra.read()), (230, 210),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.3, color=(255,255,255), thickness=1, lineType=cv2.LINE_AA)
                # cv2.putText(data, "Tracking :"+str(tracking.read()), (230, 220),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.3, color=(255,255,255), thickness=1, lineType=cv2.LINE_AA)
                if not retval:
                    print("read fail")
                    break
                self.sendBase64(data)
            else:
                break

        video.release()
        self.disconnect()
        print("Program exit")
#


