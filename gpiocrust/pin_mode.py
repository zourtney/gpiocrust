from enum import Enum

"""
An enumeration representing the different PIN numbering schemes supported
by GPIO.
"""
class PinMode(Enum):
    BCM = 1
    BOARD = 2
