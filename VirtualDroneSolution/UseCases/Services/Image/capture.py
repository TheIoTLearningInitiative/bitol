import cv2

cap = cv2.VideoCapture(0)
framerate = 25.0

#out = cv2.VideoWriter('appsrc ! videoconvert ! '
#                      'x264enc noise-reduction=10000 speed-preset=ultrafast tune=zerolatency ! '
#                      'rtph264pay config-interval=1 pt=96 !'
#                      'tcpserversink host=127.0.0.1 port=5000 sync=false',
#                      0, framerate, (640, 480))

out = cv2.VideoWriter('appsrc ! videoconvert ! video/x-raw,format=YUY2,width=640,height=480 ! jpegenc ! rtpjpegpay ! '
                      'udpsink host=127.0.0.1 port=5000',
                      0, framerate, (640, 480))

#out = cv2.VideoWriter('v4l2src ! video/x-raw,format=YUY2,width=640,height=480 ! jpegenc ! rtpjpegpay ! '
#                      'udpsink host=127.0.0.1 port=5000',
#                       0, framerate, (640, 480))


while cap.isOpened():
    ret, frame = cap.read()
    if ret:

        out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
