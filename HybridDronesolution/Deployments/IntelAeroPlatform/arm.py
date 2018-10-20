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

def arm_and_wait(mode, aTargetTime):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    #while not vehicle.is_armable:
    #    print(" Waiting for vehicle to initialise...")
    #    time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode(mode)
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

    parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
    parser.add_argument('--connect',
                        help="Vehicle connection target string. If not specified, SITL automatically started and used.")
    parser.add_argument('--id')
    args = parser.parse_args()

    connection_string = args.connect
    vehicleid = float(args.id)
    sitl = None

    print('Connecting to vehicle on: %s' % connection_string)
    vehicle = connect(connection_string, wait_ready=False)

    print " Type: %s" % vehicle._vehicle_type
    print " Armed: %s" % vehicle.armed
    print " System status: %s" % vehicle.system_status.state
    print " GPS: %s" % vehicle.gps_0
    print " Alt: %s" % vehicle.location.global_relative_frame.alt

    #vehicle.parameters['MAV_SYS_ID'] = vehicleid
    #print " Sys Id: %s" % vehicle.parameters['MAV_SYS_ID']

    #for property, value in vars(vehicle.parameters).iteritems():
    #    print property, ": ", value

    #cmds = vehicle.commands
    #cmds.clear()
    #cmds.upload()

    arm_and_wait("STABILIZED", 5)

    vehicle.mode = VehicleMode("STABILIZED")
    vehicle.armed = False
    while vehicle.armed:
        print(" Waiting for disarming...")
        time.sleep(1)

    vehicle.close()
