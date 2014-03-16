gpiocrust
=========

.. image:: http://travis-ci.org/zourtney/gpiocrust.png?branch=dev
         :target: http://travis-ci.org/zourtney/gpiocrust

A concise, pythonic wrapper around the Raspberry Pi’s `RPi.GPIO`_
library. An encrusting, if you will.

With (almost silent) fallback to mock objects, you can prototype pin I/O locally on your favorite computer, even when your Pi is on the other side of town. See *Mock API* for more details.

In a nutshell
-------------

Installation with pip is a snap:

.. code:: bash

    pip install gpiocrust

Coding pin I/O couldn't be easier -- open up a Python file and start coding! Here's a bare-bones example that will turn GPIO pin 15 on:

.. code:: python

    from gpiocrust import Header, OutputPin

    with Header() as header:
      pin = OutputPin(15, value=0)
      pin.value = 1

Classes
-------

**Header**

The ``Header`` class just wraps the GPIO setup and teardown methods.
Most importantly, it ensures that ``GPIO.cleanup()`` is called. For
example:

.. code:: python

    from gpiocrust import Header

    with Header() as header:
      # Application logic goes here
      pass

    # All cleaned up now.

**OutputPin**

The ``OutputPin`` class controls a single GPIO pin for output. Set its
value to ``True`` (``1``) or ``False`` (``0``). That’s all there is to
it!

.. code:: python

    from gpiocrust import Header, OutputPin

    with Header() as header:
      shiny_led = OutputPin(11)
      shiny_led.value = True
      ...

``value`` defaults to ``False``, but can be set with a keyword argument.

.. code:: python

    shiny_led = OutputPin(11, value=True)

**PWMOutputPin**

The ``PWMOutputPin`` class controls a single GPIO pin for output, but
allows for variable ``value``\ s via software pulse width modulation.

.. code:: python

    from gpiocrust import Header, PWMOutputPin

    with Header() as header:
      soft_led = PWMOutputPin(11)
      soft_led.value = 0.25
      ...

You can set the frequency (Hz) via the ``frequency`` property. For
example:

.. code:: python

    from gpiocrust import Header, PWMOutputPin

    with Header() as header:
      soft_led = PWMOutputPin(11, frequency=100)
      soft_led.frequency = 50

**NOTE:** the RPi.GPIO implementation uses duty cycle values from ``0``
to ``100``. To be consistent with ``OutputPin``, ``PWMOutputPin`` uses
decimal values ``0.0`` to ``1.0``.

For a good overview of how to use the `RPi.GPIO`_ implementation, see
`this video`_.

**InputPin**

The ``InputPin`` class controls a single GPIO pin for input. You can
watch for edge events using a ``callback`` argument or via the
``@change`` decorator. For now, ``InputPin`` only supports watching
``GPIO.BOTH`` (rising *and* falling) events.

.. code:: python

    from gpiocrust import Header, InputPin

    def alert_president(value):
      pass

    with Header() as header:
      the_red_button = InputPin(11, callback=alert_president)

It’s even cleaner with the ``@change`` decorator.

.. code:: python

    from gpiocrust import Header, InputPin

    with Header() as header:
      the_red_button = InputPin(11, value=0)

      @the_red_button.change
      def alert_president(value):
        pass

Mock API
--------

Mock classes are included that mimick the native GPIO functionality. The
library falls back to mock objects when the ``RPi.GPIO`` package cannot
be loaded. This allows one to code the general I/O flow of an
application in development environments where running code on a physical
Raspberry Pi is inconvenient or impossible (i.e, the computer you're 
reading this on).

Fallback is automatic, so your import statements will look just as
before.

OutputPin example
-----------------

.. code:: python

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


.. _RPi.GPIO: https://pypi.python.org/pypi/RPi.GPIO
.. _this video: http://youtu.be/uUn0KWwwkq8
