#!/usr/bin/env bash

# set -x

# =============================================================================
# Variables
# =============================================================================

# Server

SERVER_IP=$1

# Core :: Copter

COPTER_DOCKER_IMAGE=${USER}/core-copter
COPTER_NUMBER=1
COPTER_NAMES[0]='quintanaroo-copter'
COPTER_NAMES[1]='yucatan-copter'

# Vehicle

VEHICLE_ID=1
VEHICLE_LATITUDE=20.6552144
#VEHICLE_LATITUDE=20.6710109
VEHICLE_LONGITUDE=-103.3239878
#VEHICLE_LONGITUDE=-103.4562345
VEHICLE_ALTITUDE=5

# Task

TASK_DOCKER_IMAGE=${USER}/task
TASK_DOCKER_IMAGE_ID=${TASK_DOCKER_IMAGE}-id

# Connection

CONNECTION_PROTOCOL=tcp
CONNECTION_PORT_GROUND_CONTROL_STATION=5762
CONNECTION_PORT_COMMUNICATION_LIBRARY=5763

# Image

SERVICE_FACEDETECT_IP=$3

# Network

NETWORK_NAME="xunankab_network"
NETWORK_SUBNET="172.0.0.0"

# =============================================================================
# Main
# =============================================================================

docker network ls --filter name=${NETWORK_NAME} | grep ${NETWORK_NAME}
if [ $? -ne 0 ]; then
    docker network create --subnet=${NETWORK_SUBNET}/16 ${NETWORK_NAME}
fi

for ((i=0; i<=$COPTER_NUMBER; i++)); do
  COPTER_NAME=${COPTER_NAMES[$i]}
  UUID=`docker run -itd --name ${COPTER_NAME} \
                               ${COPTER_DOCKER_IMAGE} \
                               ${VEHICLE_ID} \
                               ${VEHICLE_LATITUDE} ${VEHICLE_LONGITUDE} \
                               ${VEHICLE_ALTITUDE}`
  IP=`docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${COPTER_NAME}`
  echo "Copter Information: " $COPTER_NAME $IP $UUID
  sleep 3
  CONNECTION=${CONNECTION_PROTOCOL}:${IP}:${CONNECTION_PORT_COMMUNICATION_LIBRARY}
  docker run $TASK_DOCKER_IMAGE_ID $CONNECTION ${VEHICLE_ID}
done

                               #-p ${CONNECTION_PORT_GROUND_CONTROL_STATION}:${CONNECTION_PORT_GROUND_CONTROL_STATION=5762} \
                               #-p ${CONNECTION_PORT_COMMUNICATION_LIBRARY}:${CONNECTION_PORT_COMMUNICATION_LIBRARY} \

#docker run --net ${NETWORK_NAME} --ip ${COPTER_IP} -itd ${COPTER_IMAGE}

# Main :: Image

#docker run --net ${NETWORK_NAME} --ip ${SERVICE_FACEDETECT_IP} -it -p 5000:5000/udp -p 5600:5600/udp xe1gyq/facedetect
#docker run --net ${NETWORK_NAME} --ip ${SERVICE_FACEDETECT_IP} -itd xe1gyq/facedetect
#gst-launch-1.0 -v v4l2src device=/dev/video0 ! image/jpeg,width=640, height=480, framerate=30/1 ! rtpjpegpay ! udpsink host=${SERVICE_FACEDETECT_IP} port=5000 &
#gst-launch-1.0 -v udpsrc port=5600 ! application/x-rtp, media=video, clock-rate=90000, encoding-name=JPEG, payload=26 ! rtpjpegdepay ! jpegdec ! xvimagesink sync=0 &
