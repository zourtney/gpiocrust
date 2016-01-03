"""An object-oriented wrapper around RPi.GPIO"""

import RPi.GPIO as GPIO
import gpiocrust.edges as edges
from gpiocrust.pin_mode import PinMode

_edge_to_rpi_edge = {
    edges.RISING: GPIO.RISING,
    edges.FALLING: GPIO.FALLING,
    edges.BOTH: GPIO.BOTH,
}

_pinmode_to_rpi_mode = {
    PinMode.BCM: GPIO.BCM,
    PinMode.BOARD: GPIO.BOARD
}

class Header(object):
    """Controls initializing and cleaning up GPIO header."""
    
    def __init__(self, mode=PinMode.BOARD):
        self._pinsForCleanup = []
        GPIO.setmode(_pinmode_to_rpi_mode[mode])

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        GPIO.cleanup()
        for pin in self._pinsForCleanup:
            pin.cleanup()
    
    def registerPinForCleanup(self, pin):
        self._pinsForCleanup.append(pin)


class OutputPin(object):
    """A single GPIO pin set for output"""

    def __init__(self, pin, value=0):
        self._pin = int(pin)
        GPIO.setup(self._pin, GPIO.OUT, initial=value)

    @property
    def value(self):
        return GPIO.input(self._pin)

    @value.setter
    def value(self, val):
        GPIO.output(self._pin, int(val))


class PWMOutputPin(OutputPin):
    """
    A single pulse width modulated output pin.

    Note: duty cycle values are controlled via the `value` property and range in
    value from 0.0 to 1.0, NOT 0 to 100.
    """

    def __init__(self, pin, frequency=50.0, value=0.0):
        super(PWMOutputPin, self).__init__(pin)
        self._frequency = frequency
        self._value = value
        self._pulse = GPIO.PWM(self._pin, frequency)
        self._pulse.start(self._value)

    def __del__(self):
        self._pulse.stop()

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        self._frequency = float(
            value)  # No GetFrequency API provided, so store it
        self._pulse.ChangeFrequency(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = float(
            value)  # No GetDutyCycle API provided, so store it too
        self._pulse.ChangeDutyCycle(self._value * 100.0)


class InputPin(object):
    """A single GPIO pin set for input"""

    def __init__(self, pin, value=0, callback=None, edge=edges.BOTH,
                 bouncetime=0, header=None):
        self._pin = int(pin)
        self._edge = _edge_to_rpi_edge[edge]
		self._header = header
        GPIO.setup(self._pin, GPIO.IN,
                   pull_up_down=GPIO.PUD_DOWN if value == 0 else GPIO.PUD_UP)
        GPIO.add_event_detect(self._pin, self._edge,
                              bouncetime=bouncetime)
        if callback is not None:
            GPIO.add_event_callback(self._pin, callback)
        if header != None:
            header.registerPinForCleanup(self)
    
    def __del__(self):
        if (self._header == None):
            self.cleanup()
    
    def cleanup(self):
        GPIO.remove_event_detect(self._pin)

    @property
    def value(self):
        return GPIO.input(self._pin)

    def change(self, fn, edge=edges.BOTH):
        """Allow for `@change` decorator"""

        def wrapped(pin):
            fn(self.value)

        GPIO.add_event_callback(self._pin, wrapped, _edge_to_rpi_edge[edge])

    def wait_for_edge(self):
        """
        This will remove remove any callbacks you might have specified
        """
        GPIO.remove_event_detect(self._pin)
        GPIO.wait_for_edge(self._pin, self._edge)
