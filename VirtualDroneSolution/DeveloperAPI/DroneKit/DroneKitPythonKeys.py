
"""
Simple script for take off and control with arrow keys
"""


import time
from threading import Thread
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, LocationGlobal
from pymavlink import mavutil

#- Importing Tkinter: sudo apt-get install python-tk
import Tkinter as tk


#-- Connect to the vehicle
print('Connecting...')
vehicle = connect('udp:127.0.0.1:14551')

#-- Setup the commanded flying speed
gnd_speed = 5 # [m/s]
elev_speed = 1 # [m/s]

#-- Setup the commanded jaw degree
jaw_delta = 10 # [deg]

#-- Setup initial jaw angle
jaw_angle = 0 # [deg]

#-- global control variables
velocity_x = 0
velocity_y = 0
velocity_z = 0
stop = False


#-- Define arm and takeoff
def arm_and_takeoff(altitude):

   while not vehicle.is_armable:
      print("waiting to be armable")
      time.sleep(1)

   print("Arming motors")
   vehicle.mode = VehicleMode("GUIDED")
   vehicle.armed = True

   while not vehicle.armed: time.sleep(1)

   print("Taking Off")
   vehicle.simple_takeoff(altitude)

   while True:
      v_alt = vehicle.location.global_relative_frame.alt
      print(">> Altitude = %.1f m"%v_alt)
      if v_alt >= altitude - 1.0:
          print("Target altitude reached")
          break
      time.sleep(1)

 #-- Define the function for sending mavlink velocity command in body frame
def set_velocity_body(vehicle, vx, vy, vz):
    """ Remember: vz is positive downward!!!
    http://ardupilot.org/dev/docs/copter-commands-in-guided-mode.html

    Bitmask to indicate which dimensions should be ignored by the vehicle 
    (a value of 0b0000000000000000 or 0b0000001000000000 indicates that 
    none of the setpoint dimensions should be ignored). Mapping: 
    bit 1: x,  bit 2: y,  bit 3: z, 
    bit 4: vx, bit 5: vy, bit 6: vz, 
    bit 7: ax, bit 8: ay, bit 9: az


    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
            0, # time_boot_ms (not used)
            0, 0, # target_system, target_component
            mavutil.mavlink.MAV_FRAME_BODY_NED, # frame
            0b0000111111000111, #-- BITMASK -> Consider only the velocities
            0, 0, 0,        #-- POSITION
            vx, vy, vz,     #-- VELOCITY
            0, 0, 0,        #-- ACCELERATIONS (not supported yet, ignored in GCS_Mavlink)
            0, 0) 			# yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)
    vehicle.send_mavlink(msg)
    vehicle.flush()


#-- Define the function for sending mavlink condition jaw command
def set_condition_yaw(vehicle, heading, relative=False):
    if relative:
        is_relative=1 #yaw relative to direction of travel
    else:
        is_relative=0 #yaw is an absolute angle
    # create the CONDITION_YAW command using command_long_encode()
    msg = vehicle.message_factory.command_long_encode(
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
        0, #confirmation
        heading,    # param 1, yaw in degrees
        0,          # param 2, yaw speed deg/s
        0,          # param 3, direction -1 ccw, 1 cw
        is_relative, # param 4, relative offset 1, absolute angle 0
        0, 0, 0)    # param 5 ~ 7 not used
    # send command to vehicle
    vehicle.send_mavlink(msg)
    vehicle.flush()


def send_command():
    global jaw_angle, velocity_x, velocity_y, velocity_z, stop
    while not stop: 
        set_velocity_body(vehicle, velocity_x, velocity_y, velocity_z)
        set_condition_yaw(vehicle,jaw_angle)
        time.sleep(1)


#-- Key event function
def key(history):
    global gnd_speed, jaw_angle, jaw_delta, velocity_x, velocity_y, velocity_z

    if 'r' in history:
        print("r pressed >> Set the vehicle to RTL")
        stop=True
        vehicle.mode = VehicleMode("RTL")
        return

    if 'space' in history:
        vehicle.mode = VehicleMode("GUIDED")
        return

    if '1' in history:
        gnd_speed = 5
    elif '2' in history:
        gnd_speed = 10
    elif '3' in history:
        gnd_speed = 15

    velocity_x = -gnd_speed if 'Down' in history else gnd_speed if 'Up' in history else 0
    velocity_y = -gnd_speed if 'a' in history else gnd_speed if 'd' in history else 0
    velocity_z = -elev_speed if 'w' in history else elev_speed if 's' in history else 0

    if 'Left' in history: # turn left
        jaw_angle -= jaw_delta
        if jaw_angle < 0:
            jaw_angle += 360
        print("jaw: %d" % jaw_angle)
    elif 'Right' in history:  # turn right
        jaw_angle += jaw_delta
        if jaw_angle > 360:
            jaw_angle -= 360
        print("jaw: %d" % jaw_angle)


history = []
def keyup(event):
    if event.keysym in history :
        history.pop(history.index(event.keysym))
        key(history)

def keydown(event):
    if not event.keysym in history :
        history.append(event.keysym)
        key(history)


#---- MAIN FUNCTION
#- Takeoff
arm_and_takeoff(10)
Thread(target=send_command).start()

#- Read the keyboard with tkinter
root = tk.Tk()
print(">> Control the drone with the arrow keys. Press r for RTL mode")

#root.bind_all('<Key>', key)
root.bind_all("<KeyPress>", keydown)
root.bind_all("<KeyRelease>", keyup)
root.mainloop()

