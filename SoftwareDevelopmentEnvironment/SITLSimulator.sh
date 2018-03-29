#!/bin/bash

set -x

# =============================================================================
# Variables
# =============================================================================

export DIRECTORY_SOURCE=$HOME/src/
export DIRECTORY_ARDUPILOT=$DIRECTORY_SOURCE/ardupilot/
export DIRECTORY_ARDUCOPTER=$DIRECTORY_ARDUPILOT/ArduCopter

# =============================================================================
# Functions
# =============================================================================

# None

# =============================================================================
# Main
# =============================================================================

source $HOME/.bashrc
cd $DIRECTORY_ARDUCOPTER
screen -dm -S sim_vehicle.py -v ArduCopter -l 20.6546009,-103.3915602,30,0

sleep 15

cd $DIRECTORY_SOFTWAREDEVELOPMENTENVIRONMENT

# End of File
