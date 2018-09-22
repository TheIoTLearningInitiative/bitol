#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================
# Libraries
# =============================================================================

import argparse
import math
import re
import sys
import time

from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil

from dronekit import connect, Command, LocationGlobal, VehicleMode, LocationGlobalRelative

# =============================================================================
# Functions
# =============================================================================

def altitude_callback(self, attr_name, value):
    print("Altitude: %s" % vehicle.location.global_relative_frame.alt)

def arm_and_takeoff(tgt_altitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    while vehicle.gps_0.fix_type < 2:
        print "Waiting for GPS...:", vehicle.gps_0.fix_type
        time.sleep(1)

    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Takeoff")
    vehicle.simple_takeoff(tgt_altitude)

    while True:
        altitude = vehicle.location.global_relative_frame.alt
        if altitude >= tgt_altitude -1:
            print("Altitude reached")
            break

        time.sleep(1)

# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':

    # Set up option parsing to get connection string
    parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
    parser.add_argument('--connect',
                        help="Vehicle connection target string. If not specified, SITL automatically started and used.")
    parser.add_argument('--id')
    parser.add_argument('--alt')
    args = parser.parse_args()

    connection_string = args.connect
    vehicleid = float(args.id)
    altitude = float(args.alt)
    sitl = None

    # Start SITL if no connection string specified
    if not connection_string:
        import dronekit_sitl
        sitl = dronekit_sitl.start_default()
        connection_string = sitl.connection_string()

    # Connect to the Vehicle
    print('Connecting to vehicle on: %s' % connection_string)
    vehicle = connect(connection_string, wait_ready=True)

    #if re.search(r'PX4*', str(vehicle.version)):
    #    print vehicle.parameters['MAV_SYS_ID']
    #    time.sleep(5)
    #    vehicle.parameters['MAV_SYS_ID'] = vehicleid
    #else:
    #    vehicle.parameters['SYSID_THISMAV'] = vehicleid
    print " Type: %s" % vehicle._vehicle_type
    print " Armed: %s" % vehicle.armed
    print " System status: %s" % vehicle.system_status.state
    print " GPS: %s" % vehicle.gps_0
    print " Alt: %s" % vehicle.location.global_relative_frame.alt

    vehicle.add_attribute_listener('location', altitude_callback)

    # Get Vehicle Home location - will be `None` until first set by autopilot
    #while not vehicle.home_location:
    #    cmds = vehicle.commands
    #    cmds.download()
    #    cmds.wait_ready()
    #    if not vehicle.home_location:
    #        print " Waiting for home location ..."

    # We have a home location.
    print "Home location: %s" % vehicle.home_location

    # Initialize the takeoff sequence
    arm_and_takeoff(altitude)

    time.sleep(5)

    vehicle.mode = VehicleMode("LAND")
    while vehicle.armed:
        print(" Waiting for disarming...")
        time.sleep(1)

    vehicle.remove_attribute_listener('location', altitude_callback)

    # Close vehicle object
    vehicle.close()

    # Shut down simulator if it was started.
    if sitl:
        sitl.stop()
