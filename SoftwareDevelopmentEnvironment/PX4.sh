#!/bin/bash

set -x

# =============================================================================
# Variables
# =============================================================================

# None

# =============================================================================
# Functions
# =============================================================================

# None

# =============================================================================
# Main
# =============================================================================

cd $HOME

sudo apt-get update
sudo apt-get upgrade
sudo apt-get autoremove

sudo apt-get remove -y modemmanager
sudo usermod -a -G dialout $USER

wget -O - https://raw.githubusercontent.com/PX4/Devguide/master/build_scripts/ubuntu_sim_nuttx.sh | bash

cd $HOME

# End of File
