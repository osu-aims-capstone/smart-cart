import pigpio
GPIO = pigpio.pi()

GPIO.write(19, 0)
GPIO.write(18, 0)
GPIO.stop()
