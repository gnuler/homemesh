
import threading
import mosquitto
import time


class MQTTWatcher(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.topic = "#"
        self.handlers = {}

        self.hostname = "127.0.0.1"
        self.client =  mosquitto.Mosquitto("test-client")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_subcribe = self.on_subcribe
        self.client.on_publish = self.on_publish
        self.client.on_log = self.on_log

        self.stop_ev = threading.Event()

    def on_connect(self, obj, rc):
        if rc == 0:
            print("Connected successfully.")

    def on_message(self, obj, msg):
        parts = msg.topic.split('/')
        root = self.handlers

        for i in range(len(parts)):
            p = parts[i]
            lastOne = i == (len(parts)-1)

            if p in root.keys():
                if lastOne:
                    root[p](msg.payload)
                else:
                    root = root[p]
            else:
                print "Unhandled msg"
                return


    def on_publish(self, obj,  mid):
        #print "on_publish"
        pass

    def on_subcribe(self, obj, mid, granted_qos):
        #print "on_subcribe"
        pass

    def on_log(self, obj, level, string):
        print string

    def stop(self):
        self.stop_ev.set()
    
    def run(self):

        self.client.connect("127.0.0.1", 1883)
        print self.client.subscribe("#")    

        res = 0
        while (not self.stop_ev.is_set() and res == 0):
            res = self.client.loop()

        self.client.disconnect()

    def addMsgHandlers(self, handlers):
        self.handlers.update(handlers)


from watertank.models import WaterTankController

def onOffToBool(string):
    if string.lower() == "on":
        return True
    elif string.lower() == "off":
        return False
    
    print "Unknown status"
    return None
 
class WaterTankMqttUpdater:

    def __init__(self):

        self.handlers = {
            'WaterTank' : { 
                'Pump': { 
                    'Main' : { 'Status' : self.mainPumpStateChanged }
                 },
                'Sensor': {
                    'AlarmHigh' : { ' Status' : self.alarmHighStateChanged },
                    'AlarmLoq'  : { ' Status' : self.alarmLowStateChanged }
                }
                        
            }
        }


   
    def mainPumpStateChanged(self, msg):
        wtc = WaterTankController.objects.get()
        wtc.pumpIsOn = onOffToBool(msg)
        wtc.save()

    def alarmHighStateChanged(self, msg):
        wtc = WaterTankController.objects.get()
        wtc.alarmHigh = onOffToBool(msg)
        wtc.save()

    def alarmLowStateChanged(self, msg):
        wtc = WaterTankController.objects.get()
        wtc.alarmLow = onOffToBool(msg)
        wtc.save()

    
if False:

    mqtt = MQTTWatcher()
    mqtt.start()

    wtup = WaterTankMqttUpdater()

    mqtt.addMsgHandlers(wtup.handlers)
    #mqtt.addMsgHandlers(handlers)

    while True:
        try:
            print "lalala"
            time.sleep(10)
        except KeyboardInterrupt:
            print "Ctrl-c received! Sending kill to threads..."
            mqtt.stop()
