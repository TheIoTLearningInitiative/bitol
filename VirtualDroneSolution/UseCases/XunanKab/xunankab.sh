#!/usr/bin/env bash

set -x

# =============================================================================
# Variables
# =============================================================================

# Variables :: Server

SERVER_IP=$1

# Variables :: Copter

COPTER_IMAGE="xe1gyq/copter"
COPTER_IP=$2

# Variables :: Image

SERVICE_FACEDETECT_IP=$3

# Variables :: Network

NETWORK_NAME="xunankab_network"
NETWORK_SUBNET="172.0.0.0"

# =============================================================================
# Main
# =============================================================================

docker network ls --filter name=${NETWORK_NAME} | grep ${NETWORK_NAME}
if [ $? -ne 0 ]; then
    docker network create --subnet=${NETWORK_SUBNET}/16 ${NETWORK_NAME}
fi

#docker run --net ${NETWORK_NAME} --ip ${COPTER_IP} -itd ${COPTER_IMAGE}

# Main :: Image

#docker run --net ${NETWORK_NAME} --ip ${SERVICE_FACEDETECT_IP} -it -p 5000:5000/udp -p 5600:5600/udp xe1gyq/facedetect
docker run --net ${NETWORK_NAME} --ip ${SERVICE_FACEDETECT_IP} -itd xe1gyq/facedetect
gst-launch-1.0 -v v4l2src device=/dev/video0 ! image/jpeg,width=640, height=480, framerate=30/1 ! rtpjpegpay ! udpsink host=${SERVICE_FACEDETECT_IP} port=5000 &
gst-launch-1.0 -v udpsrc port=5600 ! application/x-rtp, media=video, clock-rate=90000, encoding-name=JPEG, payload=26 ! rtpjpegdepay ! jpegdec ! xvimagesink sync=0 &
