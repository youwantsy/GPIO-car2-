import paho.mqtt.client as mqtt
import threading
import queue

class Subscriber_order:
    data = queue.Queue()
    def __init__(self,brokerIp, brokerPort, subtopic):
        self.__brokerIp = brokerIp
        self.__brokerPort = brokerPort
        self.__subtopic = subtopic

    def connect(self):
        thread = threading.Thread(target=self.__run)
        thread.start()

    def __run(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.__on_connect
        self.client.on_disconnect = self.__on_disconnect
        self.client.connect(self.__brokerIp, self.__brokerPort)
        self.client.loop_forever()

    def __on_connect(self, client, userdata, flags, rc):
        print("Subscriber_order mqtt broker connected")
        self.client.on_message = self.__on_message
        self.client.subscribe(self.__subtopic)

    def __on_disconnect(self):
        print("Subscriber_order mqtt broker disconnected")

    def __on_message(self, client, userdata, message):
        datadic = {}
        datadic.update({message.topic:str(message.payload, encoding="UTF-8")})
        self.data.put(datadic)
        #print(data)

    def disconnect(self):
        self.client.disconnect()

if __name__ == "__main__":
    subscriber_order = Subscriber_order("192.168.3.177", 1883, "/order/#")
    subscriber_order.connect()