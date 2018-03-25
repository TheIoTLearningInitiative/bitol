#!/bin/sh

# set -x

# =============================================================================
# Variables
# =============================================================================

export MAIN_PID=$$
export MAIN_PID_PATH="/tmp/main"
export MAIN_DIRECTORY=`dirname "$(readlink -f "$0")"`

export JMAVSIM=$MAIN_DIRECTORY/VirtualDroneSolution/FlightCode/SoftwareInTheLoop/JMAVSim/
export SIMVEHICLE=$MAIN_DIRECTORY/VirtualDroneSolution/FlightCode/SoftwareInTheLoop/ArdupilotSitl/
export GROUNDCONTROLSTATION=$MAIN_DIRECTORY/VirtualDroneSolution/GroundControlStation/
export QGROUNDCONTROL=$MAIN_DIRECTORY/VirtualDroneSolution/GroundControlStation/QGroundControl/
export DRONEKIT=$MAIN_DIRECTORY/VirtualDroneSolution/DeveloperAPI/DroneKit/

# =============================================================================
# Functions
# =============================================================================

# None

# =============================================================================
# Main
# =============================================================================


# VirtualDroneSolution/FlightCode/SoftwareInTheLoop/
export PATH=$PATH:$JMAVSIM
export PATH=$PATH:$SIMVEHICLE

# VirtualDroneSolution/GroundControlStation/
export PATH=$PATH:$GROUNDCONTROLSTATION
export PATH=$PATH:$QGROUNDCONTROL

# VirtualDroneSolution/DeveloperAPI/DroneKit/
export PATH=$PATH:$DRONEKIT

# End Of File
