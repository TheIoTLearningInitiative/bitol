#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dronekit import connect, VehicleMode
import time

import dronekit_sitl

sitl = dronekit_sitl.start_default()   #(sitl.start)
connection_string = sitl.connection_string()

vehicle = connect(connection_string, wait_ready=True)

vehicle.wait_ready('autopilot_version')
print('Autopilot version: %s'%vehicle.version)

print('Supports set attitude from companion: %s'%vehicle.capabilities.set_attitude_target_local_ned)
print('Position: %s'% vehicle.location.global_relative_frame)
print('Attitude: %s'% vehicle.attitude)
print('Velocity: %s'%vehicle.velocity) #- North, east, down
print('Last Heartbeat: %s'%vehicle.last_heartbeat)
print('Is the vehicle armable: %s'%vehicle.is_armable)
print('Groundspeed: %s'% vehicle.groundspeed) #(%)
print('Mode: %s'% vehicle.mode.name)
print('Armed: %s'%vehicle.armed)
print('EKF Ok: %s'%vehicle.ekf_ok)

def attitude_callback(self, attr_name, value):
    print(vehicle.attitude)

vehicle.add_attribute_listener('attitude', attitude_callback)
time.sleep(5)
vehicle.remove_attribute_listener('attitude', attitude_callback) #(.remove)

print("Maximum Throttle: %d"%vehicle.parameters['THR_MIN']) 

vehicle.parameters['THR_MIN'] = 50
time.sleep(1)
print("Maximum Throttle: %d"%vehicle.parameters['THR_MIN'])

vehicle.close()
sitl.stop()
