#!/bin/bash

set -x

# =============================================================================
# Variables
# =============================================================================

export DIRECTORY_DOWNLOADS=$HOME/Downloads/

# =============================================================================
# Functions
# =============================================================================

# None

# =============================================================================
# Main
# =============================================================================

cd $HOME

cd $DIRECTORY_DOWNLOADS
wget http://firmware.ardupilot.org/Tools/APMPlanner/apm_planner_2.0.24_xenial64.deb
sudo dpkg -i apm_planner*.deb
sudo apt-get -f install
sudo dpkg -i apm_planner*.deb

cd $HOME

# End of File
