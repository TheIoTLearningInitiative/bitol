#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================
# Libraries
# =============================================================================

from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil # Needed for command message definitions

from modules.altitude import *
from modules.arm import *
from modules.callbacks import *
from modules.hover import *
from modules.mode import *
from modules.ned import *
from modules.takeoff import *
from modules.yaw import *

import argparse
import time
import math
import sys

# =============================================================================
# Functions
# =============================================================================

def location_callback(self, attr_name, value):
    print("location_callback: %s" % vehicle.location.global_relative_frame)

def rangefinder_callback(self, attr_name, value):
    print("rangefinder_callback: %s" % vehicle.rangefinder.distance)

def mode_callback(self, attr_name, value):
    print("mode_callback: %s" % vehicle.mode.name)

# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Control Copter and send commands in GUIDED mode ')
    parser.add_argument('--connect',
                       help="Vehicle connection target string. If not specified, SITL automatically started and used.")
    parser.add_argument('--id',
                       help="Vehicle Identification")
    parser.add_argument('--altitude',
                       help="Vehicle Altitude")
    args = parser.parse_args()

    connection_string = args.connect
    vehicle_id = float(args.id)
    vehicle_altitude = float(args.altitude)
    mode_wait = 3
    command_wait = 10

    print('Connecting to vehicle on: %s' % connection_string)
    vehicle = connect(connection_string, wait_ready=False, baud=57600)
    time.sleep(1)

    #vehicle.add_attribute_listener('mode', mode_callback)
    #vehicle.add_attribute_listener('rangefinder', rangefinder_callback)
    #vehicle.add_attribute_listener('location', location_callback)

    arm_and_takeoff_nogps(vehicle, vehicle_mode="STABILIZED" ,vehicle_altitude=vehicle_altitude)

    #print "setting throttle channel to 1500 via channel overrides"
    #print(" Ch3: %s" % vehicle.channels['3'])
    #vehicle.channels.overrides['3'] = 1500
    #print(" Ch3: %s" % vehicle.channels['3'])
    #time.sleep(1)

    time.sleep(10)

    #mode(vehicle, mode="STABILIZED")
    #time.sleep(mode_wait)

    #vehicle.remove_attribute_listener('location', location_callback)
    #vehicle.remove_attribute_listener('rangefinder', rangefinder_callback)
    #vehicle.remove_attribute_listener('mode', mode_callback)

    #print "setting throttle channel to 1500 via channel overrides"
    #print(" Ch3: %s" % vehicle.channels['3'])
    #vehicle.channels.overrides['3'] = None
    #print(" Ch3: %s" % vehicle.channels['3'])
    #time.sleep(1)

    print("Setting LAND mode...")
    mode(vehicle, mode="LAND")
    time.sleep(mode_wait)

    print("Close vehicle object")
    vehicle.close()

    print("Completed")
