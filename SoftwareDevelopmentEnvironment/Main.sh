#!/bin/bash

set -x

# =============================================================================
# Variables
# =============================================================================

export DIRECTORY_BITOL=$HOME/Bitol/
export DIRECTORY_SOFTWAREDEVELOPMENTENVIRONMENT=$DIRECTORY_BITOL/SoftwareDevelopmentEnvironment/

# =============================================================================
# Functions
# =============================================================================

# None

# =============================================================================
# Main
# =============================================================================

# wget -O - https://raw.githubusercontent.com/TheIoTLearningInitiative/Bitol/master/SoftwareDevelopmentEnvironment/Main.sh | bash

echo "Software Development Environment :: Started"

cd $HOME

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get autoremove -y

sudo apt install -y tree
sudo apt install -y jstest-gtk

sudo apt install -y git
sudo apt install -y nmap
sudo apt install -y screen

if [ -d "$DIRECTORY_BITOL" ]
then
    cd $DIRECTORY_BITOL
    git pull
else
    git clone https://github.com/TheIoTLearningInitiative/Bitol.git
fi

# cat << EOM >> $HOME/.bashrc
# source $HOME/Bitol/Main.sh
# EOM

# source $HOME/.bashrc

cd $DIRECTORY_SOFTWAREDEVELOPMENTENVIRONMENT

#bash OpenCV.sh
#bash PX4.sh
bash MAVLink.sh
bash Ardupilot.sh
bash SITLSimulator.sh
bash DroneKit.sh
# bash DroneCore.sh
bash QGroundControl.sh
bash APMPLanner.sh
bash GStreamer.sh
#bash JMAVSim.sh

cd $HOME

echo "Software Development Environment :: Completed"

# End of File
