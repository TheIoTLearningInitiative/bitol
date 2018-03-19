#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time, sys, argparse, math
from dronekit import connect, Command, LocationGlobal, VehicleMode, LocationGlobalRelative
 
import argparse  
parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='127.0.0.1:14551')
args = parser.parse_args()
 
# Connect to the Vehicle
print 'Connecting to vehicle on: %s' % args.connect
#vehicle = connect(args.connect, baud=57600, wait_ready=True, heartbeat_timeout=60)
vehicle = connect(args.connect, wait_ready=False)
 
print " Type: %s" % vehicle._vehicle_type
print " Armed: %s" % vehicle.armed
print " System status: %s" % vehicle.system_status.state
print " GPS: %s" % vehicle.gps_0
print " Alt: %s" % vehicle.location.global_relative_frame.alt
 
def PX4setMode(mavMode):
    vehicle._master.mav.command_long_send(vehicle._master.target_system, vehicle._master.target_component,
                                               mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0,
                                               mavMode,
                                               0, 0, 0, 0, 0, 0)
 
# Function to arm and then takeoff to a user specified altitude
def arm_and_takeoff(aTargetAltitude):
 
  print "Basic pre-arm checks"
  # Don't let the user try to arm until autopilot is ready
  #while not vehicle.is_armable:
    #print " Waiting for vehicle to initialise..."
    #time.sleep(1)
        #
  print "Arming motors"
  # Copter should arm in GUIDED mode
  #vehicle.mode    = VehicleMode("GUIDED")
  #vehicle.mode    = VehicleMode("POSCTL")
  MAV_MODE_AUTO   = 4
 
  PX4setMode(MAV_MODE_AUTO)
  time.sleep(1)
  vehicle.armed   = True
 
  while not vehicle.armed:
    print " Waiting for arming..."
    time.sleep(1)
 
  print "Taking off!"
  vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude
 
  home = vehicle.location.global_frame
  print home
  time.sleep(2)
 
  # Check that vehicle has reached takeoff altitude
  while True:
    try:
      print " Altitude: ", vehicle.location.global_relative_frame.alt 
      #Break and return from function just below target altitude.        
      if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: 
        print "Reached target altitude"
        break
      time.sleep(1)
    except KeyboardInterrupt:
      break
      #sys.exit()
 
 
# Initialize the takeoff sequence to 20m
arm_and_takeoff(20)
 
print("Take off complete")
 
# Hover for 10 seconds
time.sleep(10)
 
print("Now let's land")
#vehicle.mode = VehicleMode("LAND")
vehicle.mode = VehicleMode("RTL")
 
# Close vehicle object
vehicle.close()
