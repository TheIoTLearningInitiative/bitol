#!/usr/bin/env sh

UDP_PORT=$1

gst-launch-1.0 -v udpsrc port=${UDP_PORT} ! application/x-rtp, media=video, clock-rate=90000, encoding-name=JPEG, payload=26 ! rtpjpegdepay ! jpegdec ! xvimagesink sync=0
