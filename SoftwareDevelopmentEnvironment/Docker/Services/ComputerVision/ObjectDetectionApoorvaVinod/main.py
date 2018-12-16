import cv2
import argparse
import numpy as np
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--input', help='Path to input image.')
args = parser.parse_args()

# Minimum confidence threshold. Increasing this will improve false positives but will also reduce detection rate.
min_confidence=0.14
model = 'model_data/yolov2.weights'
config = 'model_data/yolov2.cfg'

framerate=25
name="quintanaroo"
streamport="5000"
displayip="172.17.0.1"
displayport="5100"

command='udpsrc port=%s ! application/x-rtp, encoding-name=JPEG, payload=26 ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink' % streamport
#command='udpsrc port=%s ! application/x-rtp ! rtph264depay ! avdec_h264 ! videoconvert ! appsink' % streamport
cap = cv2.VideoCapture(command)

display="appsrc ! videoconvert ! video/x-raw,format=YUY2,width=640,height=480 ! jpegenc ! rtpjpegpay ! udpsink host=" + displayip + " port=" + displayport
displayout = cv2.VideoWriter(display, 0, framerate, (640, 480))

#Load names of classes
classes = None
with open('model_data/coco_classes.txt', 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')
print(classes)

# Load weights and construct graph
net = cv2.dnn.readNetFromDarknet(config, model)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

winName = 'Running YOLO Model'
cv2.namedWindow(winName, cv2.WINDOW_NORMAL)

while(True):

    #Read input image
    ret, frame = cap.read()
    #print(frame)
    #rows = frame.shape[0]
    #cols = frame.shape[1]
    frame_resized = cv2.resize(frame,(300,300))

    # Get width and height
    #height,width,ch=frame.shape

    # Create a 4D blob from a frame.
    blob = cv2.dnn.blobFromImage(frame_resized, 1.0/255.0, (416, 416), True, crop=False)
    #blob = cv2.dnn.blobFromImage(frame, 1.0/127.5, (300, 300), (127.5, 127.5, 127.5), True)
    net.setInput(blob)
    # Run the preprocessed input blog through the network
    predictions = net.forward()
    probability_index=5

    for i in range(predictions.shape[0]):
        prob_arr=predictions[i][probability_index:]
        class_index=prob_arr.argmax(axis=0)
        confidence= prob_arr[class_index]
        if confidence > min_confidence:
            x_center=predictions[i][0]*width
            y_center=predictions[i][1]*height
            width_box=predictions[i][2]*width
            height_box=predictions[i][3]*height

            x1=int(x_center-width_box * 0.5)
            y1=int(y_center-height_box * 0.5)
            x2=int(x_center+width_box * 0.5)
            y2=int(y_center+height_box * 0.5)
    
            cv2.rectangle(frame,(x1,y1),(x2,y2),(255,255,255),1)
            cv2.putText(frame,classes[class_index]+" "+"{0:.1f}".format(confidence),(x1,y1), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255$
            # cv2.imwrite("out_"+args.input, frame)
    #cv2.imshow(winName, frame)
    cv2.putText(frame, name, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,177,1), 3)
    displayout.write(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
out.release()

