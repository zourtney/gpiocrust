import unittest

from nose.tools import assert_equals, assert_not_equals

from gpiocrust.gpio_mock import OutputPin, PWMOutputPin


class OutputPinBase(object):
    """Shared, testable functionality between OutputPin and PWMOutputPin"""

    def test_default_value(self):
        assert_equals(self.pin.value, 0)

    def test_pin(self):
        assert_equals(self.pin._pin, 16)

    def test_pin_assignment(self):
        assert_equals(self.pin.value, 0)
        self.pin.value = 1
        assert_equals(self.pin.value, 1)


class OutputPinTests(unittest.TestCase, OutputPinBase):
    """OutputPin-specific tests"""

    def setUp(self):
        self.pin = OutputPin(pin=16)

    def test_exists(self):
        assert isinstance(self.pin, OutputPin)

    def test_pin_assignment_iffy_values(self):
        self.pin.value = 0.9
        assert_not_equals(self.pin.value, 0.9)
        self.pin.value = 1.1
        assert_not_equals(self.pin.value, 1.1)


class PWMOutputPinTests(unittest.TestCase, OutputPinBase):
    """PWMOutputPin-specific tests"""

    def setUp(self):
        self.pin = PWMOutputPin(pin=16)

    def test_exists(self):
        assert isinstance(self.pin, PWMOutputPin)

        # Mock API does no bounds checking, so no need to test values. These are
        # floats, so pretty much everything will pass...

# Stragglers
def test_pin_kwargs():
    pin = OutputPin(pin=15, value=1)
    assert_equals(pin._pin, 15)
    assert_equals(pin.value, 1)

def test_pwm_pin_kwargs():
    pin = PWMOutputPin(pin=15, value=0.4)
    assert_equals(pin._pin, 15)
    assert_equals(pin.value, 0.4)
