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

def attitude_callback(self, attr_name, value):
    print(vehicle.attitude)

def arm_and_wait(aTargetTime):
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
    sitl = None

    # Start SITL if no connection string specified
    if not connection_string:
        import dronekit_sitl
        sitl = dronekit_sitl.start_default()
        connection_string = sitl.connection_string()

    # Connect to the Vehicle
    print('Connecting to vehicle on: %s' % connection_string)
    vehicle = connect(connection_string, wait_ready=True)

    vehicle.parameters['SYSID_THISMAV'] = vehicleid
    print " Type: %s" % vehicle._vehicle_type
    print " Armed: %s" % vehicle.armed
    print " System status: %s" % vehicle.system_status.state
    print " GPS: %s" % vehicle.gps_0
    print " Alt: %s" % vehicle.location.global_relative_frame.alt

    vehicle.add_attribute_listener('attitude', attitude_callback)

    cmds = vehicle.commands
    cmds.clear()
    cmds.upload()

    # Initialize the takeoff sequence to 20m
    arm_and_wait(5)

    print("Arm and wait complete")

    vehicle.remove_attribute_listener('attitude', attitude_callback)

    # Close vehicle object
    vehicle.close()

    # Shut down simulator if it was started.
    if sitl:
        sitl.stop()
