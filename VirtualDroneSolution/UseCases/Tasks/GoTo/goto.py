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

from dronekit import connect, VehicleMode, LocationGlobalRelative

# =============================================================================
# Functions
# =============================================================================

def arm_and_takeoff(tgt_altitude):
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
    parser.add_argument('--lat')
    parser.add_argument('--long')
    parser.add_argument('--alt')
    args = parser.parse_args()

    connection_string = args.connect
    vehicleid = float(args.id)
    latitude = float(args.lat)
    longitude = float(args.long)
    altitude = float(args.alt)

    remainingdistance=0

    print("Connection to the vehicle on %s" % connection_string)
    vehicle = connect(connection_string, wait_ready=True)
    vehicle.parameters['SYSID_THISMAV'] = vehicleid

    while not vehicle.home_location:
        cmds = vehicle.commands
        cmds.download()
        cmds.wait_ready()
        if not vehicle.home_location:
            print " Waiting for home location ..."
    print "Home location: %s" % vehicle.home_location

    arm_and_takeoff(altitude)

    # Get the set of commands from the vehicle
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()

    waypoint = LocationGlobalRelative(latitude, longitude, altitude)
    distancetowaypoint = get_distance_metres(vehicle.location.global_frame, waypoint)
    print "Distance to waypoint: ", distancetowaypoint

    vehicle.simple_goto(waypoint)

    while vehicle.mode.name=='GUIDED':
        remainingdistance = get_distance_metres(vehicle.location.global_frame, waypoint)
        print "Remaining distance to waypoint", remainingdistance
        if remainingdistance <= 1:
            break

    print "\nSet Vehicle.mode = GUIDED (currently: %s)" % vehicle.mode.name 
    vehicle.mode = VehicleMode("GUIDED")
    while not vehicle.mode.name=='GUIDED':
        print " Waiting for mode change ..."

    vehicle.close()
