import cv2
import sys

device_port_udp_in=sys.argv[0]
server_ip=sys.argv[1]
server_port_udp_out=sys.argv[2]
framerate=25

cap = cv2.VideoCapture('udpsrc port=5000 ! application/x-rtp, encoding-name=JPEG, payload=26 ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink')
#cap = cv2.VideoCapture('udpsrc port=5000 ! application/x-rtp ! rtph264depay ! avdec_h264 ! videoconvert ! appsink')

out = cv2.VideoWriter('appsrc ! videoconvert ! video/x-raw,format=YUY2,width=640,height=480 ! jpegenc ! rtpjpegpay ! '
                      'udpsink host=172.17.0.1 port=5600',
                      0, framerate, (640, 480))
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

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
	out.write(frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cap.release()
out.release()
