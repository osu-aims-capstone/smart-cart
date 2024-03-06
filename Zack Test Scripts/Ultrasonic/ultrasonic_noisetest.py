import RPi.GPIO as GPIO
import time
import csv
from datetime import timedelta
GPIO.setmode(GPIO.BCM)
CM_TO_FEET = 30.48
runs = []
logfile = input('Output file name?\n')
logfile = logfile + '.csv'

#LED will illuminate if something detected in # feet
##RED_DISTANCE = 1
##YELLOW_DISTANCE = 3
##GREEN_DISTANCE = 5
##
##RED_DISTANCE = RED_DISTANCE * CM_TO_FEET
##YELLOW_DISTANCE = YELLOW_DISTANCE * CM_TO_FEET
##GREEN_DISTANCE = GREEN_DISTANCE * CM_TO_FEET

#Set up GPIO Pins
TRIGTOP=21
ECHOTOP=20
REDTOP=26
YELLOWTOP=19
GREENTOP=13

GPIO.setup(TRIGTOP,GPIO.OUT)
GPIO.setup(ECHOTOP,GPIO.IN)
##GPIO.setup(REDTOP,GPIO.OUT)
##GPIO.setup(YELLOWTOP,GPIO.OUT)
GPIO.setup(GREENTOP,GPIO.OUT)


TRIGMID=0
ECHOMID=1
REDMID=7
YELLOWMID=8
GREENMID=25

GPIO.setup(TRIGMID,GPIO.OUT)
GPIO.setup(ECHOMID,GPIO.IN)
##GPIO.setup(REDMID,GPIO.OUT)
##GPIO.setup(YELLOWMID,GPIO.OUT)
##GPIO.setup(GREENMID,GPIO.OUT)

TRIGLOW=22
ECHOLOW=23
REDLOW=27
YELLOWLOW=17
GREENLOW=18

GPIO.setup(TRIGLOW,GPIO.OUT)
GPIO.setup(ECHOLOW,GPIO.IN)
##GPIO.setup(REDLOW,GPIO.OUT)
##GPIO.setup(YELLOWLOW,GPIO.OUT)
##GPIO.setup(GREENLOW,GPIO.OUT)

def light_off(RED, YELLOW, GREEN):
   GPIO.output(RED,False)
   GPIO.output(YELLOW,False)
   GPIO.output(GREEN,False)


def sensor_read(TRIG, ECHO, RED, YELLOW, GREEN):
    timeoutTimer = time.time() + 2
    timeout = False
    pulse_start = 0
    pulse_end = 0
    GPIO.output(TRIG,False)
    time.sleep(0.04)
    GPIO.output(TRIG,True)
    time.sleep(0.00001)
    GPIO.output(TRIG,False)
    while GPIO.input(ECHO)==0 and not timeout:
        pulse_start=time.time()
        if timeoutTimer < pulse_start:
            timeout = True
    while GPIO.input(ECHO)==1 and not timeout:
        pulse_end=time.time()
    if not timeout:
        pulse_duration=pulse_end-pulse_start
    else:
        pulse_duration=0
        print('Timeout')
    distance=pulse_duration*17150
    distance=round(distance,2)
    return distance

#while True:

for i in  range(3000):
    GPIO.output(GREENTOP,True)
    top = sensor_read(TRIGTOP, ECHOTOP, REDTOP, YELLOWTOP, GREENTOP)
    mid = sensor_read(TRIGMID, ECHOMID, REDMID, YELLOWMID, GREENMID)
    GPIO.output(GREENTOP, False)
    low = sensor_read(TRIGLOW, ECHOLOW, REDLOW, YELLOWLOW, GREENLOW)
    run = (top, mid, low)
    runs.append(run)
    print(i)

with open(logfile, 'w', newline='') as file:
    writer = csv.writer(file, dialect='excel')
    writer.writerows(runs)

print('Done.')
GPIO.cleanup()
