#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Thanks Tiziano Fiorenzani for teaching us!
# https://github.com/tizianofiorenzani

# =============================================================================
# Libraries
# =============================================================================

import argparse
import math
import time

from dronekit import connect, Command, LocationGlobal, VehicleMode
from pymavlink import mavutil

# =============================================================================
# Functions
# =============================================================================

def arm_and_wait(tgt_altitude):
    print("Arming motors")

    while not vehicle.is_armable:
        time.sleep(1)

    while vehicle.gps_0.fix_type < 2:
        print "Waiting for GPS...:", vehicle.gps_0.fix_type
        time.sleep(1)

    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        time.sleep(1)

    print("Takeoff")
    vehicle.simple_takeoff(tgt_altitude)

    while True:
        altitude = vehicle.location.global_relative_frame.alt
        if altitude >= tgt_altitude -1:
            print("Altitude reached")
            break

        time.sleep(1)

def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.
    This method is an approximation, and will not be accurate over large distances and close to the 
    earth's poles. It comes from the ArduPilot test code: 
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='commands')
    parser.add_argument('--connect')
    parser.add_argument('--id')
    parser.add_argument('--alt')
    args = parser.parse_args()

    connection_string = args.connect
    vehicleid = float(args.id)
    altitude = float(args.alt)

    print("Connection to the vehicle on %s" % connection_string)
    vehicle = connect(connection_string, wait_ready=True)
    vehicle.parameters['SYSID_THISMAV'] = vehicleid

    cmds = vehicle.commands
    print cmds

    #vehicle.home_location=vehicle.location.global_frame
    #while not vehicle.home_location:
    #    cmds = vehicle.commands
    #    cmds.download()
    #    cmds.wait_ready()
    #    if not vehicle.home_location:
    #        print " Waiting for home location ..."
    print "Home location: %s" % vehicle.home_location
    time.sleep(5)

    #home = vehicle.location.global_relative_frame
    #print home

    print "\nSet Vehicle.mode = RTL (currently: %s)" % vehicle.mode.name
    vehicle.mode = VehicleMode("RTL")
    while not vehicle.mode.name=='RTL':
        print " Waiting for mode change ..."

    #vehicle.home_location=vehicle.location.global_frame
    #print "Get new home location"
    #cmds = vehicle.commands
    #cmds.download()
    #cmds.wait_ready()
    #print " Home Location: %s" % vehicle.home_location

    vehicle.close()
