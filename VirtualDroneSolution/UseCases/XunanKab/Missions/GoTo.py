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
# Init
# =============================================================================

parser = argparse.ArgumentParser(description='commands')
parser.add_argument('--connect')
parser.add_argument('--lat')
parser.add_argument('--long')
args = parser.parse_args()

connection_string = args.connect
lattitude = float(args.lat)
longitude = float(args.long)

print("Connection to the vehicle on %s" % connection_string)
vehicle = connect(connection_string, wait_ready=True)

# =============================================================================
# Functions
# =============================================================================

def arm_and_takeoff(tgt_altitude):
    print("Arming motors")
    
    while not vehicle.is_armable:
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
            
arm_and_takeoff(10)

vehicle.airspeed = 5
waypoint = LocationGlobalRelative(lattitude, longitude, 10)
vehicle.simple_goto(waypoint)
time.sleep(30)

vehicle.mode = VehicleMode("RTL")
time.sleep(20)
vehicle.close()
