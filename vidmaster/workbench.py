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
# from vidmaster.clip_builder import build_image_clip, build_video_clip
from clip_builder import define_audio, define_image, define_video
from clip_builder import do_concatenate, do_composite, export_video
from clip_builder import effect_margin, effect_position, effect_resize
from parser import OpDefine, OpEffect, OpMix, OpExport
from parser import parse_block


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

    def do_ops(self):
        """ Perform the operations stored. """
        for op in self.ops:

            if type(op) == OpDefine:

                if op.type == 'audio':
                    self.clips[op.name] = define_audio(op)

                elif op.type == 'image':
                    self.clips[op.name] = define_image(op)

                elif op.type == 'video':
                    self.clips[op.name] = define_video(op)

                else:
                    raise Exception("Unknown definition type")

            elif type(op) == OpEffect:

                if op.type == 'margin':
                    self.clips[op.out] = effect_margin(
                            self.clips[op.clip], op)

                elif op.type == 'position':
                    self.clips[op.out] = effect_position(
                            self.clips[op.clip], op)

                elif op.type == 'resize':
                    self.clips[op.out] = effect_resize(
                            self.clips[op.clip], op)

                else:
                    raise Exception("Unknown effect type")

            elif type(op) == OpMix:

                affected = []
                for c in op.clips:
                    affected.append(self.clips[c])

                if op.type == 'concatenation':
                    self.clips[op.out] = do_concatenate(affected)

                elif op.type == 'composition':
                    self.clips[op.out] = do_composite(affected,
                            op.height, op.width)

                else:
                    raise Exception("Unknown mix type")

            elif type(op) == OpExport:
                # This is the final operation
                export_video(self.clips[op.clip], op.out,
                        out.fps, out.codec)
                return

            else:
                raise Exception("Unknown operation type")


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
