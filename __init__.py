"""
Object oriented wrapper around RPi.GPIO. A work in progress.

(zourtney, August 2013)
"""

try:
  import RPi.GPIO
  from raspberry_pi import *
except:
  print '--------------------------------------------------------------------'
  print ' WARNING: RPi.GPIO library not found. Falling back to mock objects. '
  print '--------------------------------------------------------------------'
  from mock import *