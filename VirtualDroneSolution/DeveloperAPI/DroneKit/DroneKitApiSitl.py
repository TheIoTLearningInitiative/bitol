#!/usr/bin/python

import dronekit_sitl

print "Start DroneKit Simulator (SITL)"
sitl = dronekit_sitl.start_default()
#connection_string = sitl.connection_string()
connection_string = '127.0.0.1:14550'

# Import DroneKit-Python
from dronekit import connect, VehicleMode

# Connect to the Vehicle.
print("Connecting to vehicle on: %s" % (connection_string,))
vehicle = connect(connection_string, wait_ready=True)

# Get some vehicle attributes (state)
print "Get some vehicle attribute values:"
print " Autopilot Firmware version: %s" % vehicle.version
print " Autopilot capabilities (supports ftp): %s" % vehicle.capabilities.ftp
print " Global Location: %s" % vehicle.location.global_frame
print " Global Location (relative altitude): %s" % vehicle.location.global_relative_frame
print " Local Location: %s" % vehicle.location.local_frame
print " Attitude: %s" % vehicle.attitude
print " Velocity: %s" % vehicle.velocity
print " GPS: %s" % vehicle.gps_0
print " Groundspeed: %s" % vehicle.groundspeed
print " Airspeed: %s" % vehicle.airspeed
print " Gimbal status: %s" % vehicle.gimbal
print " Battery: %s" % vehicle.battery
print " EKF OK?: %s" % vehicle.ekf_ok
print " Last Heartbeat: %s" % vehicle.last_heartbeat
print " Rangefinder: %s" % vehicle.rangefinder
print " Rangefinder distance: %s" % vehicle.rangefinder.distance
print " Rangefinder voltage: %s" % vehicle.rangefinder.voltage
print " Heading: %s" % vehicle.heading
print " Armed: %s" % vehicle.armed
print " Is Armable?: %s" % vehicle.is_armable
print " System status: %s" % vehicle.system_status.state
print " Mode: %s" % vehicle.mode.name

# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
print("Stop DroneKit Simulator (SITL)")
sitl.stop()

print("Completed")
