#!/usr/bin/python
from __future__ import print_function

import pymavlink.mavutil as mavutil
import sys
import time

mav = mavutil.mavlink_connection('192.168.1.2:14550')
#mav = mavutil.mavlink_connection('/dev/ttyUSB0', baud=57600)
mav.wait_heartbeat()
mav.mav.command_long_send(0, 0,
                          mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1,
                          0, 0, 0, 0, 0, 0)
time.sleep(5)
mav.mav.command_long_send(0, 0,
                          mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 0,
                          0, 0, 0, 0, 0, 0)
