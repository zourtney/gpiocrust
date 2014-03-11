import unittest
from mock import Mock
from nose.tools import assert_equals
from gpiocrust.gpio_mock import InputPin


class InputPinTests(unittest.TestCase):
  """InputPin tests"""
  def setUp(self):
    self.callback = Mock()
    self.pin = InputPin(pin=16, value=0, callback=self.callback)

  def test_exists(self):
    assert isinstance(self.pin, InputPin)

  def test_pin_assignment(self):
    assert_equals(self.pin._pin, 16)

  def test_pin_value(self):
    assert_equals(self.pin.value, 0)

  def test_trigger(self):
    self.pin.trigger(1)
    self.callback.assert_called_with(1)

  # Mock API doesn't have bouncetime built out. So don't test...