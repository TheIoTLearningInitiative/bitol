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

    if vehicle.armed and vehicle.location.global_relative_frame.alt > 2:
        print "\n\tVehicle armed and possible flying, aborting take off!\n"
        return

    #print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    #while not vehicle.is_armable:
    #    print(" Waiting for vehicle to initialise...")
    #    time.sleep(1)
    print "Basic pre-arm checks"
    # Don't let the user try to fly autopilot is booting
    if vehicle.mode.name == "INITIALISING":
        print "Waiting for vehicle to initialise"
        time.sleep(1)

    vehicle.mode = VehicleMode("STABILIZE")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Takeoff")
    vehicle.simple_takeoff(tgt_altitude)

    #while True:
    #    altitude = vehicle.location.global_relative_frame.alt
    #    if altitude >= tgt_altitude -1:
    #        print("Altitude reached")
    #        break
    #     time.sleep(1)

    try:
        while vehicle.mode.name=="ALT_HOLD":
            print " -> Alt:", vehicle.location.global_relative_frame.alt
            if abs(vehicle.location.global_relative_frame.alt-tgt_altitude) < 0.05: 
                print "\n\tReached %0.1f m\n" % (tgt_altitude)
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print "Keyboard Interrupt on arm_and_takeoff."
        pass # do cleanup here

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

    print('Connecting to vehicle on: %s' % connection_string)
    #vehicle = connect(connection_string, wait_ready=False)
    vehicle = connect(connection_string, wait_ready=False, baud=57600)

    #vehicle.parameters['MAV_SYS_ID'] = vehicleid
    #vehicle.parameters['SYSID_THISMAV'] = vehicleid
    print " Type: %s" % vehicle._vehicle_type
    print " Armed: %s" % vehicle.armed
    print " System status: %s" % vehicle.system_status.state
    print " GPS: %s" % vehicle.gps_0
    print " Alt: %s" % vehicle.location.global_relative_frame.alt

    vehicle.add_attribute_listener('location', altitude_callback)

    print "Home location: %s" % vehicle.home_location

    arm_and_takeoff(altitude)

    time.sleep(1)

    vehicle.mode = VehicleMode("LAND")
    while vehicle.armed:
        print(" Waiting for disarming...")
        time.sleep(1)

    vehicle.remove_attribute_listener('location', altitude_callback)

    vehicle.close()
