#!/usr/bin/env python

# Based on research work from https://github.com/Reyes-fred/Xiaomin and authors
# See also https://github.com/opencv/opencv/tree/master/data/haarcascades

import cv2
import os
import sys

if __name__ == "__main__":

    filePath = os.path.dirname(os.path.realpath(__file__))
    print(filePath)
    cascPath = "haarcascade_frontalface_alt.xml"
    devVideo = os.environ['MAIN_DEV_VIDEO']
    videoCapture = cv2.VideoCapture(devVideo)

    while True:
   
        ret, image = videoCapture.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faceCascade = cv2.CascadeClassifier(cascPath)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
        )

        print("Found {0} faces!".format(len(faces)))

        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imshow('Face Detector', image)
     
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    sys.exit(0)
