from __future__ import print_function

import pymavlink.mavutil as mavutil
import sys

#mav = mavutil.mavlink_connection('udpin:' + sys.argv[1])
mav = mavutil.mavlink_connection('/dev/ttyUSB0', baud=57600)
mav.wait_heartbeat()

while True:
    m = mav.recv_match(type='HEARTBEAT', blocking=True)
    if m is not None:
        print(m)
