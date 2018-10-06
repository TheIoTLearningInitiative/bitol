#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Thanks Tiziano Fiorenzani for teaching us!
https://github.com/tizianofiorenzani

This script will introduce multiple things:
- Run the simulator inside dronekit
- Read and handle telemetry from the UAV
- Read and change parameters
"""

# =============================================================================
# Libraries
# =============================================================================

import argparse
import re
import time

from dronekit import connect, VehicleMode

# =============================================================================
# Functions
# =============================================================================

# None

# =============================================================================
# Main
# =============================================================================

# =============================================================================
# Init
# =============================================================================


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='commands')
    parser.add_argument('--connect')
    parser.add_argument('--id')
    args = parser.parse_args()

    connection_string = args.connect
    vehicleid = float(args.id)

    print("Connection to the vehicle on %s" % connection_string)
    vehicle = connect(connection_string, wait_ready=True)
    vehicle.wait_ready('autopilot_version')
    print('Autopilot Version: %s' % vehicle.version)

    if re.search(r'PX4*', str(vehicle.version)):
        print("Vehicle ID Old: %d" % vehicle.parameters['MAV_SYS_ID'])
        vehicle.parameters['MAV_SYS_ID'] = vehicleid
        time.sleep(1)
        print("Vehicle ID New: %d" % vehicle.parameters['MAV_SYS_ID'])
        time.sleep(1)
    else:
        print("Vehicle ID Old: %d" % vehicle.parameters['SYSID_THISMAV'])
        vehicle.parameters['SYSID_THISMAV'] = vehicleid
        time.sleep(1)
        print("Vehicle ID New: %d" % vehicle.parameters['SYSID_THISMAV'])
        time.sleep(1)

    print("Vehicle ID: %d" % vehicle.parameters['SYSID_THISMAV'])
    vehicle.close()
