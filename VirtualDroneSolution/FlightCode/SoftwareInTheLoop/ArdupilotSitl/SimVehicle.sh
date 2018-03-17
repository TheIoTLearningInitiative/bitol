#!/bin/bash

set -x

# =============================================================================
# Variables
# =============================================================================

export SIMVEHICLE_PID=$$
export SIMVEHICLE_PID_PATH="/tmp/simvehicle"
export SIMVEHICLE_ARGUMENT_ACTION=$1

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
    sim_vehicle.py -v ArduCopter -l 20.654544,-103.3930971,30,0
elif [ "$SIMVEHICLE_ARGUMENT_ACTION" = "stop" ]; then
    SIMVEHICLE_PID=`cat $SIMVEHICLE_PID_PATH`
    kill -- -$(ps -o pgid=$SIMVEHICLE_PID | grep -o [0-9]*)
fi

cd $HOME

# End Of File
