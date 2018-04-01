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

sudo apt-get update
sudo apt-get upgrade
sudo apt-get autoremove

sudo apt-get remove -y modemmanager
sudo usermod -a -G dialout $USER

# wget -O - https://raw.githubusercontent.com/PX4/Devguide/master/build_scripts/ubuntu_sim_nuttx.sh | bash
wget https://raw.githubusercontent.com/PX4/Devguide/master/build_scripts/ubuntu_sim_nuttx.sh
bash ubuntu_sim_nuttx.sh

cd $DIRECTORY_SOFTWAREDEVELOPMENTENVIRONMENT

# End of File
