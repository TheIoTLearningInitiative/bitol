import cv2
import sys

framerate=25
name=sys.argv[1]
streamport=sys.argv[2]
displayip=sys.argv[3]
displayport=sys.argv[4]
haport=sys.argv[5]

command='udpsrc port=%s ! application/x-rtp, encoding-name=JPEG, payload=26 ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink' % streamport
cap = cv2.VideoCapture(command)

display="appsrc ! videoconvert ! video/x-raw,format=YUY2,width=640,height=480 ! jpegenc ! rtpjpegpay ! udpsink host=" + displayip + " port=" + displayport
displayout = cv2.VideoWriter(display, 0, framerate, (640, 480))

ha="appsrc ! video/x-h264,width=1280,height=720,framerate=30/1 ! h264parse config-interval=1 ! matroskamux streamable=true ! tcpserversink host=::0 port=9000 sync=false sync-method=2"
haout = cv2.VideoWriter(ha, 0, framerate, (640, 480))

faceCascade = cv2.CascadeClassifier("/usr/local/share/OpenCV/haarcascades/haarcascade_fullbody.xml")

while(True):
	ret, frame = cap.read()

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	bodies = faceCascade.detectMultiScale(
		gray,
		scaleFactor=1.1,
		minNeighbors=5,
		minSize=(30, 30)
		#flags = cv2.CV_HAAR_SCALE_IMAGE
	)

	print("Found {0} bodies!".format(len(bodies)))

	for (x, y, w, h) in bodies:
		cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

	displayout.write(frame)
	haout.write(frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
out.release()
