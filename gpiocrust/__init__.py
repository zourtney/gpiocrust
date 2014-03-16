"""
Object oriented wrapper around RPi.GPIO. Falls back to mock objects if RPi.GPIO
is not found.
"""

try:
  import RPi.GPIO
  from .raspberry_pi import *
except:
  print('--------------------------------------------------------------------')
  print(' WARNING: RPi.GPIO library not found. Falling back to mock objects. ')
  print('--------------------------------------------------------------------')
  from .gpio_mock import *