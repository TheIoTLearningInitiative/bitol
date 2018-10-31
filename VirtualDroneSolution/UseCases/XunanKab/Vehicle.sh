#!/usr/bin/env bash

set -x

# =============================================================================
# Variables
# =============================================================================

SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}" )" )"

usage() {
    echo "$0 [-i initialize] [-s <server>] [-n <name>] [-c <camera>] [-p <port>]"
    echo ""
    echo "Options:"
    echo "  -i: Initialize? powerup :: powedown"
    echo "  -s: IP address of the server"
    echo "  -n: Name of the vehicle"
    echo "  -c: Camera device"
    echo "  -p: Stream port "
    echo ""
}

while getopts "i:s:n:c:p:" o; do
    case "${o}" in
        i)
            INITIALIZE="$OPTARG"
            ;;
        s)
            COMMAND_CENTER="$OPTARG"
            ;;
        n)
            NAME="$OPTARG"
            ;;
        c)
            CAMERA_DEVICE="$OPTARG"
            ;;
        p)
            STREAM_PORT="$OPTARG"
            ;;
        *)
            usage
            exit 1
            ;;
    esac
done
shift $((OPTIND-1))

VEHICLE_NAME=$NAME-vehicle
VEHICLE_ID=${VEHICLE_ID:-1}
VEHICLE_LATITUDE=${VEHICLE_LATITUDE:-20.6679137}
VEHICLE_LONGITUDE=${VEHICLE_LONGITUDE:-103.4630988}
VEHICLE_ALTITUDE=${VEHICLE_ALTITUDE:-10}

VEHICLE_DOCKER_IMAGE=user/core-copter

TASK_DOCKER_IMAGE=user/task
TASK_DOCKER_IMAGE_ID=${TASK_DOCKER_IMAGE}-id

CONNECTION_PROTOCOL=tcp
CONNECTION_PORT_GROUND_CONTROL_STATION=5762
CONNECTION_PORT_COMMUNICATION_LIBRARY=5763

FACEDETECT_DOCKER_IMAGE=user/computervision-facedetect
FACEDETECT_NAME=$NAME-facedetect

# =============================================================================
# Main
# =============================================================================

if ([ "$INITIALIZE" == "powerup" ]); then

    UUID=`docker run -itd --name ${VEHICLE_NAME} \
                                 ${VEHICLE_DOCKER_IMAGE} \
                                 ${VEHICLE_ID} \
                                 ${VEHICLE_LATITUDE} ${VEHICLE_LONGITUDE} \
                                 ${VEHICLE_ALTITUDE}`
    IP=`docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${VEHICLE_NAME}`
    echo "Copter Information: " $VEHICLE_NAME $IP $UUID
    sleep 3
    CONNECTION=${CONNECTION_PROTOCOL}:${IP}:${CONNECTION_PORT_COMMUNICATION_LIBRARY}
    docker run $TASK_DOCKER_IMAGE_ID $CONNECTION $VEHICLE_ID

    if [ -e $CAMERA_DEVICE ]; then

        gst-launch-1.0 -v v4l2src device=${CAMERA_DEVICE} ! image/jpeg,width=640, height=480, framerate=30/1 ! rtpjpegpay ! udpsink host=${IP} port=${STREAM_PORT} &

    fi

elif ([ "$INITIALIZE" == "powerdown" ]); then

    docker container rm -f ${VEHICLE_NAME}
    killall -9 gst-launch-1.0

fi
