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

cd $HOME

source $HOME/.bashrc
cd $DIRECTORY_ARDUCOPTER
sim_vehicle.py -w

cd $HOME

# End of File
