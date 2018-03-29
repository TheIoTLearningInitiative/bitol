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

sudo apt-get update -y
sudo apt-get -y install cmake build-essential colordiff astyle git libcurl4-openssl-dev doxygen

cd $DIRECTORY_SOURCE
git clone https://github.com/dronecore/DroneCore.git
cd DroneCore
git checkout master
git submodule update --init --recursive
make default

# Building Error!

cd $DIRECTORY_SOFTWAREDEVELOPMENTENVIRONMENT

# End of File
