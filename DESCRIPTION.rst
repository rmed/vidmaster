vidmaster
=========

This script aims to automate the video compositions for the `GULUC3M <http://gul.es/>`_ talks.

**Compatible with Python 2 and 3**, tested with 2.7 and 3.4 .

Dependencies
------------

vidmaster depends on `MoviePy <https://github.com/Zulko/moviepy>`_, if you are installing manually, run:

.. code-block::

    pip install moviepy

MoviePy uses FFmpeg for its operations. If for some reason FFmpeg is not available in your distribution, the ``imageio`` library (dependency from MoviePy) will download a binary and use it.

Due to ``imageio`` limitations, this will not work on Raspberry Pi automatically, so you may have to compile FFmpeg and modify some configurations

Installation
------------

vidmaster is available in the Package Index, simply run:


.. code-block::

    pip install vidmaster

to install vidmaster and its dependencies or download the source and run:

.. code-block::

    python setup.py install

Usage
-----

You can use vidmaster in two ways:

- As an independent program:

.. code-block::

    vidmaster <video script file>

- As a Python module:

.. code-block:: python

    from vidmaster.workbench import start_workbench
    import sys

    if __name__ == "__main__":
        if len(sys.argv) != 2:
            print("Usage: vidmaster.py <video script file>")
            sys.exit()

        workbench = start_workbench(sys.argv[1])

        workbench.build()

Scripting
---------

vidmaster uses a dead simple (and quite silly) scripting language for defining the compositions.

See `Scripting <https://github.com/rmed/vidmaster/wiki/Scripting>`_ for more information on the syntax or `Script example <https://github.com/rmed/vidmaster/wiki/Script-example>`_ for a real example.
