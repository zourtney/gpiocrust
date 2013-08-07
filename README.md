gpiocrust
=========

A simple object-oriented wrapper around the Raspberry Pi's [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO) library. An encrusting, if you will.

**This is a work in progress.** The goal is a consise, [pythonic](http://stackoverflow.com/a/58992/311207) API for the Raspberry Pi's general purpose I/O pins. I welcome all suggestions, contributions, and half-hearted insults.

Usage
-----

**`Header`**

The `Header` class just wraps the GPIO setup and teardown methods. Most importantly, it ensures that `GPIO.cleanup()` is called. For example:

    from gpiocrust import Header

    with Header() as header
      # Application logic goes here
      pass

    # All cleaned up now.
    
**`OutputPin`**

The `OutputPin` is controls a single GPIO pin for output. You can set its value to `True` (`1`) or `False` (`0`). That's all there is to it!

    from gpiocrust import Header, OutputPin
    
    with Header() as header:
      shiny_led = OutputPin(11)
      shiny_led.value = True

`value` defaults to `False`, but you can set it on instantiation like so:

    shiny_led = OutputPin(11, value=True)

**`PWMOutputPin`**

