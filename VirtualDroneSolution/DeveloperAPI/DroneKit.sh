#!/bin/sh

set -x

# =============================================================================
# Variables
# =============================================================================

export DRONEKIT_PID=$$
export DRONEKIT_PID_PATH=$HOME/dronekit
export DRONEKIT_ARGUMENT_ACTION=$1
export DRONEKIT_DIRECTORY=$HOME/Bitol/VirtualDroneSolution/DeveloperApi/
export DRONEKIT_PX4=$DRONEKIT_DIRECTORY/DroneKitPythonPx4.py

# =============================================================================
# Functions
# =============================================================================

# None

# =============================================================================
# Main
# =============================================================================

cd $HOME

if [ "$DRONEKIT_ARGUMENT_ACTION" = "start" ]; then
    echo $DRONEKIT_PID > $DRONEKIT_PID_PATH
    JMAVSim.sh start &
    sleep 1
    QGroundControl.sh start &
    sleep 3
    python $DRONEKIT_PX4
elif [ "$DRONEKIT_ARGUMENT_ACTION" = "stop" ]; then
    QGroundControl.sh stop &
    sleep 1
    JMAVSim.sh stop &
    sleep 1
    DRONEKIT_PID=`cat $DRONEKIT_PID_PATH`
    kill -- -$(ps -o pgid=$DRONEKIT_PID | grep -o [0-9]*)
fi

cd $HOME

# End Of File
