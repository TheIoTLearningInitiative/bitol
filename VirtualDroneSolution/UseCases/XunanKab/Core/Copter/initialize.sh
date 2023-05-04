#!/usr/bin/env bash

# set -x

# =============================================================================
# Variables
# =============================================================================

# Argument

INITIALIZE=$1

# Core :: Copter

COPTER_DOCKER_IMAGE=xe1gyq/copter
COPTER_NUMBER=4
COPTER_NAMES[0]='quintanaroo-copter'
COPTER_NAMES[1]='yucatan-copter'
COPTER_NAMES[2]='campeche-copter'
COPTER_NAMES[3]='chiapas-copter'
COPTER_NAMES[4]='tabasco-copter'

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

# =============================================================================
# Main
# =============================================================================

if ([ "$INITIALIZE" == "powerup" ]); then
  for ((i=0; i<=$COPTER_NUMBER; i++)); do
     COPTER_NAME=${COPTER_NAMES[$i]}
     UUID=`docker run -itd --name ${COPTER_NAME} \
                               ${COPTER_DOCKER_IMAGE} \
                               $i \
                               ${VEHICLE_LATITUDE} ${VEHICLE_LONGITUDE} \
                               ${VEHICLE_ALTITUDE}`
     IP=`docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${COPTER_NAME}`
     echo "Copter Information: " $COPTER_NAME $IP $UUID
     sleep 3
     CONNECTION=${CONNECTION_PROTOCOL}:${IP}:${CONNECTION_PORT_COMMUNICATION_LIBRARY}
     # docker run $TASK_DOCKER_IMAGE_ID $CONNECTION ${VEHICLE_ID}
  done
elif ([ "$INITIALIZE" == "powerdown" ]); then
  for ((i=0; i<=$COPTER_NUMBER; i++)); do
     COPTER_NAME=${COPTER_NAMES[$i]}
     docker container rm -f ${COPTER_NAME}
  done
else
    echo "No argument given..."
fi
