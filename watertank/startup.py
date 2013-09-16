
from mqtt import MQTTWatcher
from mqtt import WaterTankMqttUpdater




mqtt = MQTTWatcher()
mqtt.start()

wtup = WaterTankMqttUpdater()
mqtt.addMsgHandlers(wtup.handlers)



