import threading
import signal
import sys
import time
from queue import Queue
from datetime import datetime

from temperature import TemperatureSensor
from flame import FlameSensor
from rotary import RotarySensor
from observer import Observer


threads = []
sleeptime = 0.1
temperature_threshold = 60

def signal_handler(signal, frame):
    print ("Closing all threads...")
    for t in threads:
        if t.isAlive():
            t.stop()
    for t in threads:
        if t.isAlive():
            t.join()
    print ("Finished.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

queue_ = Queue(0)
obs = Observer(queue_)

temp_sensor = TemperatureSensor("temp", queue_, sleeptime, pin = 0)
#rotary_sensor = RotarySensor(thread_id="rotary", queue_, sleeptime)

def tempAlarm(*args, **kwargs):
    print ("HIGH TEMPERATURE: %s" % str(kwargs["value"]))
obs.addSensor("temp", temperature_threshold, tempAlarm)

def tempAlarm(*args, **kwargs):
    print ("HIGH TEMPERATURE: %s" % str(kwargs["value"]))
obs.addSensor("temp", temperature_threshold, tempAlarm)

#obs.addSensor(thread_id="rotary_sensor", -1, action) # -1 for any positive value (0 and 1 as binary)

threads.append(obs)
threads.append(temp_sensor)
#threads.append(rotary_sensor)

for t in threads:
    t.start()

while (True):
    pass