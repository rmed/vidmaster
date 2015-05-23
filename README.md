# vidmaster

This script aims to automate the video compositions for the [GULUC3M](http://gul.es) talks.

**Compatible with Python 2 and 3**, tested with 2.7 and 3.4 .

## Dependencies

vidmaster depends on [MoviePy](https://github.com/Zulko/moviepy), install with pip (plus its dependencies):

```
$ pip install moviepy
```

MoviePy uses FFmpeg for its operations. If for some reason FFmpeg is not available in your distribution, the `imageio` library (dependency from MoviePy) will download a binary and use it.

Due to `imageio` limitations, this will not work on Raspberry Pi automatically, so you may have to compile FFmpeg and modify some configurations

## Usage

You can use vidmaster in two ways:

- As an independent program:

```
python vidmaster/vidmaster.py <video script file>
```

- As a Python module:

```python
from vidmaster.workbench import start_workbench
import sys

# Can also be executed independently
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: vidmaster.py <video script file>")
        sys.exit()

    workbench = start_workbench(sys.argv[1])

    workbench.build()
```

## Scripting

vidmaster uses a dead simple (and quite silly) scripting language for defining the compositions.

See [Scripting](https://github.com/rmed/vidmaster/wiki/Scripting) for more information on the syntax or [Script example](https://github.com/rmed/vidmaster/wiki/Script-example) for a real example.