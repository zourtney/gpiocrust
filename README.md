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

The `OutputPin` class controls a single GPIO pin for output. You can set its value to `True` (`1`) or `False` (`0`). That's all there is to it!

    from gpiocrust import Header, OutputPin
    
    with Header() as header:
      shiny_led = OutputPin(11)
      shiny_led.value = True
      ...

`value` defaults to `False`, but you can set it on instantiation like so:

    shiny_led = OutputPin(11, value=True)

**`PWMOutputPin`**

The `PWMOutputPin` class controls a single GPIO pin for output, but allows for variable `value`s via software pulse width modulation.

    from gpiocrust import Header, PWMOutputPin
    
    with Header() as header:
      soft_led = PWMOutputPin(11)
      soft_led.value = 0.25
      ...

You can set the frequency (Hz) via the `frequency` property. For example:

    from gpiocrust import Header, PWMOutputPin
    
    with Header() as header:
      soft_led = PWMOutputPin(11, frequency=100)
      solf_led.frequency = 50

*
**NOTE:** the RPi.GPIO implementation uses duty cycle values from `0` to `100`. To be consistent with `OutputPin`, `PWMOutputPin` uses decimal value `0.0` to `1.0`.*

For a good overview of how to use the [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO) implementation, see [this video](http://youtu.be/uUn0KWwwkq8).