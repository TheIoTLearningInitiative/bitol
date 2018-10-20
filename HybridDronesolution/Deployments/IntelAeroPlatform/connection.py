import time
import sys
from pymavlink import mavutil

master = mavutil.mavlink_connection('udpin:0.0.0.0:14550')

master.wait_heartbeat()
mode = 'STABILIZED'

if mode not in master.mode_mapping():
    print('Unknown mode : {}'.format(mode))
    print('Try:', list(master.mode_mapping().keys()))
    exit(1)

mode_id = master.mode_mapping()
print mode_id

master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0,
    1, 0, 0, 0, 0, 0, 0)

master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0,
    0, 0, 0, 0, 0, 0, 0)


sys.exit(0)

master.mav.set_mode_send(
    master.target_system,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    mode_id)

while True:
    try:
        print(master.recv_match().to_dict())
    except:
        pass
    time.sleep(0.1)
