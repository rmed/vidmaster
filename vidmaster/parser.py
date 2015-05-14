# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2015 Rafael Medina García
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re

# REGEX_VAR = re.compile('(\w+)\s*=\s*(\w+)')
REGEX_VAR = re.compile('(\w+)\s*=\s*([a-zA-Z0-9_\/]+)')
BOOL_VARS = ['hasaudio']
INT_VARS = ['duration', 'height', 'width', 'x', 'y', 'size',
    'red', 'green', 'blue', 'fps']


class OpDefine(object):
    """ Definition of clips. """

    def __init__(self, **kwargs):
        """ Can work with image, video or audio clips.

            name     - name to assign to the clip (overwrites) [required]
            type     - video, audio or image [required]
            source   - absolute path of the source file [required]
            hasaudio - (for video only), whether a clip has audio or not
            duration - duration of the clip
        """
        self.name = kwargs['name']
        self.type = kwargs['type']
        self.source = kwargs['source']

        self.hasaudio = kwargs.get('hasaudio', False)
        self.duration = kwargs.get('duration', None)


class OpEffect(object):
    """ Apply effects to clips. """

    def __init__(self, **kwargs):
        """ Applies to resize, position and margin.

            clip - clip to apply the effect to
            type - resize, position or margin
            out  - name of the resulting clip after the effect (overwrites)

            Resize:
                height - new height for the clip
                width  - new width for the clip

            Position:
                x - new x position for the clip
                y - new y position for the clip

            Margin:
                size  - size of the margin
                red   - red color in RGB (0-255)
                green - green color in RGB (0-255)
                blue  - blue color in RGB (0-255)
        """
        self.clip = kwargs['clip']
        self.type = kwargs['type']
        self.out = kwargs['out']

        self.height = kwargs.get('height', None)
        self.width = kwargs.get('width', None)

        self.x = kwargs.get('x', None)
        self.y = kwargs.get('y', None)

        self.size = kwargs.get('size', None)
        self.red = kwargs.get('red', None)
        self.green = kwargs.get('green', None)
        self.blue = kwargs.get('blue', None)


class OpMix(object):
    """ Mix clips. """

    def __init__(self, **kwargs):
        """ Support for concatenation or composition.

            clips - ordered list of affected clips.
                In the case of concatenation, represents the order,
                while for composition represents the layers (0 is left)

            out   - output clip (overwrites)
        """
        self.clips = kwargs['clips']
        self.out = kwargs['out']


class OpExport(object):
    """ Final export. There can be only one object of this class. """

    def __init__(self, **kwargs):
        """ Should be last operation performed.

            clip   - input clip (usually final composition)
            out    - absolute path for the output file
            fps    - fps value for the final video
            height - height of the final video
            width  - width of the final video
            codec  - codec to use for the final video
        """
        self.clip = kwargs['clip']
        self.out = kwargs['out']
        self.fps = kwargs['fps']
        self.height = kwargs['height']
        self.width = kwargs['width']
        self.codec = kwargs['codec']


def get_val(var, val):
    """ Return the appropriate value for a given variable.

        This may be a string, a number or a boolean.
    """
    if var in BOOL_VARS:
        # Boolean
        if val == "1":
            return True

        elif val == "0":
            return False

    elif var in INT_VARS:
        # Integer
        return int(val)

    # Regular string
    return val

def fill_dict(lines):
    """ Return a dict that can be used as parameter for the operation
        objects.
    """
    kwargs = {}

    for line in lines:
        # Skip comments
        if not line or line.startswith('//'):
            continue

        match = REGEX_VAR.match(line).groups()
        kwargs[match[0]] = get_val(*match)

    return kwargs

def parse_block(lines):
    """ Parse a given block of code.

        lines - information stored within the block
    """
    # Remove first and list lines of the block
    btype = lines.pop(0).lstrip('#do').strip()
    lines.pop(-1)

    if btype == 'define':
        return parse_define(lines)

    elif btype in ['resize', 'position', 'margin']:
        return parse_effect(lines, btype)

    elif btype in ['concatenate', 'composition']:
        return parse_mix(lines, btype)

    elif btype == 'export':
        return parse_export(lines)

def parse_define(lines):
    """ Parse a clip definition.

        Returns an OpDefine object.
    """
    kwargs = fill_dict(lines)

    return OpDefine(**kwargs)

def parse_effect(lines, btype):
    """ Parse an effect.

        Returns an OpEffect object.
    """
    kwargs = fill_dict(lines)

    kwargs['type'] = btype

    return OpEffect(**kwargs)

def parse_export(lines):
    """ Parse the final clip export.

        Returns and OpExport object.
    """
    kwargs = fill_dict(lines)

    return OpExport(**kwargs)

def parse_mix(lines, btype):
    """ Parse a clip mixing.

        Returns an OpMix object.
    """
    kwargs = fill_dict(lines)

    kwargs['type'] = btype

    return OpMix(**kwargs)
