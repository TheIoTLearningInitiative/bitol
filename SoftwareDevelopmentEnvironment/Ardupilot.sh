#!/bin/bash

set -x

# =============================================================================
# Variables
# =============================================================================

export DIRECTORY_SOURCE=$HOME/src/
export DIRECTORY_ARDUPILOT=$DIRECTORY_SOURCE/ardupilot/

# =============================================================================
# Functions
# =============================================================================

# None

# =============================================================================
# Main
# =============================================================================

cd $HOME

sudo apt-get install -y python-matplotlib python-serial python-wxgtk3.0 python-wxtools python-lxml
sudo apt-get install -y python-scipy python-opencv ccache gawk git python-pip python-pexpect
sudo pip install future pymavlink MAVProxy

cat << EOM >> $HOME/.bashrc

export PATH=$PATH:$DIRECTORY_SOURCE/ardupilot/Tools/autotest
export PATH=/usr/lib/ccache:$PATH

EOM

source $HOME/.bashrc

cd $DIRECTORY_SOURCE
git clone git://github.com/ArduPilot/ardupilot.git
cd $DIRECTORY_ARDUPILOT
git submodule update --init --recursive

nohup sim_vehicle.py -v ArduCopter -l 20.654544,-103.3930971,30,0 &

cd $HOME

# End of File
