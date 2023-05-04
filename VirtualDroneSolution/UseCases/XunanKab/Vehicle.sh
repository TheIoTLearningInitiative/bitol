#!/usr/bin/env bash

set -x

# =============================================================================
# Variables
# =============================================================================

SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}" )" )"

usage() {
    echo "$0 [-i <initialize>] [-s <server>] [-n <name>] [-m <identification>] [-g <gcs port>]"
    echo ""
    echo "Options:"
    echo "  -i: Initialize? powerup :: powedown"
    echo "  -s: IP address of the server"
    echo "  -n: Name of the vehicle"
    echo "  -m: Id of the vehicle"
    echo "  -g: Ground Control Station Port"
    echo "  -g: Ports"
    echo ""
}

while getopts "i:s:n:m:g:p:" o; do
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
        m)
            ID="$OPTARG"
            ;;
        g)
            GCS_PORT="$OPTARG"
            ;;
	p)
	    PORT="$OPTARG"
	    ;;
        *)
            usage
            exit 1
            ;;
    esac
done
shift $((OPTIND-1))

VEHICLE_NAME=$NAME-vehicle
VEHICLE_ID=${ID}
#VEHICLE_LATITUDE=${VEHICLE_LATITUDE:-20.6679137}
#VEHICLE_LONGITUDE=${VEHICLE_LONGITUDE:--103.4630988}
VEHICLE_LATITUDE=${VEHICLE_LATITUDE:-20.6552144}
VEHICLE_LONGITUDE=${VEHICLE_LONGITUDE:--103.3239878}

VEHICLE_ALTITUDE=${VEHICLE_ALTITUDE:-10}

VEHICLE_TCP_PORT_A=$((${PORT} + 1))
VEHICLE_UDP_PORT_A=$GCS_PORT

VEHICLE_DOCKER_IMAGE=xe1gyq/copter

TASK_DOCKER_IMAGE=task-id
TASK_DOCKER_IMAGE_ID=${TASK_DOCKER_IMAGE}

CONNECTION_PROTOCOL=tcp
CONNECTION_PORT_GROUND_CONTROL_STATION=$((${PORT} + 2))
CONNECTION_PORT_COMMUNICATION_LIBRARY=$((${PORT} + 3))

# =============================================================================
# Main
# =============================================================================

if ([ "$INITIALIZE" == "powerup" ]); then

    UUID=`docker run -itd --name ${VEHICLE_NAME} \
                                 ${VEHICLE_DOCKER_IMAGE} \
                                 ${VEHICLE_ID} \
                                 ${VEHICLE_LATITUDE} ${VEHICLE_LONGITUDE} \
                                 ${VEHICLE_ALTITUDE}\
                                 ${VEHICLE_TCP_PORT_A} \
                                 ${VEHICLE_UDP_PORT_A}`
    IP=`docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${VEHICLE_NAME}`
    echo "Copter Information: " $VEHICLE_NAME $IP $UUID
    sleep 3
    CONNECTION=${CONNECTION_PROTOCOL}:${IP}:${CONNECTION_PORT_COMMUNICATION_LIBRARY}
    # docker run $TASK_DOCKER_IMAGE_ID $CONNECTION ${VEHICLE_ID}

elif ([ "$INITIALIZE" == "powerdown" ]); then

    docker container rm -f ${VEHICLE_NAME}

fi
