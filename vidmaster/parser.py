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
REGEX_VAR = re.compile('(\w+)\s*=\s*([a-zA-Z0-9_\/.:\s]+)')
BOOL_VARS = ['hasaudio']
INT_VARS = ['duration', 'height', 'width', 'x', 'y', 'size', 'opacity',
    'red', 'green', 'blue', 'fps', 'threads']
TIME_VARS = ['start', 'end']


class OpDefine(object):
    """ Definition of clips. """

    def __init__(self, **kwargs):
        """ Can work with image, video or audio clips.

            name     - name to assign to the clip (overwrites) [required]
            type     - video, audio or image [required]
            source   - absolute path of the source file [required]
            hasaudio - (for video only), whether a clip has audio or not

            For image clips:
                duration      - duration of the clip
                duration_from - set the duration based on the duration
                    of another video clip

                Priority is given to the duration parameter.
        """
        self.name = kwargs['name']
        self.type = kwargs['type']
        self.source = kwargs['source']

        self.hasaudio = kwargs.get('hasaudio', False)

        self.duration = kwargs.get('duration', None)
        self.duration_from = kwargs.get('duration_from', None)


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
                size    - size of the margin
                opacity - opacity of the margin (0-1)
                red     - red color in RGB (0-255)
                green   - green color in RGB (0-255)
                blue    - blue color in RGB (0-255)
        """
        self.clip = kwargs['clip']
        self.type = kwargs['type']
        self.out = kwargs['out']

        self.height = kwargs.get('height', None)
        self.width = kwargs.get('width', None)

        self.x = kwargs.get('x', None)
        self.y = kwargs.get('y', None)

        self.size = kwargs.get('size', None)
        self.opacity = kwargs.get('opacity', None)
        self.red = kwargs.get('red', None)
        self.green = kwargs.get('green', None)
        self.blue = kwargs.get('blue', None)


class OpMix(object):
    """ Mix clips. """

    def __init__(self, **kwargs):
        """ Support for concatenation, composition or mixing audio and video.

            type  - concatenation, composition or audio
            clips - ordered list of affected clips.
                In the case of concatenation, represents the order,
                while for composition represents the layers (0 is left)

            out   - output clip (overwrites)

            For composition:
                height - height of the final composition
                width  - width of the final composition

            For audio mixing:
                audio - audio clip to use for the video
        """
        self.type = kwargs['type']
        self.clips = kwargs.get('clips', "").split()
        self.out = kwargs['out']

        self.height = kwargs.get('height', None)
        self.width = kwargs.get('width', None)

        self.clip = kwargs.get('clip', None)
        self.audio = kwargs.get('audio', None)

class OpExport(object):
    """ Export a clip to a file """

    def __init__(self, **kwargs):
        """ There may be several exports in a script.

            clip    - input clip (usually final composition)
            out     - absolute path for the output file
            fps     - fps value for the final video
            codec   - codec to use for the final video
            preset  - FFMPEG compression preset:
                ultrafast, superfast, fast, medium, slow, superslow.
            threads - number of threads to use for ffmpeg
            params  - additional params for FFMPEG
        """
        self.clip = kwargs['clip']
        self.out = kwargs['out']
        self.fps = kwargs['fps']
        self.codec = kwargs['codec']
        self.preset = kwargs.get('preset', 'medium')
        self.threads = kwargs.get('threads', None)
        self.params = kwargs.get('params', "").split()


class OpSubclip(object):
    """ Create a subclip from the video. """

    def __init__(self, **kwargs):
        """ Params:

            clip - clip to extract a subclip from
            start - timestamp indicating start of the subclip
            end - timestamp indicating end of the subclip. If empty, will
                use end of the original clip.
            out - output clip (overwrites)

            Timestamp has the following format: 01:03:05
        """
        self.clip = kwargs['clip']
        self.start = kwargs['start']
        self.end = kwargs.get('end', None)
        self.out = kwargs['out']


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

        else:
            raise Exception("Invalid boolean value")

    elif var in INT_VARS:
        # Integer
        return int(val)

    elif var in TIME_VARS:
        # Timestamp
        t = val.split(':')
        return (int(t[0]), int(t[1]), int(t[2]))

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

    elif btype in ['concatenate', 'composition', 'setaudio']:
        return parse_mix(lines, btype)

    elif btype == 'export':
        return parse_export(lines)

    elif btype == 'subclip':
        return parse_subclip(lines)

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

def parse_subclip(lines):
    """ Parse a subclip.

        Returns an OpSubclip object.
    """
    kwargs = fill_dict(lines)

    return OpSubclip(**kwargs)
