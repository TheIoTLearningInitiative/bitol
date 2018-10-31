import cv2
import sys

framerate=25
streamport=sys.argv[1]
displayip=sys.argv[2]
displayport=sys.argv[3]

#cap = cv2.VideoCapture(0)
command='udpsrc port=%s ! application/x-rtp, encoding-name=JPEG, payload=26 ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink' % streamport
cap = cv2.VideoCapture(command)
#cap = cv2.VideoCapture('udpsrc port=5000 ! application/x-rtp ! rtph264depay ! avdec_h264 ! videoconvert ! appsink')

#out = cv2.VideoWriter('appsrc ! videoconvert ! video/x-raw,format=YUY2,width=640,height=480 ! jpegenc ! rtpjpegpay ! '
#                      'udpsink host=172.17.0.1 port=5700',
#                      0, framerate, (640, 480))
command='appsrc ! videoconvert ! video/x-raw,format=YUY2,width=640,height=480 ! jpegenc ! rtpjpegpay ! udpsink host=%s port=%s 0, %s, (640, 480)' % (displayip, displayport, framerate)
out = cv2.VideoWriter(command)

# Create the haar cascade
faceCascade = cv2.CascadeClassifier("/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")

while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()

	# Our operations on the frame come here
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Detect faces in the image
	faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor=1.1,
		minNeighbors=5,
		minSize=(30, 30)
		#flags = cv2.CV_HAAR_SCALE_IMAGE
	)

	print("Found {0} faces!".format(len(faces)))

	# Draw a rectangle around the faces
	for (x, y, w, h) in faces:
		cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)


	# Display the resulting frame
	out.write(frame)
	#cv2.imshow('frame', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
out.release()
