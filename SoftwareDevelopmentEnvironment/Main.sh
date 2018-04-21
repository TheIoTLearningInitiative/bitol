#!/bin/bash

set -x

# =============================================================================
# Variables
# =============================================================================

export DIRECTORY_BITOL=$HOME/Bitol/
export DIRECTORY_SOFTWAREDEVELOPMENTENVIRONMENT=$DIRECTORY_BITOL/SoftwareDevelopmentEnvironment/
sh_c='sudo -E sh -c'

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

$sh_c apt-get update -y
$sh_c apt-get upgrade -y
$sh_c apt-get autoremove -y

$sh_c apt install -y tree
$sh_c apt install -y jstest-gtk

$sh_c apt install -y git
$sh_c apt install -y nmap
$sh_c apt install -y screen

$sh_c pip install --upgrade pip

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

exit 0

bash OpenCV.sh
bash PX4.sh
bash MAVLink.sh
bash Ardupilot.sh
bash SITLSimulator.sh
bash DroneKit.sh
# bash DroneCore.sh
bash QGroundControl.sh
bash APMPLanner.sh
bash GStreamer.sh
bash JMAVSim.sh

cd $HOME

echo "Software Development Environment :: Completed"

# End of File
