#!/bin/bash

set -x

# =============================================================================
# Variables
# =============================================================================

export DIRECTORY_BITOL=$HOME/Bitol/
export DIRECTORY_SOFTWAREDEVELOPMENTENVIRONMENT=$DIRECTORY_BITOL/SoftwareDevelopmentEnvironment/
export DIRECTORY_DOCKER=$DIRECTORY_SOFTWAREDEVELOPMENTENVIRONMENT/Docker/

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

$sh_c apt-get install -y tree
$sh_c apt-get install -y jstest-gtk

$sh_c apt-get install -y git
$sh_c apt-get install -y nmap
$sh_c apt-get install -y screen

$sh_c pip install --upgrade pip

if [ -d "$DIRECTORY_BITOL" ]
then
    cd $DIRECTORY_BITOL
    git pull
else
    git clone https://github.com/TheIoTLearningInitiative/Bitol.git
fi

cd $DIRECTORY_DOCKER

bash build.sh -c all

echo "Software Development Environment :: Completed"

# End of File
