#!/bin/bash

set -x

# =============================================================================
# Variables
# =============================================================================

export SIMVEHICLE_PID=$$
export SIMVEHICLE_PID_PATH="/tmp/simvehicle"
export SIMVEHICLE_ARGUMENT_ACTION=$1

export DIRECTORY_SOURCE=$HOME/src/
export DIRECTORY_ARDUPILOT=$DIRECTORY_SOURCE/ardupilot

# =============================================================================
# Functions
# =============================================================================

# None

# =============================================================================
# Main
# =============================================================================

cd $HOME

if [ "$SIMVEHICLE_ARGUMENT_ACTION" = "start" ]; then
    echo $SIMVEHICLE_PID > $SIMVEHICLE_PID_PATH
    cd $DIRECTORY_ARDUPILOT
    source $HOME/.bashrc
    sim_vehicle.py -v ArduCopter -l $MAIN_LAT,$MAIN_LON,30,0
elif [ "$SIMVEHICLE_ARGUMENT_ACTION" = "stop" ]; then
    SIMVEHICLE_PID=`cat $SIMVEHICLE_PID_PATH`
    kill -- -$(ps -o pgid=$SIMVEHICLE_PID | grep -o [0-9]*)
fi

cd $HOME

# End Of File
