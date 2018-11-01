#!/usr/bin/env bash

#set -x

# =============================================================================
# Variables
# =============================================================================

SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}" )" )"

usage() {
    echo "$0 [-i initialize] [-v <vehicle>] [-n <name>] [-l <local>] [-r <remote>]"
    echo ""
    echo "Options:"
    echo "  -i: Initialize? powerup :: powedown"
    echo "  -v: IP of the vehicle"
    echo "  -n: Name of the vehicle"
    echo "  -l: Local stream port"
    echo "  -r: Remote stream port"
    echo ""
}

while getopts "i:v:n:l:r:" o; do
    case "${o}" in
        i)
            INITIALIZE="$OPTARG"
            ;;
        v)
            VEHICLE="$OPTARG"
            ;;
        n)
            NAME="$OPTARG"
            ;;
        l)
            STREAM_PORT="$OPTARG"
            ;;
        r)
            DISPLAY_PORT="$OPTARG"
            ;;
        *)
            usage
            exit 1
            ;;
    esac
done
shift $((OPTIND-1))

VEHICLE_NAME=$NAME-vehicle

FACEDETECT_DOCKER_IMAGE=user/computervision-facedetect
FACEDETECT_NAME=$NAME-facedetect

# =============================================================================
# Main
# =============================================================================

if ([ "$INITIALIZE" == "powerup" ]); then

    UUID=`docker run -itd --name ${FACEDETECT_NAME} ${FACEDETECT_DOCKER_IMAGE} ${STREAM_PORT} 172.17.0.1 ${DISPLAY_PORT}`
    IP=`docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${FACEDETECT_NAME}`
    echo "Service FaceDetect Information: " $FACEDETECT_NAME $IP $UUID
    gst-launch-1.0 -v udpsrc port=$DISPLAY_PORT ! application/x-rtp, media=video, clock-rate=90000, encoding-name=JPEG, payload=26 ! rtpjpegdepay ! jpegdec ! xvimagesink sync=0 &

elif ([ "$INITIALIZE" == "powerdown" ]); then

    docker container rm -f ${FACEDETECT_NAME}
    killall -9 gst-launch-1.0

fi
