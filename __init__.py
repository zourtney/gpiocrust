"""
Object oriented wrapper around RPi.GPIO. A work in progress.

(zourtney, August 2013)
"""

import RPi.GPIO as GPIO


class Header(object):
  """Controls initializing and cleaning up GPIO header."""
  def __init__(self):
    GPIO.setmode(GPIO.BOARD)
  def __del__(self):
    GPIO.cleanup()
  def __enter__(self):
    pass
  def __exit__(self, type, value, traceback):
    pass



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
      self._frequency = float(value)   # No GetFrequency API provided, so store it
      self._pulse.ChangeFrequency(value)

  @property
  def value(self):
    return self._value
  @value.setter
  def value(self, value):
    self._value = float(value)         # No GetDutyCycle API provided, so store it too
    self._pulse.ChangeDutyCycle(self._value * 100.0)