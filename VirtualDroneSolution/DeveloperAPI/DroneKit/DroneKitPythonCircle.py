"""
simple_goto.py: GUIDED mode "simple goto" example (Copter Only)

The example demonstrates how to arm and takeoff in Copter and how to navigate to 
points using Vehicle.commands.goto.

Full documentation is provided at http://python.dronekit.io/examples/simple_goto.html
"""

import time
import math
import sys
from droneapi.lib import VehicleMode, Location, Command
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, LocationGlobal
from pymavlink import mavutil

vehicle = connect('udp:127.0.0.1:14551')

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print "Basic pre-arm checks"
    # Don't let the user try to fly autopilot is booting
    if vehicle.mode.name == "INITIALISING":
        print "Waiting for vehicle to initialise"
        time.sleep(1)
    while vehicle.gps_0.fix_type < 2:
        print "Waiting for GPS...:", vehicle.gps_0.fix_type
        time.sleep(1)

    print "Arming motors"
    # Copter should arm in GUIDED mode
    vehicle.mode    = VehicleMode("GUIDED")
    vehicle.armed   = True
    vehicle.flush()

    while not vehicle.armed:
        print " Waiting for arming..."
        time.sleep(1)

    print "Taking off!"
    #vehicle.commands.takeoff(aTargetAltitude) # Take off to target altitude
    vehicle.simple_takeoff(aTargetAltitude)
    vehicle.flush()
    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    #  after Vehicle.commands.takeoff will execute immediately).
    #while not api.exit:
    #    print " Altitude: ", vehicle.location.alt
    #    if vehicle.location.alt>=aTargetAltitude*0.95: #Just below target, in case of undershoot.
    #        print "Reached target altitude"
    #        break;
    #    time.sleep(1)

def goto(lat, long, alt):
    print "Going to %s,%s" % (long, lat)
    point = LocationGlobalRelative(lat, long, alt)
    vehicle.simple_goto(point)
    vehicle.flush()
    while True:
        print "Long: %s, Lang: %s" % (vehicle.location.lon, vehicle.location.lat)
        dist = math.sqrt(math.pow(math.fabs(vehicle.location.lon - long), 2) + math.pow(math.fabs(vehicle.location.lat - lat), 2))
        print "Distance to point: %s" % dist
    #    if dist <= 0.00005:
    #        print "Point reached"
    #        break;
    #    time.sleep(1)

def takePic(lat, lon, alt):
    dist = math.sqrt(math.pow(math.fabs(vehicle.location.lon - lon), 2) + math.pow(math.fabs(vehicle.location.lat - lat), 2))
    heading = -math.degrees(2 * math.acos((vehicle.location.lat - center_pos.lat) / dist))
    print "Pointing nose heading %s (towards %s,%s)" % (heading, lat, lon)
    msg = vehicle.message_factory.mission_item_encode(0, 0, 0,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
        mavutil.mavlink.MAV_CMD_CONDITION_YAW,
        2,
        0,
        heading,
        0,
        1,
        0,
        0, 0, 0)
    vehicle.send_mavlink(msg)
    #cmd = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
    #    mavutil.mavlink.MAV_CMD_DO_SET_ROI, 0, 0, 3, 0, 0, 0, lat, lon, alt)
    #vehicle.commands.clear()
    #vehicle.commands.add(cmd)
    vehicle.flush()
    time.sleep(6)


def launch():
    print "Waiting for location..."
    while vehicle.location.global_frame.lat == 0:
        time.sleep(0.1)
    home_coords = [vehicle.location.global_frame.lat,
                   vehicle.location.global_frame.lon]
    print home_coords
    while not vehicle.is_armable:
            time.sleep(.1)

# Home position (Helipad) should be 55.661946, 12.282617
arm_and_takeoff(20)

radius = 0.0001
observations = 20
radians_pr_observation = 2 * math.pi / observations
print radians_pr_observation
center_pos = Location(20.653544,-103.3920971)
altitude = 5

launch()

#vehicle.gimbal.target_location(vehicle.home_location)

sys.exit(0)

# experiment with LOITER mode
"""
goto(center_pos.lat, center_pos.lon, altitude)
time.sleep(5)
vehicle.parameters["WP_LOITER_RAD"] = 10
vehicle.mode = VehicleMode("LOITER")
vehicle.flush()
time.sleep(30)
"""

# fly in a circle around center_pos
for i in range(1, observations):
    point = Location(center_pos.lat + radius * math.cos(radians_pr_observation*i), center_pos.lon + radius * 2 * math.sin(radians_pr_observation*i))
    print "P%s: %s, %s" % (i, point.lat, point.lon)
    goto(point.lat, point.lon, altitude)
    #takePic(center_pos.lat, center_pos.lon, altitude)

print "Returning to Launch"
vehicle.mode    = VehicleMode("RTL")
vehicle.flush()
