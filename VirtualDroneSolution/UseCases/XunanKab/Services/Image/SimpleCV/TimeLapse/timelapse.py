#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================
# Libraries
# =============================================================================

import argparse
import os
import random
import sys
import time

import SimpleCV

# =============================================================================
# Functions
# =============================================================================

# None

# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='commands')
    parser.add_argument('--frames', type=int)
    parser.add_argument('--interval', type=float)
    parser.add_argument('--fps', type=int)
    args = parser.parse_args()

    frames = args.frames
    interval = args.interval
    fps = args.fps

    cam = SimpleCV.Camera()

    for i in range(0, frames):
	print "\033[F{} :: {}s left".format(i + 1, interval * (frames - i)) 
	img = cam.getImage()
	img.save("img-{}.png".format(i))
	time.sleep(interval)

    os.system("ffmpeg -framerate {} -i img-%d.png timelapse.mp4".format(fps))
