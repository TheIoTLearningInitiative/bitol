#!/usr/bin/env bash

# set -x

# =============================================================================
# Variables
# =============================================================================

# Arguments

INITIALIZE=$1

# Core :: Copter

FACEDETECT_DOCKER_IMAGE=${USER}/computervision-facedetect
FACEDETECT_NUMBER=0
FACEDETECT_NAMES[0]='one-facedetect'
FACEDETECT_NAMES[1]='two-facedetect'

# Camera

CAMERA_DEVICE=/dev/video

# =============================================================================
# Main
# =============================================================================

if ([ "$INITIALIZE" == "powerup" ]); then
  for ((i=0; i<=$FACEDETECT_NUMBER; i++)); do
    FACEDETECT_NAME=${FACEDETECT_NAMES[$i]}
    UUID=`docker run -itd --name ${FACEDETECT_NAME} ${FACEDETECT_DOCKER_IMAGE}`
    IP=`docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${FACEDETECT_NAME}`
    echo "Service FaceDetect Information: " $FACEDETECT_NAME $IP $UUID
    gst-launch-1.0 -v v4l2src device=${CAMERA_DEVICE}${i} ! image/jpeg,width=640, height=480, framerate=30/1 ! rtpjpegpay ! udpsink host=${IP} port=5000 &
    gst-launch-1.0 -v udpsrc port=5700 ! application/x-rtp, media=video, clock-rate=90000, encoding-name=JPEG, payload=26 ! rtpjpegdepay ! jpegdec ! xvimagesink sync=0 &
  done
elif ([ "$INITIALIZE" == "powerdown" ]); then
  for ((i=0; i<=$FACEDETECT_NUMBER; i++)); do
     FACEDETECT_NAME=${FACEDETECT_NAMES[$i]}
     docker container rm -f ${FACEDETECT_NAME}
     killall -9 gst-launch-1.0
  done
else
    echo "No argument given..." 
fi

#                          -p 5000:5000/udp -p 5700:5700/udp \

#docker run --net ${NETWORK_NAME} --ip ${SERVICE_FACEDETECT_IP} -it -p 5000:5000/udp -p 5600:5600/udp xe1gyq/facedetect
#docker run --net ${NETWORK_NAME} --ip ${SERVICE_FACEDETECT_IP} -itd xe1gyq/facedetect
#gst-launch-1.0 -v v4l2src device=/dev/video0 ! image/jpeg,width=640, height=480, framerate=30/1 ! rtpjpegpay ! udpsink host=${SERVICE_FACEDETECT_IP} port=5000 &
#gst-launch-1.0 -v udpsrc port=5600 ! application/x-rtp, media=video, clock-rate=90000, encoding-name=JPEG, payload=26 ! rtpjpegdepay ! jpegdec ! xvimagesink sync=0 &
