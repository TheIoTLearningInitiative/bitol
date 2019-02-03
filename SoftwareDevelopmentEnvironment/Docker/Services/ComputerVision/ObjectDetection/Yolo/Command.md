- https://github.com/xe1gyq/Real_time_Object_detection_and_tracking

```sh
$ gst-launch-1.0 -v v4l2src device=/dev/video0 ! image/jpeg,width=640, height=480, framerate=30/1 ! rtpjpegpay ! udpsink host=127.0.0.1 port=5000
```

```sh
$ docker run -it -e DISPLAY=:0 -v /tmp/.X11-unix:/tmp/.X11-unix --device /dev/video0 -p 5001:5000/udp xe1gyq/yolo
```

```sh
$ bash main.sh quintanaroo 5000 172.17.0.1 5100
```

```sh
$ gst-launch-1.0 -v udpsrc port=5100 ! application/x-rtp, media=video, clock-rate=90000, encoding-name=JPEG, payload=26 ! rtpjpegdepay ! jpegdec ! xvimagesink sync=0
```

## Inputs

```
#command='udpsrc port=%s ! application/x-rtp, encoding-name=JPEG, payload=26 ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink' % streamport
#command='udpsrc port=%s ! application/x-rtp ! rtph264depay ! avdec_h264 ! videoconvert ! appsink' % streamport
#cap = cv2.VideoCapture(command)
#cap = cv2.VideoCapture("http://172.17.0.1:8080/?action=stream")
cap = cv2.VideoCapture("http://192.168.1.79:8080/?action=stream")
#cap = cv2.VideoCapture("tcp://172.17.0.1:6000")
```
