# GStreamer

## Build

```sh
$ docker build -t xe1gyq/gstreamer .
```

## Run

```sh
$ docker run -it --device /dev/video0 xe1gyq/gstreamer
```

## Format

### x-h264

```sh
$ gst-launch-1.0 v4l2src ! video/x-h264,width=1280,height=720,framerate=30/1 ! h264parse config-interval=1 ! matroskamux streamable=true ! tcpserversink host=::0 port=5000 sync=false sync-method=2
```

### x-rtp

```sh
$ gst-launch-1.0 -v udpsrc port=5600 ! application/x-rtp, media=video, clock-rate=90000, encoding-name=JPEG, payload=26 ! rtpjpegdepay ! jpegdec ! xvimagesink sync=0
$ gst-launch-1.0 udpsrc port=5600 caps='application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264' ! rtph264depay ! avdec_h264 ! autovideosink fps-update-interval=1000 sync=false
```
### x-raw

```sh
$ gst-launch-1.0 videotestsrc ! video/x-raw,width=640,height=480 ! videoconvert ! x264enc ! rtph264pay ! udpsink host=172.17.0.1 port=5600
$ gst-launch-1.0 v4l2src ! video/x-raw,width=640,height=480 ! x264enc ! rtph264pay ! udpsink host=172.0.0.1 port=5600
```
