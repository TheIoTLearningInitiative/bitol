#!/usr/bin/env bash

set -x

# =============================================================================
# Variables
# =============================================================================

SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}" )" )"

usage() {
    echo "$0 [-i initialize] [-s <vehicleip>] [-n <name>] [-m identification]"
    echo ""
    echo "Options:"
    echo "  -i: Initialize? powerup :: powedown"
    echo "  -s: IP address of the client"
    echo "  -n: Name of the vehicle"
    echo "  -m: Id of the vehicle"
    echo ""
}

while getopts "i:s:n:m:" o; do
    case "${o}" in
        i)
            INITIALIZE="$OPTARG"
            ;;
        s)
            VEHICLEIP="$OPTARG"
            ;;
        n)
            NAME="$OPTARG"
            ;;
        m)
            ID="$OPTARG"
            ;;
        *)
            usage
            exit 1
            ;;
    esac
done
shift $((OPTIND-1))

VEHICLE_NAME=${NAME}-telemetry
VEHICLE_ID=${ID}

SERVICE_TELEMETRY_DOCKER_IMAGE=user/telemetry
SERVICE_TELEMETRY_MQTT_DOCKER_IMAGE=${SERVICE_TELEMETRY_DOCKER_IMAGE}-mqtt

CONNECTION_PROTOCOL=tcp
CONNECTION_PORT_GROUND_CONTROL_STATION=5762
CONNECTION_PORT_COMMUNICATION_LIBRARY=5763
CONNECTION_PORT_COMMUNICATION_TELEMETRY=5764

# =============================================================================
# Main
# =============================================================================

if ([ "$INITIALIZE" == "powerup" ]); then

    CONNECTION=${CONNECTION_PROTOCOL}:${VEHICLEIP}:${CONNECTION_PORT_COMMUNICATION_TELEMETRY}
    UUID=`docker run -itd --name ${VEHICLE_NAME} ${SERVICE_TELEMETRY_MQTT_DOCKER_IMAGE} ${CONNECTION} ${VEHICLE_ID}`
    IP=`docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${VEHICLE_NAME}`
    echo "Telemetry Information: " $VEHICLE_NAME $IP $UUID

elif ([ "$INITIALIZE" == "powerdown" ]); then

    docker container rm -f ${VEHICLE_NAME}

fi
