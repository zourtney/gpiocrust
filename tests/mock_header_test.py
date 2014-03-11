import unittest
from mock import Mock
from gpiocrust.gpio_mock import Header


class HeaderTests(unittest.TestCase):
  def setUp(self):
    self.header = Header()

  def test_exists(self):
    assert isinstance(self.header, Header)

def test_header_with_block_usage():
  old_enter = Header.__enter__; Header.__enter__ = Mock()
  old_exit = Header.__exit__; Header.__exit__ = Mock()

  header = Header()
  with header as h:
    pass

  header.__enter__.assert_called_with()
  Header.__enter__ = old_enter
  
  header.__exit__.assert_called_with(None, None, None)
  Header.__exit__ = old_exit