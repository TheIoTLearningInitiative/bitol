#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================
# Libraries
# =============================================================================

import argparse
import math
import sys
import time

from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil

from dronekit import connect, Command, LocationGlobal, VehicleMode, LocationGlobalRelative

# =============================================================================
# Functions
# =============================================================================

def arm_and_wait(aTargetTime):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    #print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    #while not vehicle.is_armable:
    #    print(" Waiting for vehicle to initialise...")
    #    time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("STABILIZE")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Wait!")
    time.sleep(5)

# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':

    # Set up option parsing to get connection string
    parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
    parser.add_argument('--connect',
                        help="Vehicle connection target string. If not specified, SITL automatically started and used.")
    parser.add_argument('--id')
    args = parser.parse_args()

    connection_string = args.connect
    vehicleid = float(args.id)

    print('Connecting to vehicle on: %s' % connection_string)
    vehicle = connect(connection_string, wait_ready=False, baud=57600)

    #vehicle.parameters['MAV_SYS_ID'] = vehicleid
    #vehicle.parameters['SYSID_THISMAV'] = vehicleid
    print " Type: %s" % vehicle._vehicle_type
    print " Armed: %s" % vehicle.armed
    print " System status: %s" % vehicle.system_status.state
    print " GPS: %s" % vehicle.gps_0
    print " Alt: %s" % vehicle.location.global_relative_frame.alt
    #print " Vehicle Id: %s" % vehicle.parameters['MAV_SYS_ID']

    cmds = vehicle.commands
    cmds.clear()
    cmds.upload()

    arm_and_wait(1)

    while vehicle.armed:
        print(" Waiting for disarming...")
        time.sleep(1)

    vehicle.close()

