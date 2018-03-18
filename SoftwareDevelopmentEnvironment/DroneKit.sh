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

cd $HOME

sudo apt install -y python-pip python-dev
sudo pip install dronekit
sudo pip install dronekit-sitl -UI

cd $DIRECTORY_SOURCE

git clone https://github.com/dronekit/dronekit-python.git
cd dronekit-python
python setup.py build
sudo python setup.py install

cd $HOME

# End of File
