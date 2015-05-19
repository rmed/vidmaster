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


from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.tools.cuts import find_video_period
from moviepy.video.VideoClip import ImageClip
from moviepy.video.io.VideoFileClip import VideoFileClip
import moviepy.video.fx.all as vfx

import os


def define_audio(op):
    """ Define an audio clip from source file.

        source - absolute path to the file
    """
    clip = AudioFileClip(op.source)

    return clip

def define_image(op, ext_duration=None):
    """ Define a static image clip from source file.

        source   - absolute path to the file
        duration - duration in seconds
        ext_duration - clip to obtain the duration from

        Mainly used for intro/outro and static background.
    """
    if ext_duration:
        # clip = ImageClip(op.source, duration=find_video_period(ext_duration))
        clip = ImageClip(op.source, duration=ext_duration.duration)

    else:
        clip = ImageClip(op.source, duration=op.duration)

    return clip

def define_video(op):
    """ Define a video clip from source file.

        source   - absolute path to the file
        hasaudio - whether the clip has its own audio or not
    """
    clip = VideoFileClip(op.source, audio=op.hasaudio)

    return clip

def do_concatenate(clips):
    """ Concatenate clips into one.

        clips - ordered list of clips to concatenate
    """
    result = concatenate_videoclips(clips)

    return result

def do_composite(clips, height, width):
    """ Create a composition of clips.

        clips  - list of clips to composite ordered by layer
        height - height of the final composition
        width  - width of the final composition
    """
    result = CompositeVideoClip(clips, size=(width, height))

    return result

def do_set_audio(clip, audio):
    """ Set the audio of a video clip.

        clip  - clip in which to set the audio
        audio - audio clip to use as audio
    """
    result = clip.set_audio(audio)

    return result

def do_subclip(clip, op):
    """ Create a subclip.

        clip - original clip to create a subclip from
        start - timestamp indicating start of the clip
        end - timestamp indicating end of the clip, or None in order
            to use end of original clip
    """
    result = clip.subclip(op.start, op.end)

    return result

def effect_margin(clip, op):
    """ Add a margin to a clip (video or image).

        clip    - clip to apply the effect to
        size    - size of the margin
        opacity - opacity of the clip
        red     - amount of red for the color of the margin
        green   - amount of green for the color of the margin
        blue    - amount of blue for the color of the margin
    """
    result = clip.fx(vfx.margin, mar=op.size,
            color=(op.red, op.green, op.blue), opacity=op.opacity)

    return result

def effect_position(clip, op):
    """ Apply a position effect to a clip (video or image).

        clip - clip to apply the effect to
        x    - new X position for the clip
        y    - new Y position for the clip
    """
    result = clip.set_position((op.x, op.y))

    return result

def effect_resize(clip, op):
    """ Apply a resize effect to a clip (video or image).

        clip   - clip to apply the effect to
        height - new height for the clip
        width  - new width for the clip
    """
    result = clip.fx(vfx.resize, height=op.height, width=op.width)

    return result

def export_video(clip, op):
    """ Export the clip to a file.

        clip   - clip to export
        out    - absolute path to the resulting file
        fps    - frames per second for the video
        codec  - codec to use for encoding
    """
    clip.write_videofile(
            op.out,
            fps=op.fps,
            codec=op.codec,
            preset=op.preset,
            threads=op.threads,
            ffmpeg_params=op.params)
