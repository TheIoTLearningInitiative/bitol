#!/usr/bin/env python

import cv2
import os
import sys

if __name__ == "__main__":

    cascPath = "HaarcascadeFrontalfaceAlt.xml"
    videoCapture = cv2.VideoCapture("/dev/video0")

    while True:
   
        faceCascade = cv2.CascadeClassifier(cascPath)
        ret, image = videoCapture.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            #flags = cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        #print "Found {0} faces!".format(len(faces))

        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imshow('Face Detector', image)
     
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    sys.exit(0)
