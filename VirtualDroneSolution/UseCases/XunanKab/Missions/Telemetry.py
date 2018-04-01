#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Thanks Tiziano Fiorenzani for teaching us!
https://github.com/tizianofiorenzani

This script will introduce multiple things:
- Run the simulator inside dronekit
- Read and handle telemetry from the UAV
- Read and change parameters
"""

# =============================================================================
# Libraries
# =============================================================================

import argparse
import time

from dronekit import connect, VehicleMode

# =============================================================================
# Init
# =============================================================================

parser = argparse.ArgumentParser(description='commands')
parser.add_argument('--connect')
parser.add_argument('--id')
args = parser.parse_args()

connection_string = args.connect
vehicleid = float(args.id)

print("Connection to the vehicle on %s" % connection_string)
vehicle = connect(connection_string, wait_ready=True)
vehicle.wait_ready('autopilot_version')
print('Autopilot Version: %s' % vehicle.version)

# =============================================================================
# Functions
# =============================================================================

# None

# =============================================================================
# Main
# =============================================================================

print("Vehicle ID Old: %d" % vehicle.parameters['SYSID_THISMAV']) 
vehicle.parameters['SYSID_THISMAV'] = vehicleid
time.sleep(1)
print("Vehicle ID New: %d" % vehicle.parameters['SYSID_THISMAV'])

time.sleep(1)

print('Supports set attitude from companion: %s' % vehicle.capabilities.set_attitude_target_local_ned)
print('Position: %s' % vehicle.location.global_relative_frame)
print('Attitude: %s' % vehicle.attitude)
print('Velocity: %s' % vehicle.velocity)
print('Last Heartbeat: %s' % vehicle.last_heartbeat)
print('Is the vehicle armable: %s' % vehicle.is_armable)
print('Groundspeed: %s' % vehicle.groundspeed)
print('Mode: %s' % vehicle.mode.name)
print('Armed: %s' %vehicle.armed)
print('EKF Ok: %s' %vehicle.ekf_ok)

def attitude_callback(self, attr_name, value):
    print(vehicle.attitude)

vehicle.add_attribute_listener('attitude', attitude_callback)
time.sleep(5)
vehicle.remove_attribute_listener('attitude', attitude_callback)

vehicle.close()
