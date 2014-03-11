gpiocrust
=========

A simple object-oriented wrapper around the Raspberry Pi's [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO) library. An encrusting, if you will.

**This is a work in progress.** The goal is a consise, [pythonic](http://stackoverflow.com/a/58992/311207) API for the Raspberry Pi's general purpose I/O pins. I welcome all suggestions, contributions, and half-hearted insults.

Usage
-----

**Header**

The `Header` class just wraps the GPIO setup and teardown methods. Most importantly, it ensures that `GPIO.cleanup()` is called. For example:

    from gpiocrust import Header

    with Header() as header:
      # Application logic goes here
      pass

    # All cleaned up now.
    
**OutputPin**

The `OutputPin` class controls a single GPIO pin for output. You can set its value to `True` (`1`) or `False` (`0`). That's all there is to it!

    from gpiocrust import Header, OutputPin
    
    with Header() as header:
      shiny_led = OutputPin(11)
      shiny_led.value = True
      ...

`value` defaults to `False`, but you can set it on instantiation like so:

    shiny_led = OutputPin(11, value=True)

**PWMOutputPin**

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

**NOTE:** the RPi.GPIO implementation uses duty cycle values from `0` to `100`. To be consistent with `OutputPin`, `PWMOutputPin` uses decimal values `0.0` to `1.0`.

For a good overview of how to use the [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO) implementation, see [this video](http://youtu.be/uUn0KWwwkq8).

**InputPin**

The `InputPin` class controls a single GPIO pin for input. You can watch for edge events using a `callback` argument or via the `@change` decorator. For now, `InputPin` only supports watching `GPIO.BOTH` (rising and falling) events.

    from gpiocrust import Header, InputPin

    def alert_president(value):
      pass

    with Header() as header:
      the_red_button = InputPin(11, callback=alert_president)

Using the `@change` decorator is recommended.

    from gpiocrust import Header, InputPin

    with Header() as header:
      the_red_button = InputPin(11, value=0)

      @the_red_button.change
      def take_action(value):
        pass

Mock API
--------
Mock classes are included that mimick the native GPIO functionality. The library falls back to mock objects when the `RPi.GPIO` package cannot be loaded. This allows one to code the general I/O flow of an application in development environments where running code on a physical Raspberry Pi is inconvenient or impossible.

Fallback is automatic, so your import statements will look just as before.

OutputPin example
-----------------

    import time
    from gpiocrust import Header, OutputPin, PWMOutputPin

    with Header() as header:
      pin11 = OutputPin(11)
      pin15 = PWMOutputPin(15, frequency=100, value=0)
  
      try:
        while 1:
          # Going up
          pin11.value = True
    
          for i in range(100):
            pin15.value = i / 100.0
            time.sleep(0.01)
    
          time.sleep(0.5)
    
          # Going down
          pin11.value = False
          
          for i in range(100):
            pin15.value = (100 - i) / 100.0
            time.sleep(0.01)
          
          time.sleep(0.5)
      except KeyboardInterrupt:
        pass