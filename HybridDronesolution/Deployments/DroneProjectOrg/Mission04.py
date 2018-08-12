#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Thanks Tiziano Fiorenzani for teaching us!
# https://github.com/tizianofiorenzani

# =============================================================================
# Libraries
# =============================================================================

import argparse
import time

from dronekit import connect, VehicleMode, LocationGlobalRelative

# =============================================================================
# Functions
# =============================================================================

def arm_and_takeoff(tgt_altitude):
    print("Arming motors")

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

    print("Connection to the vehicle on %s" % connection_string)
    vehicle = connect(connection_string, wait_ready=True)

    vehicle.parameters['SYSID_THISMAV'] = vehicleid
    arm_and_takeoff(altitude)

    vehicle.airspeed = 15
    waypoint = LocationGlobalRelative(latitude, longitude, altitude)
    vehicle.simple_goto(waypoint)
    time.sleep(30)

    vehicle.parameters['RTL_ALT'] = 5
    vehicle.mode = VehicleMode("RTL")
    time.sleep(20)
    vehicle.close()
