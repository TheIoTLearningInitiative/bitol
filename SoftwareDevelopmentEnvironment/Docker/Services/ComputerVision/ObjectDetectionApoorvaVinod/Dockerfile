FROM user/core-opencv

MAINTAINER Abraham Arce "xe1gyq@gmail.com"

ARG OPENCV_VERSION=3.4.2

ENV TIMEZONE America/Mexico_City
ENV USER root

ENV DEBIAN_FRONTEND noninteractive

WORKDIR /

EXPOSE 5000

USER user
WORKDIR /home/user

RUN git clone https://github.com/xe1gyq/Real_time_Object_detection_and_tracking.git

WORKDIR /home/user/Real_time_Object_detection_and_tracking/model_data/

RUN wget https://github.com/Reyes-fred/Xiaomin/raw/master/Scripts/ImageRecognition/RealtimeObjectDetection/MobileNetSSD_deploy.caffemodel

RUN wget https://pjreddie.com/media/files/yolov2.weights

RUN wget https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg
RUN wget https://pjreddie.com/media/files/yolov3.weights

WORKDIR /home/user/Real_time_Object_detection_and_tracking/
