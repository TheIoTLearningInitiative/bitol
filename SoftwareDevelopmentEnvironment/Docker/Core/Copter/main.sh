#!/bin/bash

# set -x

# =============================================================================
# Variables
# =============================================================================

ARDUPILOT=$HOME/ardupilot
ENVIRONMENTAL=/etc/profile

VEHICLEID=$1
LATITUDE=$2
LONGITUDE=$3
ALTITUDE=$4

# =============================================================================
# Functions
# =============================================================================

# None

# =============================================================================
# Main
# =============================================================================

PATH=$PATH:$HOME/ardupilot/Tools/autotest
PATH=/usr/lib/ccache:$PATH

. $ENVIRONMENTAL

cd $HOME/ardupilot/
echo "SYSID_THISMAV=${VEHICLEID}" | tee -a $ARDUPILOT/Tools/autotest/default_params/copter.parm
#sim_vehicle.py -v ArduCopter -l ${LATITUDE},${LONGITUDE},${ALTITUDE},0
sim_vehicle.py -v ArduCopter -l ${LATITUDE},${LONGITUDE},${ALTITUDE},0 --out=tcpin:127.0.0.1:5764
