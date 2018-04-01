#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Thanks Tiziano Fiorenzani for teaching us!
https://github.com/tizianofiorenzani

Drone Delivery: We are going to build a mission in mission planner, upload the mission to the drone.
The script will connect with the vehicle and check if a new mission has been uploaded. 
As soon as a valid mission is available, we takeoff in GUIDED mode and then we switch
to AUTO. When the mission is completed we command to co back to home and land
"""

import time
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, LocationGlobal
from pymavlink import mavutil

def arm_and_takeoff(altitude):

   while not vehicle.is_armable:
      print("waiting to be armable")
      time.sleep(1)

   print("Arming motors")
   vehicle.mode = VehicleMode("GUIDED")
   vehicle.armed = True

   while not vehicle.armed: 
      time.sleep(1)

   print("Taking Off")
   vehicle.simple_takeoff(altitude)

   while True:
      v_alt = vehicle.location.global_relative_frame.alt
      print(">> Altitude = %.1f m"%v_alt)
      if v_alt >= altitude - 1.0:
          print("Target altitude reached")
          break
      time.sleep(1)

def clear_mission(vehicle):
    cmds = vehicle.commands
    vehicle.commands.clear()
    vehicle.flush()

    # After clearing the mission you MUST re-download the mission from the vehicle
    # before vehicle.commands can be used again
    # (see https://github.com/dronekit/dronekit-python/issues/230)
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()

def download_mission(vehicle):
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready() # wait until download is complete.
    

def get_current_mission(vehicle):
    print "Downloading mission"
    download_mission(vehicle)
    missionList = []
    n_WP        = 0
    for wp in vehicle.commands:
        missionList.append(wp)
        n_WP += 1 
        
    return n_WP, missionList
    

def add_last_waypoint_to_mission(
        vehicle,
        wp_Last_Latitude,
        wp_Last_Longitude,
        wp_Last_Altitude):

    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()

    missionlist=[]
    for cmd in cmds:
        missionlist.append(cmd)

    wpLastObject = Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, 
                           wp_Last_Latitude, wp_Last_Longitude, wp_Last_Altitude)
    missionlist.append(wpLastObject)

    cmds.clear()

    for cmd in missionlist:
        cmds.add(cmd)
    cmds.upload()
    
    return (cmds.count)    

def ChangeMode(vehicle, mode):
    while vehicle.mode != VehicleMode(mode):
            vehicle.mode = VehicleMode(mode)
            time.sleep(0.5)
    return True

gnd_speed = 10 # [m/s]
mode      = 'GROUND'

print('Connecting...')
vehicle = connect('udp:127.0.0.1:14551')
#vehicle = connect('tcp:127.0.0.1:5762', wait_ready=True)


while True:
    
    if mode == 'GROUND':
        n_WP, missionList = get_current_mission(vehicle)
        time.sleep(2)
        if n_WP > 0:
            print ("A valid mission has been uploaded: takeoff!")
            mode = 'TAKEOFF'
            
    elif mode == 'TAKEOFF':
       
        add_last_waypoint_to_mission(vehicle, vehicle.location.global_relative_frame.lat, 
                                       vehicle.location.global_relative_frame.lon, 
                                       vehicle.location.global_relative_frame.alt)
        print("Home waypoint added to the mission")
        time.sleep(1)
        arm_and_takeoff(10)
        
        print("Changing to AUTO")
        ChangeMode(vehicle,"AUTO")
        
        vehicle.groundspeed = gnd_speed
        mode = 'MISSION'
        print ("Swiitch mode to MISSION")
        
    elif mode == 'MISSION':
        #-- vehicle.commands.cout is the total number of waypoints
        #-- vehicle.commands.next is the waypoint the vehicle is going to
        #-- once next == cout, we just go home
        
        print ("Current WP: %d of %d "%(vehicle.commands.next, vehicle.commands.count))
        if vehicle.commands.next == vehicle.commands.count:
            print ("Final waypoint reached: go back home")

            clear_mission(vehicle)
            print ("Mission deleted")
            
            ChangeMode(vehicle,"RTL")
            mode = "BACK"
            
    elif mode == "BACK":
        if vehicle.location.global_relative_frame.alt < 1:
            print ("Switch to GROUND mode, waiting for new missions")
            mode = 'GROUND'
    time.sleep(0.5)
