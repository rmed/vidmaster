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

import os
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
# from vidmaster.clip_builder import build_image_clip, build_video_clip
from clip_builder import build_image_clip, build_video_clip
from parser import parse_block


# class Workbench(object):

#     def __init__(self):
#         # Metadata
#         self.title = None
#         self.desc = None
#         self.fps = 0
#         self.height = 0
#         self.width = 0
#         self.output = None
#         self.codec = None

#         # Intro/outro
#         self.intro = None

#         # Clips
#         self.clips = {}

#         # Composition layers
#         self.composition = []

#     def build(self):
#         """ Build the final video. """
#         # Create main composition
#         print("Creating main composition...")

#         comp_list = []
#         for c in self.composition:
#             comp_list.append(self.clips[c])

#         final = CompositeVideoClip(comp_list, size=(self.width,self.height))

#         # Concatenate intro/outro if any
#         # if self.intro:
#             # print("Adding intro/outro...")
#             # inout = self.clips[self.intro]
#             # final = concatenate_videoclips([inout, final, inout])

#         # Build the video
#         print("Creating final video...")
#         final.write_videofile(
#             self.output,
#             fps=self.fps,
#             codec=self.codec,
#             # Modify these?
#             preset="ultrafast")

class Workbench(object):

    def __init__(self, ops=[], clips={}):
        self.ops = ops
        self.clips = clips


def start_workbench(script):
    """ Initialize the workbench parsing the script file.

        This will return a Workbench object that includes all the
        operations to apply.
    """
    if not os.path.isfile(script):
        raise Exception("Cannot access script")

    wb = Workbench()

    # Parse the script
    with open(script, 'r') as f:
        file_lines = f.read().splitlines()

    while file_lines:
        line = file_lines.pop(0)

        # Check if block
        if line.startswith('#do'):
            block = []
            block.append(line)

            # Read all the block
            while not line.startswith('#end') and file_lines:
                line = file_lines.pop(0)
                if not line or line.startswith('//'):
                    continue
                block.append(line)

            wb.ops.append(parse_block(block))

    return wb

# def start_workbench(config):
#     """ Initialize the workbench parsing the configuration file.

#         This will return a Workbench object that includes all the clips,
#         effects, transitions, etc. applied.
#     """
#     wb = Workbench()

#     # Gather metadata
#     info = config['info']

#     wb.title = info['title']
#     wb.desc = config.get('info' ,'description')
#     wb.fps = int(info['fps'])
#     wb.height = int(info['height'])
#     wb.width = int(info['width'])
#     wb.output = info['output']
#     wb.codec = config.get('info', 'codec')

#     # Build video clips
#     vclips = config['video-clips']

#     for k in vclips:
#         # Get path
#         cpath = vclips[k]

#         # Get info for this clip
#         audio = config.getboolean(k, 'audio')
#         # vfps = int(vclips[k]['vfps'])
#         afps = int(config[k]['afps']) if config.get(k, 'afps') else None
#         start = config.get(k, 'start')
#         end = config.get(k, 'end')

#         # Get effects for this clip
#         ceffects = [config[e] for e in config.keys() if e.strip().startswith(
#             'effect ' + k)]

#         # Build clip
#         clip = build_video_clip(
#             path=cpath,
#             audio=audio,
#             afps=afps,
#             start=start,
#             end=end,
#             effects=ceffects)

#         wb.clips[k] = clip

#     # Build image clips
#     iclips = config['images']

#     for k in iclips:
#         # Get path
#         ipath = iclips[k]

#         # Get duration info
#         duration = int(config[k]['duration']) if config.get(
#             k, 'duration') else None

#         # Get effects for this clip
#         ieffects = [config[e] for e in config.keys() if e.strip().startswith(
#             'effect ' + k)]

#         clip = build_image_clip(
#             path=ipath,
#             duration=duration,
#             effects=ieffects)

#         wb.clips[k] = clip

#         is_intro = config.getboolean(k, 'intro')
#         if is_intro:
#             wb.intro = k

#     # Obtain composition layers (list)
#     layers = config['composition']['layers'].split(' ')
#     wb.composition = layers

#     return wb
