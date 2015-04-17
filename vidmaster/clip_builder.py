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


from moviepy.video.VideoClip import ImageClip
from moviepy.video.io.VideoFileClip import VideoFileClip
import moviepy.video.fx.all as vfx

import os

def build_image_clip(path, duration):
    """ Build a static image clip for composition with params:

        path -- the path to the file
        duration -- duration in seconds

        If no duration is specified, the clip will have infinite
        duration.

        This is mainly used for intro/outro and static background
    """
    print("Building clip for image file '%s'..." % path)
    # Base
    clip = ImageClip(path, duration=duration)

    return clip

def build_video_clip(path, audio, afps, start, end, effects):
    """ Build a video clip for later composition with the following params:

        path    -- the path to the file
        audio   -- whether the clip has audio or not
        afps    -- fps of the audio clip
        start   -- start of the clip
        end     -- end of the clip
        effects -- list of effects to apply

        start and end are used for defining the final subclip that will
        be used for composition. If these values are not specified, all
        the clip will be used

        Returns a VideoFileClip object
    """
    print("Building clip for video file '%s'..." % path)
    # Base
    clip = VideoFileClip(path, audio=audio, audio_fps=afps).subclip(
        start or 0, end)

    # Add effects
    for e in effects:
        print("Applying %s..." % e.name)

        if e['type'] == 'margin':
            clip = clip.fx(vfx.margin, mar=int(e['size']))

        elif e['type'] == 'position':
            clip = clip.set_position((int(e['x']),int(e['y'])))

        elif e['type'] == 'resize':
            clip = clip.fx(
                vfx.resize,
                height=int(e['height']),
                width=int(e['width']))

    return clip
