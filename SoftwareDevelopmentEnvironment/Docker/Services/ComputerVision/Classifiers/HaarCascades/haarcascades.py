import cv2
import sys

framerate=25
name=sys.argv[1]
streamport=sys.argv[2]
displayip=sys.argv[3]
displayport=sys.argv[4]

command='udpsrc port=%s ! application/x-rtp, encoding-name=JPEG, payload=26 ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink' % streamport
command='udpsrc port=%s ! application/x-rtp ! rtph264depay ! avdec_h264 ! videoconvert ! appsink' % streamport
cap = cv2.VideoCapture(command)

display="appsrc ! videoconvert ! video/x-raw,format=YUY2,width=640,height=480 ! jpegenc ! rtpjpegpay ! udpsink host=" + displayip + " port=" + displayport
displayout = cv2.VideoWriter(display, 0, framerate, (640, 480))

faceCascade = cv2.CascadeClassifier("/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_alt2.xml")

while(True):
	ret, frame = cap.read()

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor=1.1,
		minNeighbors=5,
		minSize=(30, 30)
	)

	print("Found {0} faces!".format(len(faces)))

	for (x, y, w, h) in faces:
		cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

	cv2.putText(frame, name, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,177,1), 3)

	displayout.write(frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
out.release()
