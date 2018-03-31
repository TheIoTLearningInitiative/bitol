#!/bin/bash

set -x

# =============================================================================
# Variables
# =============================================================================

export DIRECTORY_SOURCE=$HOME/src/

# =============================================================================
# Functions
# =============================================================================

# None

# =============================================================================
# Main
# =============================================================================

sudo apt-get update
sudo apt-get install -y python-matplotlib python-serial python-wxgtk3.0 python-wxtools python-lxml
sudo apt-get install -y python-scipy python-opencv ccache gawk git python-pip python-pexpect
sudo pip install future pymavlink MAVProxy

cat << EOM >> $HOME/.bashrc

export PATH=$PATH:$DIRECTORY_SOURCE/ardupilot/Tools/autotest
export PATH=/usr/lib/ccache:$PATH

EOM

source $HOME/.bashrc

if [ -d "$DIRECTORY_SOURCE" ]
then
    cd $DIRECTORY_SOURCE
else
    mkdir $DIRECTORY_SOURCE
fi

git clone git://github.com/ArduPilot/ardupilot.git
cd ardupilot
git submodule update --init --recursive

export PATH=$PATH:$DIRECTORY_SOURCE/ardupilot/Tools/autotest
export PATH=/usr/lib/ccache:$PATH

screen -dm -S sim_vehicle.py -v ArduCopter -l 20.654544,-103.3930971,30,0 &

cd $DIRECTORY_SOFTWAREDEVELOPMENTENVIRONMENT

# End of File
