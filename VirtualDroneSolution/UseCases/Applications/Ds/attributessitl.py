#!/usr/bin/python

# =============================================================================
# Libraries
# =============================================================================

import argparse
import time

from pprint import pprint

from pymavlink import mavutil, mavwp

from dronekit import connect, VehicleMode, Command


# =============================================================================
# Objects
# =============================================================================

class VehicleStates(object):
  hover = "HOVER"
  flying = "FLYING"
  takeoff = "TAKEOFF"
  unknown = "UNKNOWN"
  avoidance = "AVOIDANCE"
  landing = "LANDING"
  landed = "LANDED"

# =============================================================================
# Functions
# =============================================================================

def channels_callback(self, attr_name, value):
    print(vehicle.channels)

def rangefinder_callback(self, attr_name, value):
    print(vehicle.rangerfinder)


class DroneAttitude():

    def __init__(self):

        self.vehicle = None
        self.vehicle_initialized = False
        self.vehicle_state = VehicleStates.unknown

    def initialize(self)
        if (not self.vehicle_initialized):
            self.vehicle = dronekit.connect(self.USB, baud = self.BAUDRATE, wait_ready=True)

    def takeoff(self, target_altitude):

        self.vehicle_state = VehicleStates.takeoff

        self.arm_drone()
        self.switch_control()

        initial_alt = self.vehicle.location.global_relative_frame.alt

        while((self.vehicle.location.global_relative_frame.alt - initial_alt) < target_altitude):
            self.set_angle_thrust(StandardAttitudes.level, StandardThrusts.takeoff)
            sleep(self.STANDARD_SLEEP_TIME)

        print('Reached target altitude:{0:.2f}m'.format(self.vehicle.location.global_relative_frame.alt))

def hover(duration):

        LOITER_HOVER_THROTTLE = 1500

	vehicle.channels.overrides['3'] = LOITER_HOVER_THROTTLE

	msg = vehicle.message_factory.command_long_encode(
					0, 0,       # target system, target component
					mavutil.mavlink.MAV_CMD_NAV_LOITER_UNLIM, # command
					0,          # confirmation
					0, 0, 0, 0, # param 1-4, not used
					0, 0, 0)    # param 5-7, set 0 for current position
	vehicle.send_mavlink(msg)
	vehicle.flush()
	time.sleep(duration)
	vehicle.channels.overrides['3'] = None
	return True

# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Print out vehicle state information. Connects to SITL on local PC by default.')
    parser.add_argument('--connect',
                       help="vehicle connection target string. If not specified, SITL automatically started and used.")
    parser.add_argument('--id')
    args = parser.parse_args()

    connection_string = args.connect
    vehicleid = float(args.id)
    pwm = 1000

    # Connect to the Vehicle.
    #   Set `wait_ready=True` to ensure default attributes are populated before `connect()` returns.
    print "\nConnecting to vehicle on: %s" % connection_string
    vehicle = connect(connection_string, wait_ready=True, source_system=vehicleid)
    #vehicle = connect(connection_string, wait_ready=False, baud=57600)

    #vehicle.parameters['SYSID_THISMAV'] = vehicleid
    # Get some vehicle attributes (state)
    print "Get some vehicle attribute values:"
    print " Autopilot Firmware version: %s" % vehicle.version
    #print " Autopilot capabilities (supports ftp): %s" % vehicle.capabilities.ftp
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
    print " Vehicle Id: %s" % vehicle.parameters
    print " Vehicle Id: %s" % vehicle.parameters["SYSID_THISMAV"]
    print " Param: %s" % vehicle.parameters['WP_YAW_BEHAVIOR']
    #print vehicle.parameters
    #pprint(vars(vehicle.parameters))
    for property, value in vars(vehicle).iteritems():
        print property, ": ", value

    #vehicle.mode = VehicleMode("GUIDED")
    print vehicle.mode

    #vehicle.add_attribute_listener('channels', channels_callback)
    vehicle.add_attribute_listener('rangefinder', rangefinder_callback)

    hover(5)

    while pwm < 1005:
        SERVO_CHANNEL=1
        rgb_led = vehicle.message_factory.command_long_encode(
            vehicleid,     # target_system
            0,             # target component
            mavutil.mavlink.MAV_CMD_DO_SET_SERVO, #command
            0,             #confirmation
            8,             # param 1, Servo number
            pwm,           # PWM value
            0, 0, 0, 0, 0) # param 3 ~ 7 not used
        vehicle.send_mavlink(rgb_led)
        vehicle.flush()
        #Command(1,1,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
        #          mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
        #          0,1,SERVO_CHANNEL,pwm,0,0,0,0,0)
        time.sleep(1)
        pwm += 1

    vehicle.remove_attribute_listener('channels', altitude_callback)
    vehicle.remove_attribute_listener('rangefinder', altitude_callback)

    vehicle.close()

    print("Completed")
