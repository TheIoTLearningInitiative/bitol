#!/bin/bash

set -x

# =============================================================================
# Variables
# =============================================================================

IPADDRESS=$1
PORT=$2
VEHICLEID=$3
LATITUDE=$4
LONGITUDE=$5
ALTITUDE=$6

# =============================================================================
# Functions
# =============================================================================

# None

# =============================================================================
# Main
# =============================================================================

cd $HOME/
python circular.py --connect=tcp:${IPADDRESS}:${PORT} --id=${VEHICLEID} \
               --lat=${LATITUDE} --lon=${LONGITUDE} --alt=${ALTITUDE} 
