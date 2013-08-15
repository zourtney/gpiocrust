"""
A mock API for when RPi.GPIO is not available. Useful for building out
applications while not on the Pi itself.

(zourtney, August 2013)
"""

class Header(object):
  def __init__(self):
    pass
  def __del__(self):
    pass
  def __enter__(self):
    pass
  def __exit__(self, type, value, traceback):
    pass



class OutputPin(object):
  def __init__(self, pin, value=0):
    self._pin = int(pin)
    self._value = value

  @property
  def value(self):
    return self._value
  @value.setter
  def value(self, val):
    self._value = int(val)



class PWMOutputPin(OutputPin):
  def __init__(self, pin, frequency=50.0, value=0.0):
    super(PWMOutputPin, self).__init__(pin)
    self._frequency = frequency
    self._value = value
    self._pulse = frequency

  def __del__(self):
    pass

  @property
  def frequency(self):
      return self._frequency
  @frequency.setter
  def frequency(self, value):
      self._frequency = float(value)

  @property
  def value(self):
    return self._value
  @value.setter
  def value(self, value):
    self._value = float(value)



class InputPin(object):
  def __init__(self, pin, value=0, callback=None, bouncetime=0):
    self._pin = int(pin)
    self._value = value
    self._callback = callback
    #TODO: bouncetime  -->  self._bouncetime = bouncetime

  def __del__(self):
    pass

  @property
  def value(self):
    return self._value
  
  def change(self, fn):
    def wrapped(pin):
      fn(self.value)
    #TODO: finish

  def trigger(self, value):
    #TODO: bouncetime
    self._callback(value)