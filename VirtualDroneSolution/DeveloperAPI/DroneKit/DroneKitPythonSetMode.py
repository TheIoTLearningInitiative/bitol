#!/usr/bin/python

connection_string = '127.0.0.1:5501'

# Import DroneKit-Python
from dronekit import connect, VehicleMode
from pymavlink import mavutil

def set_mode(flightmode):
    # create the MAV_CMD_DO_SET_MODE command
    msg = vehicle.message_factory.command_long_encode(
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_CMD_DO_SET_MODE, #command
        0, #confirmation
        flightmode,
        0, 0, 0, 0, 0, 0 )
    # send command to vehicle
    vehicle.send_mavlink(msg)

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

set_mode(20)

print " Mode: %s" % vehicle.mode.name

# Close vehicle object before exiting script
vehicle.close()

print("Completed")
