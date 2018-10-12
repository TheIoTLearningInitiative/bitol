#!/usr/bin/env bash

#set -x

# =============================================================================
# Variables
# =============================================================================

DIRECTORY_USECASES=`dirname "$(readlink -f "$0")"`
DIRECTORY_IMAGES=$DIRECTORY_USECASES/Images
DIRECTORY_DOCKER=$DIRECTORY_IMAGES/Docker

# =============================================================================
# Functions
# =============================================================================

usage() {
    echo "$0 [-h] [-c <components>]"
    echo ""
    echo "Options:"
    echo "  -c: Components"
    echo ""
}

# =============================================================================
# Main
# =============================================================================

while getopts "c:" o; do
    case "${o}" in
        c)
            COMPONENTS="$OPTARG"
            ;;
        *)
            usage
            exit 1
            ;;
    esac
done
shift $((OPTIND-1))

if ([ "$COMPONENTS" != "all" ]); then
    echo "Building individual components is not supported."
    exit -1
fi

cd $DIRECTORY_DOCKER

for COMPONENT in *
do
    cd $DIRECTORY_DOCKER/$COMPONENT
    component=`echo "$COMPONENT" | tr '[:upper:]' '[:lower:]'`
    docker build -t $USER/$component .
done

# End of file
