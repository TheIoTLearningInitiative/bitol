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

sudo apt update -y
sudo apt install -y build-essential python-pip python-dev
sudo apt install -y python-cherrypy3
sudo apt install -y python-matplotlib
sudo apt install -y python-gps gpsd gpsd-clients

sudo pip install pip --upgrade
sudo pip install sphinx monotonic future nose mock sphinx-3dr-theme
sudo pip install pymavlink
sudo pip install dronekit
sudo pip install dronekit-sitl -UI

cd $DIRECTORY_SOURCE

git clone https://github.com/dronekit/dronekit-python.git
cd dronekit-python
python setup.py build
sudo python setup.py install

cd $DIRECTORY_SOFTWAREDEVELOPMENTENVIRONMENT

# End of File
