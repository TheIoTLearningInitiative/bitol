#!/usr/bin/python

# =============================================================================
# https://github.com/LU-Jiale/MSc_CXmodel-Drone
# https://github.com/LU-Jiale/cx_model_drone
# https://github.com/Drones4STEM/DroneController/
# https://github.com/MST-MRR/IARC-2018
# https://github.com/alduxvm/DronePilot
# https://github.com/intel-aero/meta-intel-aero/wiki
# =============================================================================

# =============================================================================
# D1L D1M D2L D2M D3L D3M D4L D4M D5L D5M D6L D6M D7L D7M D8L D8M
# =============================================================================

# =============================================================================
# Libraries
# =============================================================================

import argparse
import csv
import math
import sys
import threading
import time
from time import sleep
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

class DroneAttitude():

  def __init__(self, roll, pitch, yaw):
    self.pitch_deg = pitch
    self.yaw_deg = yaw
    self.roll_deg = roll
    self.pitch = math.radians(pitch)
    self.yaw = math.radians(yaw)
    self.roll = math.radians(roll)
    self.quaternion = self.get_quaternion()

  def get_quaternion(self):
    q = []

    t0 = math.cos(self.yaw * 0.5)
    t1 = math.sin(self.yaw * 0.5)
    t2 = math.cos(self.roll * 0.5)
    t3 = math.sin(self.roll * 0.5)
    t4 = math.cos(self.pitch * 0.5)
    t5 = math.sin(self.pitch * 0.5)

    w = t0 * t2 * t4 + t1 * t3 * t5
    x = t0 * t3 * t4 - t1 * t2 * t5
    y = t0 * t2 * t5 + t1 * t3 * t4
    z = t1 * t2 * t4 - t0 * t3 * t5

    q.append(w)
    q.append(x)
    q.append(y)
    q.append(z)

    return q

class StandardAttitudes(object):
    level = DroneAttitude(0,0,0)
    forward = DroneAttitude(0,-5,0)
    backward = DroneAttitude(0,5,0)
    left = DroneAttitude(-5, 0, 0)
    right = DroneAttitude(5, 0, 0)

class StandardThrusts(object):
    none = 0.00
    hover = 0.525
    takeoff = 0.75
    full = 1.00

class Lights(threading.Thread):

    def __init__(self, atc_instance):
        self.atc = atc_instance
        self.stoprequest = threading.Event()
        super(Lights, self).__init__()

    def run(self):
        while not self.stoprequest.isSet():
            if self.atc.STATE == VehicleStates.hover or self.atc.STATE == VehicleStates.flying:
            #self.atc.check_sonar_sensors()
            #self.atc.check_battery_voltage()
                sleep(0.1)

    def start_lights(self):
        pwm = 1000
        while pwm < 1005:
            SERVO_CHANNEL=1
            rgb_led = self.vehicle.message_factory.command_long_encode(
                self.vehicle_id,     # target_system
                0,             # target component
                mavutil.mavlink.MAV_CMD_DO_SET_SERVO, #command
                0,             #confirmation
                8,             # param 1, Servo number
                pwm,           # PWM value
                0, 0, 0, 0, 0) # param 3 ~ 7 not used
            self.vehicle.send_mavlink(rgb_led)
            self.vehicle.flush()
            #Command(1,1,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
            #          mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
            #          0,1,SERVO_CHANNEL,pwm,0,0,0,0,0)
            time.sleep(1)
            pwm += 1

class Drone():

    def __init__(self, vehicle_connection, vehicle_id):

        self.vehicle = None
        self.vehicle_connection = vehicle_connection
        self.vehicle_id = vehicle_id
        self.vehicle_initialized = False
        self.vehicle_state = VehicleStates.unknown
        self.LAND_ALTITUDE = 0.5
        self.STANDARD_ATTITUDE_BIT_FLAGS = 0b00111111

    def channels_callback(self, attr_name, value):
        print(vehicle.channels)

    def rangefinder_callback(self, attr_name, value):
        print(vehicle.rangerfinder)

    def start_callbacks(self):
        self.vehicle.add_attribute_listener('channels', self.channels_callback)
        self.vehicle.add_attribute_listener('rangefinder', self.rangefinder_callback)

    def stop_callbacks(self):
        self.vehicle.remove_attribute_listener('channels', self.channels_callback)
        self.vehicle.remove_attribute_listener('rangefinder', self.rangefinder_callback)

    def start_lights(self):
        pwm = 1000
        while pwm < 1005:
            SERVO_CHANNEL=1
            rgb_led = self.vehicle.message_factory.command_long_encode(
                self.vehicle_id,     # target_system
                0,             # target component
                mavutil.mavlink.MAV_CMD_DO_SET_SERVO, #command
                0,             #confirmation
                8,             # param 1, Servo number
                pwm,           # PWM value
                0, 0, 0, 0, 0) # param 3 ~ 7 not used
            self.vehicle.send_mavlink(rgb_led)
            self.vehicle.flush()
            #Command(1,1,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
            #          mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
            #          0,1,SERVO_CHANNEL,pwm,0,0,0,0,0)
            time.sleep(1)
            pwm += 1

    def switch_control(self):
        #if not self.failsafes:
        #    self.failsafes = FailsafeController(self)
        #    self.failsafes.start()
        #print self.vehicle.mode.name
        if self.vehicle.mode.name != "GUIDED_NOGPS":
            self.vehicle.mode = VehicleMode("GUIDED_NOGPS")
            while(self.vehicle.mode.name != "GUIDED_NOGPS"):
                sleep(1)

    def set_angle_thrust(self, attitude, thrust):
        while(self.vehicle.mode.name != "GUIDED_NOGPS"):
             sleep(1)
        message = self.vehicle.message_factory.set_attitude_target_encode(
            0,                                 # Timestamp in milliseconds since system boot (not used).
            0,                                 # System ID
            0,                                 # Component ID
            self.STANDARD_ATTITUDE_BIT_FLAGS,  # Bit flags. 
            attitude.quaternion,               # Attitude quaternion.
            0,                                 # Body roll rate.
            0,                                 # Body pitch rate.
            0,                                 # Body yaw rate.
            thrust                             # Collective thrust, from 0-1.
        )
        self.vehicle.send_mavlink(message)
        self.vehicle.commands.upload()
        self.last_attitude = attitude
        self.last_thrust = thrust

    def connect(self):

        if (not self.vehicle_initialized):

            print "\nConnecting to vehicle on: %s" % self.vehicle_connection
            #self.vehicle = dronekit.connect(self.USB, baud = self.BAUDRATE, wait_ready=True)
            #self.vehicle = connect(self.vehicle_connection, wait_ready=True, source_system=self.vehicle_id)
            self.vehicle = connect(self.vehicle_connection, wait_ready=False, baud=57600, source_system=self.vehicle_id)

            if not self.vehicle:
                print("\nUnable to connect to vehicle.")
                return

            time.sleep(5)

            #vehicle.parameters['SYSID_THISMAV'] = vehicleid
            # Get some vehicle attributes (state)
            print " Autopilot Firmware version: %s" % self.vehicle.version
            print " Rangefinder: %s" % self.vehicle.rangefinder
            print " Rangefinder distance: %s" % self.vehicle.rangefinder.distance
            print " Rangefinder voltage: %s" % self.vehicle.rangefinder.voltage
            print " Armed: %s" % self.vehicle.armed
            print " Is Armable?: %s" % self.vehicle.is_armable
            print " System status: %s" % self.vehicle.system_status.state
            print " Mode: %s" % self.vehicle.mode.name
            #print " Vehicle Id: %s" % self.vehicle.parameters["SYSID_THISMAV"]
            #print " Param: %s" % self.vehicle.parameters['WP_YAW_BEHAVIOR']

            #self.vehicle.mode = VehicleMode("STABILIZE")
            self.vehicle.mode = VehicleMode("LOITER")
            print self.vehicle.mode
            sleep(3)
            self.STATE = VehicleStates.landed
            self.vehicle_initialized = True

    def arm(self):
        self.vehicle.armed = True
        #mav.mav.command_long_send(mav.target_system, mav.target_component,
        #                  mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1,
        #                  0, 0, 0, 0, 0, 0)
        while ( not self.vehicle.armed ):
            sleep(1)

    def takeoff(self, target_altitude):

        self.vehicle_state = VehicleStates.takeoff
        self.switch_control()

        initial_alt = self.vehicle.location.global_relative_frame.alt

        while((self.vehicle.location.global_relative_frame.alt - initial_alt) < target_altitude):
            self.set_angle_thrust(StandardAttitudes.level, StandardThrusts.takeoff)
            sleep(1)

        print('Reached target altitude:{0:.2f}m'.format(self.vehicle.location.global_relative_frame.alt))

    def land(self):
        self.vehicle.mode = VehicleMode("LAND")
        self.STATE = VehicleStates.landing
        #while((self.vehicle.location.global_relative_frame.alt) >= self.LAND_ALTITUDE):
        #    sleep(1)
        #else:
        #    self.STATE = VehicleStates.landed
        self.STATE = VehicleStates.landed

    def disarm(self):
        self.vehicle.armed = False
        #mav.mav.command_long_send(mav.target_system, mav.target_component,
        #                  mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 0,
        #                  0, 0, 0, 0, 0, 0)
        while(self.vehicle.armed):
            sleep(1)

    def disconnect(self):
        self.vehicle.close()

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

    parser = argparse.ArgumentParser(description='Drone S')
    parser.add_argument('--connect',
                       help="Vehicle Connection")
    parser.add_argument('--id',
                       help="Vehicle Identification")
    args = parser.parse_args()

    vehicle_connection = args.connect
    vehicle_id = float(args.id)

    with open("Sequence.txt") as csvfile:
        content = csv.reader(csvfile, delimiter=',')
        for row in content:
            if len(row) == 8:
                print "Commands"
                for drone in row:
                    print drone

    quintanaroo = Drone(vehicle_connection, vehicle_id)
    quintanaroo.connect()
    quintanaroo.arm()
    #quintanaroo.start_callbacks()
    #quintanaroo.start_lights()
    quintanaroo.takeoff(2)
    #sleep(5)
    quintanaroo.land()
    #quintanaroo.stop_callbacks()
    quintanaroo.disarm()
    quintanaroo.disconnect()

    print("Completed")
