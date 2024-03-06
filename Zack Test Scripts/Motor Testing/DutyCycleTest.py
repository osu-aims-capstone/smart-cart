import RPi.GPIO as IO
IO.setmode (IO.BCM)
IO.setup(6,IO.OUT)
freq = input('Frequncy?\n')
freq = int(freq)
duty = 100
p = IO.PWM(6,freq)
p.start(duty)
while True:
    duty = input('Duty Cycle?\n')
    duty = int(duty)
    p.ChangeDutyCycle(duty)
