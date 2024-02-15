import threading
from gpiozero import DigitalInputDevice, Robot
from time import sleep

import time
import pigpio

import rotary_encoder

import RPi.GPIO as GPIO
import time
TRIG=21
ECHO=20
GPIO.setmode(GPIO.BCM)

#!/usr/bin/env python

import pigpio

class decoder:

   """Class to decode mechanical rotary encoder pulses."""

   def __init__(self, pi, gpioA, gpioB, callback):

      """
      Instantiate the class with the pi and gpios connected to
      rotary encoder contacts A and B.  The common contact
      should be connected to ground.  The callback is
      called when the rotary encoder is turned.  It takes
      one parameter which is +1 for clockwise and -1 for
      counterclockwise.

      EXAMPLE

      import time
      import pigpio

      import rotary_encoder

      pos = 0

      def callback(way):

         global pos

         pos += way

         print("pos={}".format(pos))

      pi = pigpio.pi()

      decoder = rotary_encoder.decoder(pi, 7, 8, callback)

      time.sleep(300)

      decoder.cancel()

      pi.stop()

      """

      self.pi = pi
      self.gpioA = gpioA
      self.gpioB = gpioB
      self.callback = callback
      self.pos =0

      self.levA = 0
      self.levB = 0

      self.lastGpio = None

      self.pi.set_mode(gpioA, pigpio.INPUT)
      self.pi.set_mode(gpioB, pigpio.INPUT)

      self.pi.set_pull_up_down(gpioA, pigpio.PUD_UP)
      self.pi.set_pull_up_down(gpioB, pigpio.PUD_UP)

      self.cbA = self.pi.callback(gpioA, pigpio.EITHER_EDGE, self._pulse)
      self.cbB = self.pi.callback(gpioB, pigpio.EITHER_EDGE, self._pulse)

   def _pulse(self, gpio, level, tick):

      """
      Decode the rotary encoder pulse.

                   +---------+         +---------+      0
                   |         |         |         |
         A         |         |         |         |
                   |         |         |         |
         +---------+         +---------+         +----- 1

             +---------+         +---------+            0
             |         |         |         |
         B   |         |         |         |
             |         |         |         |
         ----+         +---------+         +---------+  1
      """

      if gpio == self.gpioA:
         self.levA = level
      else:
         self.levB = level;

      if gpio != self.lastGpio: # debounce
         self.lastGpio = gpio

         if   gpio == self.gpioA and level == 1:
            if self.levB == 1:
               self.callback(self,1)
         elif gpio == self.gpioB and level == 1:
            if self.levA == 1:
               self.callback(self,-1)

   def cancel(self):

      """
      Cancel the rotary encoder decoder.
      """

      self.cbA.cancel()
      self.cbB.cancel()
      



def callback(self,way):


    self.pos += way


pi = pigpio.pi()
   
e1 = rotary_encoder.decoder(pi, 23, 24, callback)
   
e2 = rotary_encoder.decoder(pi, 5, 6, callback)
   
#while True:
    #print(f'pos1: {e1.pos}, pos2: {e2.pos}')
    #time.sleep(0.1)
   
   

#time.sleep(300)

#decoder.cancel()

#pi.stop()



def clamp(value):
    return max(min(1, value), 0)

SAMPLETIME = 0.5
TARGET = 200
KP = 0.0001
KD = 0.0005
KI = 0.00005

r = Robot((10,9), (8,7)) 

#m1 is left motor and m2 is right motor

m1_speed = 0
m2_speed = 0
r.value = (m1_speed, m2_speed)

e1_prev_error = 0
e2_prev_error = 0

e1_sum_error = 0
e2_sum_error = 0

xh,yh =0,0
xd,yd = 30,30
totRot1= 0
totRot2 =0

while (xh != xd) and (yh !=yd):
    
    print("distance measurement in progress")
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.output(TRIG,False)
    print ("waiting for sensor to settle")
    time.sleep(0.2)
    GPIO.output(TRIG,True)
    time.sleep(0.00001)
    GPIO.output(TRIG,False)
    while GPIO.input(ECHO)==0:
        pulse_start=time.time()
    while GPIO.input(ECHO)==1:
        pulse_end=time.time()
    pulse_duration=pulse_end-pulse_start
    distance=pulse_duration*17150
    distance=round(distance,2)
    print("distance:",distance,"cm")
    
    if distance <=100:
        TARGET = -50
    else:
        TARGET = 200

    
    while distance <=100:
        TARGET = -50
        e1_error = TARGET + e1.pos
        e2_error = 50 - e2.pos
        m1_speed -= ((e1_error * KP) + (e1_prev_error * KD) + (e1_sum_error * KI))
        m2_speed += (e2_error * KP)  + (e1_prev_error * KD) + (e2_sum_error * KI)

        m1_speed = min(1, m1_speed)
        m2_speed = max(min(1, m2_speed), 0)
        r.value = (m1_speed, m2_speed)
        
        print("e1 {} e2 {}".format(e1.pos, e2.pos))
        print("m1 {} m2 {}".format(m1_speed, m2_speed))
    
        print("m1 {} m2 {}".format(m1_speed, m2_speed))
        
        e1.pos =0 
        e2.pos =0

        sleep(SAMPLETIME)
    
        e1_prev_error = e1_error
        e2_prev_error = e2_error

        e1_sum_error += e1_error
        e2_sum_error += e2_error
        
        print("distance measurement in progress")
        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)
        GPIO.output(TRIG,False)
        print ("waiting for sensor to settle")
        time.sleep(0.2)
        GPIO.output(TRIG,True)
        time.sleep(0.00001)
        GPIO.output(TRIG,False)
        while GPIO.input(ECHO)==0:
            pulse_start=time.time()
        while GPIO.input(ECHO)==1:
            pulse_end=time.time()
        pulse_duration=pulse_end-pulse_start
        distance=pulse_duration*17150
        distance=round(distance,2)
        print("distance:",distance,"cm")


    e1_error = TARGET - e1.pos
    e2_error = TARGET - e2.pos

    m1_speed += (e1_error * KP) + (e1_prev_error * KD) + (e1_sum_error * KI)
    m2_speed += (e2_error * KP)  + (e1_prev_error * KD) + (e2_sum_error * KI)

    m1_speed = max(min(1, m1_speed), 0)
    m2_speed = max(min(1, m2_speed), 0)
    r.value = (m1_speed, m2_speed)

    print("e1 {} e2 {}".format(e1.pos, e2.pos))
    print("m1 {} m2 {}".format(m1_speed, m2_speed))
    
    print("m1 {} m2 {}".format(m1_speed, m2_speed))
    
    totRot1+=e1.pos
    totRot2+= e2.pos
    
    if (totRot1>=300) and (totRot2>=300):
        xh+=1
        yh+=1
        totRot1= 0
        totRot2 =0

    print("xh {} yh {}".format(xh, yh))

    e1.pos =0 
    e2.pos =0

    sleep(SAMPLETIME)

    e1_prev_error = e1_error
    e2_prev_error = e2_error

    e1_sum_error += e1_error
    e2_sum_error += e2_error
