#!/usr/bin/env bash

set -x

# =============================================================================
# Variables
# =============================================================================

DIRECTORY_DOCKER=`dirname "$(readlink -f "$0")"`

DIRECTORY_CORE=$DIRECTORY_DOCKER/Core
DIRECTORY_TASKS=$DIRECTORY_DOCKER/Tasks
DIRECTORY_APPLICATIONS=$DIRECTORY_DOCKER/Applications
DIRECTORY_SERVICES=$DIRECTORY_DOCKER/Services
DIRECTORY_SERVICES_COMPUTERVISION=$DIRECTORY_SERVICES/ComputerVision
DIRECTORY_SERVICES_TELEMETRY=$DIRECTORY_SERVICES/Telemetry

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

cd $DIRECTORY_CORE

for COMPONENT in *
do
    cd $DIRECTORY_CORE/$COMPONENT
    component=`echo "$COMPONENT" | tr '[:upper:]' '[:lower:]'`
    docker build -t user/core-$component .
done

cd $DIRECTORY_TASKS

for COMPONENT in *
do
    cd $DIRECTORY_TASKS/$COMPONENT
    component=`echo "$COMPONENT" | tr '[:upper:]' '[:lower:]'`
    docker build -t user/task-$component .
done

cd $DIRECTORY_SERVICES_COMPUTERVISION

for COMPONENT in *
do
    cd $DIRECTORY_SERVICES_COMPUTERVISION/$COMPONENT
    component=`echo "$COMPONENT" | tr '[:upper:]' '[:lower:]'`
    docker build -t user/computervision-$component .
done

cd $DIRECTORY_SERVICES_TELEMETRY

for COMPONENT in *
do
    cd $DIRECTORY_SERVICES_TELEMETRY/$COMPONENT
    component=`echo "$COMPONENT" | tr '[:upper:]' '[:lower:]'`
    docker build -t user/telemetry-$component .
done

exit 0

cd $DIRECTORY_APPLICATIONS

for COMPONENT in *
do
    cd $DIRECTORY_APPLICATIONS/$COMPONENT
    component=`echo "$COMPONENT" | tr '[:upper:]' '[:lower:]'`
    docker build -t user/a_$component .
done

# End of file
