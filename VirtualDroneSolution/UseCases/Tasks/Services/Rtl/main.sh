#!/bin/bash

set -x

# =============================================================================
# Variables
# =============================================================================

IPADDRESS=$1
PORT=$2
VEHICLEID=$3
ALTITUDE=$4
SPEED=$5

# =============================================================================
# Functions
# =============================================================================

# None

# =============================================================================
# Main
# =============================================================================

cd $HOME/
python rtl.py --connect=${IPADDRESS}:${PORT} --id=${VEHICLEID} \
              --alt=${ALTITUDE} --speed=${SPEED}
