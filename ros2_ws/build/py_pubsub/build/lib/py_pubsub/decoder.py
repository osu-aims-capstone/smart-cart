import pigpio

class Decoder:

    """Class to decode mechanical rotary encoder pulses."""

    def __init__(self, pi, gpioA, gpioB, callback):

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


        if gpio == self.gpioA:
            self.levA = level
        else:
            self.levB = level

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