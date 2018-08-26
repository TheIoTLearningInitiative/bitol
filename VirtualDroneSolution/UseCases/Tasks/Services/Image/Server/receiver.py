import cv2

#cap = cv2.VideoCapture('udpsrc port=5000 ! application/x-rtp, media=video, clock-rate=90000, encoding-name=JPEG, payload=26 !'
#                       'rtpjpegdepay ! jpegdec ! xvimagesink sync=0')
#cap = cv2.VideoCapture('udpsrc port=5000 caps=\"application/x-rtp, format=(string)I420, width=(int)1280, height=(int)720,'
#                        'pixel-aspect-ratio=(fraction)1/1, interlace-mode=(string)progressive, colorimetry=(string)bt709, framerate=(fraction)25/1\" !'
#                         'rtph264depay ! videoconvert ! decodebin ! appsink')
#cap = cv2.VideoCapture('udpsrc port=5000 ! application/x-rtp, media=video, clock-rate=90000, encoding-name=JPEG, payload=26 !'
#                       'rtpjpegdepay ! jpegdec ! appsink')
#cap = cv2.VideoCapture('udpsrc port=5000 caps=\"application/x-rtp, media=video" ! rtpjpegdepay ! jpegdec ! appsink')

# gst-launch-1.0 -v videotestsrc ! video/x-raw,framerate=20/1 ! videoscale ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink host=X.X.X.X port=5000
# gst-launch-1.0 -v udpsrc port=5000 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! decodebin ! videoconvert ! autovideosink

#cap = cv2.VideoCapture('udpsrc port=5000 ! application/x-rtp,media=video,payload=96,clock-rate=90000,encoding-name=H264, !'
#                       ' rtph264depay ! decodebin ! videoconvert ! video/x-raw, format=BGR ! appsink')

#cap = cv2.VideoCapture("udpsrc port=5000 caps=\"application/x-rtp,  format=(string)i420, width=(int)1280, height=(int)720,  pixel-aspect-ratio=(fraction)1/1, interlace-mode=(string)progressive,  colorimetry=(string)bt709, framerate=(fraction)25/1\" ! rtph264depay !  videoconvert ! decodebin ! appsink") 
#cap = cv2.VideoCapture("udpsrc port=5000 caps=\"application/x-rtp,  format=(string)i420, width=(int)1280, height=(int)720,  pixel-aspect-ratio=(fraction)1/1, interlace-mode=(string)progressive,  colorimetry=(string)bt709, framerate=(fraction)25/1\" ! rtph264depay !  videoconvert ! decodebin ! autovideosink") 
#cap = cv2.VideoCapture('udpsrc port=5000 caps=\"application/x-rtp, media=video, clock-rate=9000, encoding-name=JPEG, payload=26" ! rtpjpegdepay ! jpegdec ! xvimagesink sync=0') 
#cap = cv2.VideoCapture('udpsrc port=5000 ! application/x-rtp, media=video, clock-rate=9000, encoding-name=JPEG ! rtpjpegdepay ! jpegdec ! appsink')
#cap = cv2.VideoCapture('udpsrc port=5000 ! application/x-rtp, encoding-name=JPEG, payload=26 ! rtpjpegdepay ! jpegdec ! autovideosink')
cap = cv2.VideoCapture('udpsrc port=5000 ! application/x-rtp, encoding-name=JPEG, payload=26 ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink')
#cap = cv2.VideoCapture('videotestsrc ! appsink')
#cap = cv2.VideoCapture('autovideosrc ! autovideosink')

#out = cv2.VideoWriter('appsrc ! videoconvert ! video/x-raw,format=YUY2,width=640,height=480 ! jpegenc ! rtpjpegpay ! '
#                      'udpsink host=127.0.0.1 port=5000',
#                      0, framerate, (640, 480))

while(cap.isOpened()):
    print("loop")

    ret, frame = cap.read()
    print("ret, frame")

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    print("gray")

    cv2.imshow('frame', gray)
    print("imshow")
    if cv2.waitKey(40) & 0xFF == ord('q'):
        print("breaking")
        break

cap.release()
cv2.destroyAllWindows()
