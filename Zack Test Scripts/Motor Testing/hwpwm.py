import pigpio
import time

GPIO = pigpio.pi()
freqset = 0
dutyset = 0
reverse = 2

while freqset == 0:
    try:
        freq=input('Frequency?')
        freq=int(freq)
        freqset = 1
    except ValueError:
        print('Not an integer, try again.')
while dutyset == 0:
    try:
        duty=input('duty?')
        duty=int(duty)
        dutyset = 1
    except ValueError:
        print('Not an integer, try again.')
while reverse not in {0, 1}:
    try:
        reverse = input('forward(1) or back(0)?')
        reverse = int(reverse)
    except ValueError:
        print('Not an integer, try again.')

                       
duty=duty*10000
print(duty)

#
# pigpio uses BROADCOM PIN NUMBERING !!!
#

PWML = 12 # Physical Pin #32
PWMR = 13 # Physical Pin #33
RevL = 5  # Physical Pin #29
RevR = 6  # Physical Pin #31
          # Phyiscal pins 30 and 34 are ground


# Set the GPIO-Mode to ALT5 for HW-PWM
GPIO.set_mode(PWML, pigpio.ALT5)
GPIO.set_mode(PWMR, pigpio.ALT5)
GPIO.set_mode(RevL, pigpio.OUTPUT)
GPIO.set_mode(RevR, pigpio.OUTPUT)
GPIO.write(RevL,reverse)
GPIO.write(RevR,reverse)

# Start the signal geaneration
# 
GPIO.hardware_PWM(PWML, freq, duty)
GPIO.hardware_PWM(PWMR, freq, duty)

try:
        # Keep the script running until Ctrl + C are pressed
        while True:
            dutyset = 0
            while dutyset == 0:
                try:
                    duty=input('duty?')
                    duty=int(duty)
                    dutyset = 1
                except ValueError:
                    print('Not an integer, try again.')
            duty=duty*10000
            GPIO.hardware_PWM(PWMR, freq, duty)
            GPIO.hardware_PWM(PWML, freq, duty)
except KeyboardInterrupt:
        pass

# Pull down the GPIO-Pin and cleanup with stop()
GPIO.write(PWMR, 0)
GPIO.write(PWML, 0)
GPIO.write(RevL,0)
GPIO.write(RevR,0)
GPIO.stop()
