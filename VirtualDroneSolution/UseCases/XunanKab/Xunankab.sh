#!/usr/bin/env bash

set -x

# =============================================================================
# Variables
# =============================================================================

SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}" )" )"

usage() {
    echo "$0 [-s <server>] [-n <name>] [-c <camera>]"
    echo ""
    echo "Options:"
    echo "  -s: IP address of the server"
    echo "  -n: Name of the vehicle"
    echo "  -c: Camera device"
    echo ""
}

while getopts "s:n:c" o; do
    case "${o}" in
        s)
            COMMAND_CENTER="$OPTARG"
            ;;
        n)
            VEHICLE_NAME="$OPTARG"
            ;;
        c)
            CAMERA_DEVICE="$OPTARG"
            ;;
        *)
            usage
            exit 1
            ;;
    esac
done
shift $((OPTIND-1))

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

SERVICE_FACEDETECT_IP=$3

# =============================================================================
# Main
# =============================================================================

docker container rm -f ${VEHICLE_NAME}
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
  echo "We have a camera"
fi
