#!/bin/bash

# set -x

# =============================================================================
# Variables
# =============================================================================

ARDUPILOT = $HOME/ardupilot
ENVIRONMENTAL = /etc/profile

VEHICLEID = $1

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

echo SYSID_THISMAV=$1 | tee -a $ARDUPILOT/Tools/autotest/default_params/plane.parm
screen sim_vehicle.py -v ArduCopter -l $LATITUDE,$LONGITUDE,$ALTTITUDE,0
